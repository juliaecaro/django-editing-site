from django.test import TestCase
from media_files.fields import ThumbnailLanguageField, VideoLanguageField, ClientField, GameField
from media_files.models import Thumbnails, Videos
from django.core.exceptions import ValidationError

# CLIENT FIELD TESTS
class ClientFieldTests(TestCase):

  def setUp(self):
    """Set up any required data for testing."""
    self.model_with_client = Videos(client="Test Client")
    self.model_without_client = Videos()

  def test_client_field_max_length(self):
    """Test that the client field has the correct max_length."""
    max_length = self.model_with_client._meta.get_field('client').max_length
    self.assertEqual(max_length, 50)

  def test_client_field_null(self):
    """Test that the client field can be null."""
    self.assertTrue(self.model_without_client._meta.get_field('client').null)

  def test_client_field_blank(self):
    """Test that the client field can be blank."""
    self.assertTrue(self.model_without_client._meta.get_field('client').blank)

  def test_save_client_field(self):
    """Test saving a model with a client field."""
    self.model_with_client.save()
    saved_model = Videos.objects.get(id=self.model_with_client.id)
    self.assertEqual(saved_model.client, "Test Client")

  def test_client_field_validation(self):
    """Test validation of the client field (if any specific validation)."""
    with self.assertRaises(ValidationError):
      self.model_with_client.client = ""
      self.model_with_client.full_clean()  # This will trigger validation

  def test_deconstruct(self):
    # Create an instance of the custom field
    field = ClientField()

    # Deconstruct the field
    name, path, args, kwargs = field.deconstruct()

    # # Print debug information
    # print(f"Name: {name}, Path: {path}, Args: {args}, Kwargs: {kwargs}")

    # Assert the name of the field
    self.assertIsNone(name)

    # Assert the path of the field class
    self.assertEqual(path, 'media_files.fields.ClientField')  # Adjust based on the actual path

    # Assert the arguments passed
    self.assertEqual(args, ())

    # Assert the keyword arguments
    # Check that max_length is not in kwargs as it is the default
    self.assertNotIn('max_length', kwargs)

    # Check other default kwargs
    self.assertEqual(kwargs, {'null': True, 'blank': True})

# GAME FIELD TESTS
class GameFieldTests(TestCase):

  def setUp(self):
    """Set up any required data for testing."""
    self.model_with_game = Thumbnails(game="Test Game")
    self.model_without_game = Thumbnails()

  def test_game_field_max_length(self):
      """Test that the GameField has the correct max_length."""
      max_length = self.model_with_game._meta.get_field('game').max_length
      self.assertEqual(max_length, 100)

  def test_game_field_null(self):
      """Test that the GameField does not allow null values."""
      field = self.model_with_game._meta.get_field('game')
      self.assertFalse(field.null)

  def test_game_field_blank(self):
      """Test that the GameField does not allow blank values."""
      field = self.model_with_game._meta.get_field('game')
      self.assertFalse(field.blank)

  def test_save_game_field(self):
      """Test saving a model with a GameField."""
      self.model_with_game.save()
      saved_model = Thumbnails.objects.get(id=self.model_with_game.id)
      self.assertEqual(saved_model.game, "Test Game")

  def test_deconstruct(self):
      """Test the deconstruct method of the GameField."""
      # Create an instance of the custom field
      field = GameField()
      name, path, args, kwargs = field.deconstruct()

      self.assertIsNone(name)
      self.assertEqual(path, 'media_files.fields.GameField')
      self.assertEqual(args, ())
      self.assertEqual(kwargs, {'null': False, 'blank': False})

# THUMBNAIL LANGUAGE FIELD TESTS
class ThumbnailLanguageFieldTests(TestCase):

  def setUp(self):
      """Set up any required data for testing."""
      self.model_with_language = Thumbnails(language="Spanish")
      self.model_without_language = Thumbnails()

  def test_language_field_max_length(self):
      """Test that the ThumbnailLanguageField has the correct max_length."""
      max_length = self.model_with_language._meta.get_field('language').max_length
      self.assertEqual(max_length, 50)

  def test_language_field_null(self):
      """Test that the ThumbnailLanguageField allows null values."""
      field = self.model_with_language._meta.get_field('language')
      self.assertTrue(field.null)

  def test_language_field_blank(self):
      """Test that the ThumbnailLanguageField allows blank values."""
      field = self.model_with_language._meta.get_field('language')
      self.assertTrue(field.blank)

  def test_save_language_field(self):
      """Test saving a model with a ThumbnailLanguageField."""
      self.model_with_language.save()
      saved_model = Thumbnails.objects.get(id=self.model_with_language.id)
      self.assertEqual(saved_model.language, "Spanish")

  def test_deconstruct(self):
      """Test the deconstruct method of the ThumbnailLanguageField."""
      # Create an instance of the field
      field = ThumbnailLanguageField()
      name, path, args, kwargs = field.deconstruct()

      self.assertIsNone(name)
      self.assertEqual(path, 'media_files.fields.ThumbnailLanguageField')  # Adjust path if needed
      self.assertEqual(args, ())
      self.assertEqual(kwargs, {'null': True, 'blank': True})

# VIDEO LANGUAGE FIELD TESTS
class VideoLanguageFieldTests(TestCase):

  def setUp(self):
      """Set up any required data for testing."""
      self.model_with_language = Videos(language="English")
      self.model_without_language = Videos()

  def test_language_field_max_length(self):
      """Test that the VideoLanguageField has the correct max_length."""
      max_length = self.model_with_language._meta.get_field('language').max_length
      self.assertEqual(max_length, 50)

  def test_language_field_null(self):
      """Test that the VideoLanguageField allows null values."""
      field = self.model_with_language._meta.get_field('language')
      self.assertTrue(field.null)

  def test_language_field_blank(self):
      """Test that the VideoLanguageField does not allow blank values."""
      field = self.model_with_language._meta.get_field('language')
      self.assertFalse(field.blank)

  def test_save_language_field(self):
      """Test saving a model with a VideoLanguageField."""
      self.model_with_language.save()
      saved_model = Videos.objects.get(id=self.model_with_language.id)
      self.assertEqual(saved_model.language, "English")

  def test_deconstruct(self):
        """Test the deconstruct method of the VideoLanguageField."""
        # Create an instance of the field
        field = VideoLanguageField()
        name, path, args, kwargs = field.deconstruct()

        # # Print out the deconstruct output for debugging
        # print(f'Name: {name}, Path: {path}, Args: {args}, Kwargs: {kwargs}')

        self.assertIsNone(name)
        self.assertEqual(path, 'media_files.fields.VideoLanguageField')  # Adjust path if needed
        self.assertEqual(args, ())
        self.assertEqual(kwargs, {'null': True, 'blank': False})