from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, StatusLog

@receiver(post_save, sender=Order)
def track_status_update(sender, instance, created, **kwargs):
    if not created and 'status' in instance.changed_fields:
        old_status = instance.get_field_value('status', instance.changed_fields['status'][0])
        new_status = instance.status
        StatusLog.objects.create(order=instance, old_status=old_status, new_status=new_status)
