from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from apps.wallet.models import RatesHistory
from config.elastic import es


@receiver(post_save, sender=RatesHistory)
def update_es_history_record(sender, instance, **kwargs):
    queryset = sender.objects.get(id=instance.id)
    es.index(
        index='curs-valutar-rateshistory',
        body=queryset.es_doc(),
        id=instance.id
    )


@receiver(pre_delete, sender=RatesHistory)
def delete_es_history_record(sender, instance, *args, **kwargs):
    es.delete(
        index='curs-valutar-rateshistory',
        id=instance.id
    )
