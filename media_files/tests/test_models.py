from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.utils import timezone
from ..models import Thumbnails, Videos

# THUMBNAIL MODEL CLASS
class ThumbnailModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.game_instance = 'Test Game'
        cls.language_instance = 'English'
        # Capture the current date before creating the thumbnail
        cls.current_date = timezone.now().date()

    def image_file(self):
        image = Image.new('RGB', (100, 100), color='red')
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG')  # Save image to byte array
        img_byte_arr.seek(0)  # Rewind the byte array

        return SimpleUploadedFile("test_image.jpg", img_byte_arr.read(), content_type="image/jpeg")

    def setUp(self):
        # Create a Thumbnail instance for testing __str__
        self.thumbnail = Thumbnails.objects.create(
            title='Test Thumbnail',
            image=self.image_file(),
            language=self.language_instance,
            game=self.game_instance,
            date_uploaded=self.current_date
        )

    # THUMBNAIL MODEL TITLE TESTS
    def test_title_field(self):

        # Test that title cannot be null
        thumbnail = Thumbnails(title=None, image=self.image_file())
        with self.assertRaises(Exception):
            thumbnail.full_clean()  # should raise validation error

        # Test maximum length constraint
        long_title = 'a' * 101
        thumbnail = Thumbnails(title=long_title, image=self.image_file())

        # Validate and check if a ValidationError is raised
        with self.assertRaises(ValidationError):
            thumbnail.full_clean()  # This will trigger validation
            thumbnail.save()

    def test_thumbnail_title_field_required(self):
        """Test that the 'title' field is required."""
        # Attempt to create a Thumbnail with a None title
        thumbnail = Thumbnails(
            game=self.game_instance,
            image=self.image_file(),
            language=self.language_instance,
            title=None, # Set title to blank
            date_uploaded=self.current_date  # Set the date_uploaded to now
        )

        with self.assertRaises(ValidationError):
            thumbnail.full_clean()  # This should raise a ValidationError

    def test_valid_thumbnail_title_creation(self):
        """Test that a Thumbnail with a valid title can be created."""
        thumbnail = Thumbnails.objects.create(
            game=self.game_instance,
            image=self.image_file(),
            title='Valid Title',
            language=self.language_instance,
            date_uploaded=self.current_date
        )

        self.assertEqual(thumbnail.title, 'Valid Title')

    # Verify that the truncated title string representation of the video is correct
    def test_str_with_long_title(self):
        # Create a thumbnail instance
        thumbnail = Thumbnails.objects.create(
            title = 'A very long title that should be truncated',
            language=self.language_instance,
            game=self.game_instance,
            image=self.image_file(),
            date_uploaded=self.current_date
        )

        self.assertEqual(str(thumbnail), 'A very long title th...')

    # Verify that the short title string representation of the video is correct
    def test_str_with_short_title(self):
        # Create a thumbnail instance
        thumbnail = Thumbnails.objects.create(
            title = 'A short title',
            language=self.language_instance,
            game=self.game_instance,
            image=self.image_file(),
            date_uploaded=self.current_date
        )

        self.assertEqual(str(thumbnail), 'No Title or Game needed to be truncated')

    # Verify that the no title string representation of the video is correct
    def test_str_with_no_title(self):
        # Part 1: Test that ValidationError is raised
        with self.assertRaises(ValidationError):
            Thumbnails.objects.create(
                title=None,
                language=self.language_instance,
                game=self.game_instance,
                image=self.image_file(),
                date_uploaded=self.current_date
            )

        # Part 2: Test the __str__ method under normal conditions
        # Pass a valid title to avoid ValidationError
        thumbnail = Thumbnails.objects.create(
            title="Valid Title",
            language=self.language_instance,
            game=self.game_instance,
            image=self.image_file(),
            date_uploaded=self.current_date
        )
        self.assertEqual(str(thumbnail), 'No Title or Game needed to be truncated')

    def test_str_with_non_string_title(self):
        """Test the __str__ method when the title is not a string."""
        non_string_values = [123, 45.67, True, [], {}]

        for value in non_string_values:
            thumbnail = Thumbnails(
                title=value,
                language=self.language_instance,
                game=self.game_instance,
                image=self.image_file(),
                date_uploaded=self.current_date
            )

            with self.assertRaises(ValidationError):
                thumbnail.save()  # ValidationError should be raised here

    # Verify that the truncated game string representation of the video is correct
    def test_str_with_long_game(self):
        # Create a thumbnail instance
        self.thumbnail_with_truncated_game = Thumbnails.objects.create(
            title = 'Short Title',
            language=self.language_instance,
            game='A very long game name that should be truncated',
            image=self.image_file(),
            date_uploaded=self.current_date
        )

        self.assertEqual(str(self.thumbnail_with_truncated_game), 'A very long game nam...')

    # Verify that the short game string representation of the video is correct
    def test_str_with_short_game(self):
        # Create a thumbnail instance
        self.thumbnail = Thumbnails.objects.create(
            title = 'Short Title',
            language=self.language_instance,
            game='Short game title',
            image=self.image_file(),
            date_uploaded=self.current_date
        )

        self.assertEqual(str(self.thumbnail), 'No Title or Game needed to be truncated')

    # THUMBNAIL MODEL IMAGE TESTS
    def test_image_field(self):
        # Test that image field cannot be blank
        thumbnail = Thumbnails(title='Valid Title', image=None)
        with self.assertRaises(Exception):
            thumbnail.full_clean()  # should raise validation error

        # Test image validator
        invalid_image = SimpleUploadedFile('test.txt', b'test', content_type='text/plain')
        thumbnail = Thumbnails(title='Valid Title', image=invalid_image)
        with self.assertRaises(Exception):
            thumbnail.full_clean()  # should raise validation error

    def test_thumbnail_image_file_type(self):
        # Create and save a Thumbnail instance with a valid image
        thumbnail = Thumbnails.objects.create(
            title='Valid Title',
            image=self.image_file()
        )

        # Fetch the thumbnail instance from the database
        thumbnail = Thumbnails.objects.get(id=thumbnail.id)

        # Open the image file using Django's default storage
        try:
            with default_storage.open(thumbnail.image.name, 'rb') as img_file:
                img_content = img_file.read()  # Read the content to debug
                if not img_content:
                    self.fail(f'Image content is empty. File path: {thumbnail.image.name}')
                with io.BytesIO(img_content) as img_byte_stream:
                    img = Image.open(img_byte_stream)
                    img.verify()  # Verify that the file is an image
                    self.assertIn(img.format.lower(), ['jpeg', 'png', 'gif'])  # Check for expected formats
        except (IOError, SyntaxError) as e:
            self.fail(f'Uploaded file is not a valid image. Error: {e}. File Content: {img_content[:100]}')  # Print a portion of the content for debugging

    # THUMBNAIL MODEL DATE UPLOADED TESTS
    def test_date_uploaded_default(self):
        thumbnail = Thumbnails(title='Valid Title', image=self.image_file())
        thumbnail.save()

        saved_thumbnail = Thumbnails.objects.get(id=thumbnail.id)

        # Use timezone.now().date() for current date
        now = timezone.now().date()

        # Assertion: Check if the date_uploaded is close to now
        self.assertEqual(saved_thumbnail.date_uploaded, now)

    def test_thumbnail_date_uploaded_explicit(self):
        """Test that the 'date_uploaded' field can be explicitly set."""
        explicit_date = timezone.datetime(2023, 1, 1).date()

        # Create a Thumbnail instance with an explicit date_uploaded
        thumbnail = Thumbnails(
            title='Thumbnail with Explicit Date Uploaded',
            image=self.image_file(),
            game=self.game_instance,
            language=self.language_instance,
            date_uploaded=explicit_date
        )

        # Validate the thumbnail instance
        try:
            thumbnail.full_clean()  # This should not raise a ValidationError
            thumbnail.save()
        except ValidationError as e:
            self.fail(f'ValidationError raised: {e}')

        # Fetch it from the database and assert date_uploaded is the explicit date
        saved_thumbnail = Thumbnails.objects.get(id=thumbnail.id)
        self.assertEqual(saved_thumbnail.date_uploaded, explicit_date)

    def test_create_thumbnail_with_all_valid_fields(self):
        """Test creating a Thumbnail instance with all valid fields."""
        thumbnail = Thumbnails.objects.create(
            title='Valid Title',
            language=self.language_instance,
            game=self.game_instance,
            image=self.image_file(),
            date_uploaded=self.current_date,
        )

        # Fetch the thumbnail instance from the database
        fetched_thumbnail = Thumbnails.objects.get(id=thumbnail.id)

        # Check if the fetched instance matches the created one
        self.assertEqual(fetched_thumbnail.title, 'Valid Title')
        self.assertEqual(fetched_thumbnail.language, self.language_instance)
        self.assertEqual(fetched_thumbnail.game, self.game_instance)
        self.assertTrue(fetched_thumbnail.image)
        self.assertEqual(fetched_thumbnail.date_uploaded, self.current_date.date())

    # THUMBNAIL MODEL CREATE MODEL TESTING
    def test_create_thumbnail_with_all_valid_fields(self):
        """Test creating a Thumbnail instance with all valid fields."""
        thumbnail = Thumbnails.objects.create(
            title='Valid Title',
            language=self.language_instance,
            game=self.game_instance,
            image=self.image_file(),
            date_uploaded=self.current_date,
        )

        # Fetch the thumbnail instance from the database
        fetched_thumbnail = Thumbnails.objects.get(id=thumbnail.id)

        # Check if the fetched instance matches the created one
        self.assertEqual(fetched_thumbnail.title, 'Valid Title')
        self.assertEqual(fetched_thumbnail.language, self.language_instance)
        self.assertEqual(fetched_thumbnail.game, self.game_instance)
        self.assertTrue(fetched_thumbnail.image)
        self.assertEqual(fetched_thumbnail.date_uploaded, self.current_date)

    def test_save_and_retrieve_thumbnail(self):
        """Test saving a Thumbnail instance and check if it persists in the database."""
        thumbnail = Thumbnails(
            title='Another Valid Title',
            language=self.language_instance,
            game=self.game_instance,
            image=self.image_file(),
            date_uploaded=self.current_date,
        )
        thumbnail.save()

        # Fetch the saved instance from the database
        saved_thumbnail = Thumbnails.objects.get(id=thumbnail.id)

        # Verify that the saved data matches the created data
        self.assertEqual(saved_thumbnail.title, 'Another Valid Title')
        self.assertEqual(saved_thumbnail.language, self.language_instance)
        self.assertEqual(saved_thumbnail.game, self.game_instance)
        self.assertTrue(saved_thumbnail.image)
        self.assertEqual(saved_thumbnail.date_uploaded, self.current_date)

