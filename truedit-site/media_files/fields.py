from django.db import models

class ThumbnailLanguageField(models.CharField):
    description = "Field to store the language of the thumbnail content"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 50  # Set a default max_length if not provided
        kwargs['null'] = True  # Allow null values
        kwargs['blank'] = True  # Allow blank values in forms
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        # Ensure args is an empty tuple
        args = ()
        # Remove 'max_length' from kwargs if it is the default value
        if kwargs.get('max_length', None) == 50:
            del kwargs['max_length']
        return name, path, args, kwargs

class VideoLanguageField(models.CharField):
    description = "Field to store the language of the video content"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 50  # Set a default max_length if not provided
        kwargs['null'] = True  # Allow null values
        kwargs['blank'] = False  # Don't allow blank values in forms
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        # Ensure args is an empty tuple
        args = ()
        # Remove 'max_length' from kwargs if it is the default value
        if kwargs.get('max_length', None) == 50:
            del kwargs['max_length']
            # Ensure that 'null' and 'blank' are included in kwargs
        kwargs['null'] = self.null
        kwargs['blank'] = self.blank
        return name, path, args, kwargs

class ClientField(models.CharField):
    description = "Field to store the client of the content"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 50  # Set a default max_length if not provided
        kwargs['null'] = True  # Allow null values
        kwargs['blank'] = True  # Allow blank values in forms
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        # Ensure args is an empty tuple
        args = ()
        # print(f"Deconstruct called: Name={name}, Path={path}, Args={args}, Kwargs={kwargs}")
        # Remove 'max_length' from kwargs if it is the default value
        if kwargs.get('max_length', None) == 50:
            del kwargs['max_length']
        return name, path, args, kwargs

class GameField(models.CharField):
    description = "Field to store the game of the content"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 100  # Set a default max_length if not provided
        kwargs['null'] = False  # Don't allow null values
        kwargs['blank'] = False  # Don't allow blank values in forms
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        # Ensure args is an empty tuple
        args = ()
        # Remove 'max_length' from kwargs if it is the default value
        if kwargs.get('max_length', None) == 100:
            del kwargs['max_length']
        # Ensure that 'null' and 'blank' are included in kwargs
        kwargs['null'] = self.null
        kwargs['blank'] = self.blank
        return name, path, args, kwargs