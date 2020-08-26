from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from apps.users import serializers
from apps.users import tokens
from apps.users.models import AlertPreference
from .tasks import email_account_activation, email_password_reset


class ProfileView(GenericAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(self.serializer_class(request.user).data)

    @swagger_auto_schema(request_body=serializers.UserUpdateSerializer)
    def put(self, request):
        serializer = serializers.UserUpdateSerializer(request.user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)


class AlertPreferencesView(GenericAPIView):
    serializer_class = serializers.AlertPreferenceSerializer
    permission_classes = [IsAuthenticated]

    operation_description = "User alert preferences. \
                'percentage_down' - Sudden price dip alert, default 3%. \
                'percentage_down_forecast' - Expected price drop alert, default 3%."

    @swagger_auto_schema(operation_description=operation_description)
    def get(self, request):
        queryset = AlertPreference.objects.get(user=request.user)
        serializer = serializers.AlertPreferenceSerializer(queryset)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=serializers.AlertPreferenceSerializer,
                         operation_description=operation_description)
    def put(self, request):
        queryset = AlertPreference.objects.get(user=request.user)
        serializer = serializers.AlertPreferenceSerializer(queryset, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)


class RegisterView(GenericAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = [AllowAny]

    @staticmethod
    def get(request):
        """
        @api {get} /users/register/ Request registration page
        @apiName RegisterView
        @apiGroup UserRegistration
        """
        return Response("Page: Registration page")

    @staticmethod
    def post(request):
        """
        @api {post} /users/register/ Request user registration
        @apiName RegisterView
        @apiGroup UserRegistration
        @apiParam {String} first_name User's first_name.
        @apiParam {String} last_name User's last_name.
        @apiParam {String} email User's email.
        @apiParam {String} username User's username.
        @apiParam {String} password User's password.
        @apiSuccess redirect to /users/register-done/
        """
        serializer = serializers.UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors)

        user_new = User.objects.create(is_active=False, **serializer.validated_data)
        user_new.set_password(serializer.validated_data['password'])
        user_new.save()

        AlertPreference.objects.create(user=user_new)

        email_account_activation.delay(
            user_pk=user_new.pk,
            domain=get_current_site(request).domain,
            uid_encoded=urlsafe_base64_encode(force_bytes(user_new.pk)),
            token=tokens.account_activation_token.make_token(user_new)
        )

        return redirect('user_register_done')


class ActivateView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.UserSerializer

    @staticmethod
    def get(request, uid_encoded, token):
        """
        @api {get} /users/activate/encoded_uid/token Request user activation
        @apiName ActivateView
        @apiGroup UserActivation
        """
        # Check if link is valid
        try:
            uid = force_text(urlsafe_base64_decode(uid_encoded))
        except(TypeError, ValueError, OverflowError):
            return Response(status.HTTP_404_NOT_FOUND)

        user = User.objects.filter(pk=uid).first()

        # Check if requested user exists and activation token is valid
        if user is None or not tokens.account_activation_token.check_token(user, token):
            return Response(status.HTTP_404_NOT_FOUND)

        # Activate user
        user.is_active = True
        user.save()

        return redirect('user_activate_done')


class PasswordResetView(GenericAPIView):
    serializer_class = serializers.PasswordResetSerializer
    permission_classes = [AllowAny]

    @staticmethod
    def get(request):
        """
        @api {get} /users/password-reset/ Request password reset
        @apiName PasswordResetView
        @apiGroup UserPasswordReset
        """
        return Response("Page: Reset password page")

    @staticmethod
    def post(request):
        """
        @api {post} /users/password-reset/ Confirm password reset
        @apiName PasswordResetView
        @apiGroup UserPasswordReset
        @apiParam {String} email User's email.
        """
        serializer = serializers.PasswordResetSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors)

        user = User.objects.filter(email=serializer.validated_data['email']).first()

        if user is not None:
            email_password_reset.delay(
                user_pk=user.pk,
                domain=get_current_site(request).domain,
                uid_encoded=urlsafe_base64_encode(force_bytes(user.pk)),
                token=tokens.password_reset_token.make_token(user)
            )

        return redirect('password_reset_done')


class PasswordChangeView(GenericAPIView):
    serializer_class = serializers.PasswordChangeSerializer
    permission_classes = [AllowAny]

    @staticmethod
    def get(request, uid_encoded, token):
        """
        @api {get} /users/password-change/uid_encoded/token Request password change page
        @apiName PasswordChangeView
        @apiGroup UserPasswordChange
        """
        # Check if link is valid
        try:
            uid = force_text(urlsafe_base64_decode(uid_encoded))
        except(TypeError, ValueError, OverflowError):
            return Response(status.HTTP_404_NOT_FOUND)

        user = User.objects.filter(pk=uid).first()

        if user is None or not tokens.account_activation_token.check_token(user, token):
            return Response(status.HTTP_404_NOT_FOUND)

        return Response("Page: password change page")

    @staticmethod
    def post(request, uid_encoded, token):
        """
        @api {post} /users/password-change/uid_encoded/token Request password change page
        @apiName PasswordChangeView
        @apiGroup Users
        @apiParam {String} password1 User's new password.
        @apiParam {String} password2 User's new password confirm.
        """
        # Check if link is valid
        try:
            uid = force_text(urlsafe_base64_decode(uid_encoded))
        except(TypeError, ValueError, OverflowError):
            return Response(status.HTTP_404_NOT_FOUND)

        user = User.objects.filter(pk=uid).first()

        if user is None or not tokens.account_activation_token.check_token(user, token):
            return Response(status.HTTP_404_NOT_FOUND)

        # Check if request data is valid
        serializer = serializers.PasswordChangeSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors)

        # Change password
        user.set_password(serializer.validated_data['password1'])
        user.save()

        return redirect('password_change_done')


class RegisterDoneView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.UserSerializer

    @staticmethod
    def get(request):
        """
        @api {get} /users/register-done/ Request register-done page
        @apiName RegisterDoneView
        @apiGroup UserRegistration
        """
        return Response(
            "Page: Account is successfully registered. Please follow email link for activation.",
            status=status.HTTP_201_CREATED,

        )


class ActivateDoneView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.UserSerializer

    @staticmethod
    def get(request):
        """
        @api {get} /users/activate-done/ Request activate-done page
        @apiName ActivateDoneView
        @apiGroup UserActivation
        """
        return Response("Page: Account is successfully activated.")


class PasswordResetDoneView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.UserSerializer

    @staticmethod
    def get(request):
        """
        @api {get} /users/password-reset-done/ Request password-reset-done page
        @apiName PasswordResetDoneView
        @apiGroup UserPasswordReset
        """
        return Response("Page: Password reset link is send to your email.")


class PasswordChangeDoneView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.UserSerializer

    @staticmethod
    def get(request):
        """
        @api {get} /users/password-change-done/ Request password-change-done page
        @apiName PasswordChangeDoneView
        @apiGroup UserPasswordChange
        """
        return Response("Page: Password successfully changed.")
