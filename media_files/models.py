from django.db import models
from django.utils import timezone # Timezone
from django.core.exceptions import ValidationError
from PIL import Image as PILImage
import io
from .fields import ThumbnailLanguageField, VideoLanguageField, ClientField, GameField # Adjust the import path as needed
from embed_video.fields import EmbedVideoField
from django.utils.translation import gettext_lazy as _

# Create your models here.

def validate_image_file(image):
    try:
        image_file = io.BytesIO(image.read())
        PILImage.open(image_file).verify()
    except (IOError, SyntaxError) as e:
        raise ValidationError('Uploaded file is not a valid image.')

class Thumbnails(models.Model):
    """Model representing a thumbnail."""
    title = models.CharField(max_length=100,blank=False, null=False)
    image = models.ImageField(upload_to='thumbnails/',null=True,blank=False, validators=[validate_image_file])
    language = ThumbnailLanguageField()
    game = GameField()
    date_uploaded = models.DateField(default=timezone.now)

    def clean(self):
        # Validate that the title is a string
        if not isinstance(self.title, str):
            print(f"Title is not a string before conversion: {self.title} (type: {type(self.title)})")
            raise ValidationError('Title must be a string')

    def save(self, *args, **kwargs):
        # Perform the type check before saving
        if not isinstance(self.__dict__['title'], str):
            print(f"Title is not a string before conversion in save: {self.__dict__['title']} (type: {type(self.__dict__['title'])})")
            raise ValidationError('Title must be a string')

        # Call the original save method with proper arguments
        super().save(*args, **kwargs)

    # Generic truncate method
    def _truncate(self, value):
        """Helper method to truncate a string."""
        max_length = 20

        if isinstance(value, str) and value:
            if len(value) > max_length:
                return value[:max_length] + '...'
        return value  # Return an empty string or some default value

    @property
    def truncated_title(self):
        return self._truncate(self.title)

    @property
    def truncated_game(self):
        return self._truncate(self.game)

    def __str__(self):
        """String for representing the Model object."""
        if not isinstance(self.title, str):
            return 'No Title or Game needed to be truncated'
        truncated_title = self.truncated_title
        truncated_game = self.truncated_game

        if truncated_title == self.title and truncated_game == self.game:
            return 'No Title or Game needed to be truncated'
        elif truncated_title != self.title:
            return truncated_title
        elif truncated_game != self.game:
            return truncated_game
        return 'No Title or Game needed to be truncated'

    class Meta:
        verbose_name = 'Thumbnail'
        verbose_name_plural = 'Thumbnails'

class Videos(models.Model):
    """Model representing a video."""
    title = models.CharField(max_length=200,blank=False, null=True)
    video = EmbedVideoField(null=True,blank=False)  # same like models.URLField()
    language = VideoLanguageField()
    game = GameField()
    client = ClientField()
    views = models.IntegerField(null=True, blank=True, default=0)
    likes = models.IntegerField(null=True, blank=True, default=0)
    date_uploaded = models.DateField(default=timezone.now)

    # Setting the default views and likes to 0
    def save(self, *args, **kwargs):
        # Set default values if fields are None
        if self.views is None:
            self.views = 0
        if self.likes is None:
            self.likes = 0
        super().save(*args, **kwargs)

    # Generic truncate method
    def _truncate(self, value):
        """Helper method to truncate a string."""
        max_length = 20

        if isinstance(value, str) and value:
            if len(value) > max_length:
                return value[:max_length] + '...'
        return value  # Return an empty string or some default value

    @property
    def truncated_title(self):
        return self._truncate(self.title)

    @property
    def truncated_game(self):
        return self._truncate(self.game)

    def __str__(self):
        """String for representing the Model object."""
        truncated_title = self._truncate(self.title)
        truncated_game = self._truncate(self.game)

        if truncated_title:
            return truncated_title
        elif truncated_game:
            return truncated_game
        else:
            return self.title or self.game

    class Meta:
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'