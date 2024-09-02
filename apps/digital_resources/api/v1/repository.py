from typing import List

from apps.digital_resources.models import DigitalResource


class DigitalResourcesRepository:
    @classmethod
    def get_all(cls) -> List[DigitalResource]:
        return DigitalResource.objects.filter()
