import random

from django.conf import settings

from apps.users.models import UserProfile


def generate_lib_card_no():
    while True:
        library_card_no = settings.LIBRARY_CARD_NO_PREFIX + str(
            random.randint(10000000000000, 99999999999999)
        )
        if not UserProfile.objects.filter(library_card_number=library_card_no).exists():
            return library_card_no