# VIDEO MODEL CLASS
class VideoModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.client_instance = 'Test Client'
        cls.game_instance = 'Test Game'
        cls.language_instance = 'English'
        cls.long_title = 'A' * 201  # Title length exceeds the maximum allowed length
        cls.current_date = timezone.now().date()  # Set the current date as a class attribute

        # Create a video with a valid video URL
        cls.video_with_valid_url = Videos.objects.create(
            title='Video with valid url',
            video='http://example.com/video',
            game=cls.game_instance,
            client=cls.client_instance,
            views=100,
            likes=50,
            language=cls.language_instance,
            date_uploaded=cls.current_date  # Set the date_uploaded to now
        )

        # Create a video without a valid video URL
        cls.video_without_valid_url = Videos.objects.create(
            title='Video without valid url',
            video=None,
            game=cls.game_instance,
            client=cls.client_instance,
            views=100,
            likes=50,
            language=cls.language_instance,
            date_uploaded=cls.current_date  # Set the date_uploaded to now
        )

        # Create a Video instance for testing __str__
        cls.video = Videos.objects.create(
            title='Test Video',
            video='http://example.com/video',
            game=cls.game_instance,
            client=cls.client_instance,
            views=10,
            likes=5,
            language=cls.language_instance,
            date_uploaded=cls.current_date
        )

    # VIDEO MODEL TITLE TESTS
    def test_video_title_max_length(self):
        # Test to ensure that the title length is properly enforced
        video = Videos(
            title='A valid title',
            video='https://site.com',
            language='English',
            game='Some game',
        )
        try:
            video.full_clean()  # This will validate the instance
        except ValidationError as e:
            self.fail(f'ValidationError raised: {e}')

    def test_video_title_max_length_exceed(self):
        # Test to ensure that an error is raised if title exceeds max length
        video = Videos(
            title=self.long_title,
        )
        with self.assertRaises(ValidationError):
            video.full_clean()  # This should raise a ValidationError due to the title length

    def test_video_title_field_required(self):
        """Test that the 'title' field is required."""
        # Attempt to create a Video with a None title
        video = Videos(
            client=self.client_instance,
            game=self.game_instance,
            title='', # Set title to blank
            video='http://example.com/video',
            views=0,
            likes=0,
            language=self.language_instance,
            date_uploaded=self.current_date  # Set the date_uploaded to now
        )
        try:
            video.full_clean()
            self.fail('ValidationError not raised for missing title.')
        except ValidationError as e:
            self.assertIn('title', e.message_dict)

    def test_valid_video_title_creation(self):
        """Test that a Video instance with a valid title can be created successfully."""
        # Create a Video instance with a valid title
        video = Videos(
            title='Valid title',
            video='https://site.com',
            language='English',
            game='Some game',
        )

        try:
            video.full_clean()  # Validate the instance
        except ValidationError as e:
            self.fail(f'ValidationError raised: {e}')

        # Save the instance and check if it is stored correctly
        video.save()
        saved_video = Videos.objects.get(id=video.id)

        # Assert that the title matches the expected valid title
        self.assertEqual(saved_video.title, 'Valid title')

    # VIDEO MODEL CLIENT TESTS
    def test_model_client_field(self):
        instance = Videos.objects.create(client='value')
        self.assertEqual(instance.client, 'value')

    # VIDEO MODEL GAME TESTS
    def test_model_game_field(self):
        instance = Videos.objects.create(game='value')
        self.assertEqual(instance.game, 'value')

    # VIDEO MODEL VIEWS AND LIKES TESTS
    # this tests the default of both views AND likes!
    def test_views_and_likes_defaults(self):
        """Test that views and likes are set to 0 if None is provided."""
        video = Videos.objects.create(title="Test Video", views=None, likes=None)
        self.assertEqual(video.views, 0)
        self.assertEqual(video.likes, 0)

    # this tests the values of both views AND likes!
    def test_views_and_likes_with_values(self):
        """Test that views and likes retain their provided values."""
        video = Videos.objects.create(title="Test Video", views=5, likes=10)
        self.assertEqual(video.views, 5)
        self.assertEqual(video.likes, 10)

    # VIDEO MODEL DATE UPLOADED TESTS
    def test_video_date_uploaded_default(self):
        """Test that the 'date_uploaded' field has the correct default value."""

        # Create a Video instance without specifying date_uploaded
        video = Videos(
            title='Video with Default Date Uploaded',
            video='http://example.com/video',
            game=self.game_instance,
            client=self.client_instance,
            views=100,
            likes=50,
            language=self.language_instance,
        )

        # Validate the video instance
        try:
            video.full_clean()  # This should not raise a ValidationError
            video.save()
        except ValidationError as e:
            self.fail(f'ValidationError raised: {e}')

        # Fetch it from the database and assert date_uploaded is close to now
        saved_video = Videos.objects.get(id=video.id)

        # Ensure that the default date is set correctly
        now = timezone.now().date()
        default_date_uploaded = saved_video.date_uploaded

        # Compare dates directly (only dates, no time needed)
        self.assertEqual(default_date_uploaded, now)

    def test_video_date_uploaded_explicit(self):
        """Test that the 'date_uploaded' field can be explicitly set."""
        explicit_date = timezone.datetime(2023, 1, 1).date()

        # Create a Video instance with an explicit date_uploaded
        video = Videos(
            title='Thumbnail with Explicit Date Uploaded',
            video='http://example.com/video',
            game=self.game_instance,
            client=self.client_instance,
            views=100,
            likes=50,
            language=self.language_instance,
            date_uploaded=explicit_date
        )

        # Validate the thumbnail instance
        try:
            video.full_clean()  # This should not raise a ValidationError
            video.save()
        except ValidationError as e:
            self.fail(f'ValidationError raised: {e}')

        # Fetch it from the database and assert date_uploaded is the explicit date
        saved_video = Videos.objects.get(id=video.id)
        self.assertEqual(saved_video.date_uploaded, explicit_date)

    def test_video_str_method(self):
        """Test the __str__ method of the Video model."""
        video = self.video.title
        self.assertEqual(str(video), 'Test Video')