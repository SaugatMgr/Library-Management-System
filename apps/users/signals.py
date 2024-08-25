# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from apps.users.api.v1.helpers import generate_lib_card_no

# from apps.users.models import CustomUser, UserProfile


# @receiver(post_save, sender=CustomUser)
# def create_user_profile(sender, instance, created, **kwargs):
#     library_card_number = generate_lib_card_no()
#     data = {"user": instance, "library_card_number": library_card_number}
#     if created:
#         UserProfile.objects.create(**data)
#     else:
#         if not UserProfile.objects.filter(user=instance).exists():
#             UserProfile.objects.create(**data)
#         else:
#             instance.userprofile.save()
