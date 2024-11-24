from django.conf import settings
from django.db.models.signals import post_save # pre_save,post_delete,pre_delete
from django.dispatch import receiver
from store.models import Staff

# Using signals to create customer
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_customer_for_new_user(sender,**kwargs):

	if kwargs['created']:
		Staff.objects.create(user=kwargs['instance'])