from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from PIL import Image
from ..models import Thumbnails, Videos

class ViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create some Thumbnail and Video objects for testing
        cls.image_file = cls.create_image_file()
        cls.video1 = Videos.objects.create(title='Video 1', video='http://example.com/video1')
        cls.video2 = Videos.objects.create(title='Video 2', video='http://example.com/video2')
        cls.thumbnail1 = Thumbnails.objects.create(
            title='Thumbnail 1',
            image=cls.image_file,
            date_uploaded=timezone.now()
        )
        cls.thumbnail2 = Thumbnails.objects.create(
            title='Thumbnail 2',
            image=cls.image_file,
            date_uploaded=timezone.now()
        )

    def test_pricing_view(self):
        """Test the pricing view."""
        response = self.client.get(reverse('pricing'))

        # Check that the view returns a 200 status code
        self.assertEqual(response.status_code, 200)

        # Check that the correct template is used
        self.assertTemplateUsed(response, 'pricing.html')

        # Check context data
        context = response.context

        # Check counts
        num_thumbnails = Thumbnails.objects.count()
        num_videos = Videos.objects.count()

        self.assertEqual(context['num_videos'], num_videos)
        self.assertEqual(context['num_thumbnails'], num_thumbnails)

        # Calculate client counts
        # num_thumbnail_clients = Thumbnail.objects.exclude(client__isnull=True).exclude(client__exact='').values('client').distinct().count()
        num_video_clients = Videos.objects.exclude(client__isnull=True).exclude(client__exact='').values('client').distinct().count()
        num_clients = num_video_clients # + num_thumbnail_clients

        self.assertEqual(context['num_clients'], num_clients)

    def test_tos_view(self):
        """Test the Terms of Service view."""
        response = self.client.get(reverse('tos'))

        # Check that the view returns a 200 status code
        self.assertEqual(response.status_code, 200)

        # Check that the correct template is used
        self.assertTemplateUsed(response, 'tos.html')

    def test_index_view(self):
        """Test the index view."""
        response = self.client.get(reverse('index'))

        # Check that the view returns a 200 status code
        self.assertEqual(response.status_code, 200)

        # Check that the correct template is used
        self.assertTemplateUsed(response, 'index.html')

    @staticmethod
    def create_image_file():
        """Create a dummy image file for testing."""
        image = Image.new('RGB', (100, 100), color='red')
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)
        return SimpleUploadedFile("test_image.jpg", img_byte_arr.read(), content_type="image/jpeg")