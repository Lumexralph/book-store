from io import BytesIO
import logging

from PIL import Image
from django.core.files.base import ContentFile
from django.db.models.signals import pre_save
from django.dispatch import receiver
from main.models import ProductImage


THUMBNAIL_SIZE = (300, 300)

logger = logging.getLogger(__name__)


@receiver(pre_save, sender=ProductImage)
def generate_thumbnail(sender, instance, **kwargs):
    logger.info('Generating thumbnail for product %d', instance.product.id)
    image = Image.open(instance.image)
    image = image.convert('RGB')
    image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)
    temp_thumb = BytesIO()          # create a temporary in-memory buffer
    image.save(temp_thumb, "JPEG")  # save the image as JPEG format
    temp_thumb.seek(0)              # move the start of the sequence of bytes

    # set save=False otherwise it will run in infinite loop
    instance.thumbnail.save(
        instance.image.name,
        ContentFile(temp_thumb.read()),
        save=False,
    )

    # close the open file, to free up resources i.e bytes used from memory
    temp_thumb.close()
