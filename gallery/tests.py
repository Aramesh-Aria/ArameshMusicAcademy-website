from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .models import GalleryImage, GalleryPage, Video


class VideoModelTests(TestCase):
    def setUp(self):
        self.page = GalleryPage.objects.create(title='Concerts', slug='concerts')

    def test_youtube_watch_url_builds_embed_url(self):
        video = Video.objects.create(
            gallery_page=self.page, title='Concert', platform=Video.YOUTUBE,
            video_url='https://www.youtube.com/watch?v=abc123XYZ_0',
        )
        self.assertEqual(video.embed_url, 'https://www.youtube.com/embed/abc123XYZ_0')

    def test_youtube_short_url_builds_embed_url(self):
        video = Video(
            gallery_page=self.page, title='Concert', platform=Video.YOUTUBE,
            video_url='https://youtu.be/abc123XYZ_0',
        )
        self.assertEqual(video.embed_url, 'https://www.youtube.com/embed/abc123XYZ_0')

    def test_aparat_url_builds_embed_url(self):
        video = Video(
            gallery_page=self.page, title='Concert', platform=Video.APARAT,
            video_url='https://www.aparat.com/v/AbCdE',
        )
        self.assertEqual(
            video.embed_url,
            'https://www.aparat.com/video/video/embed/videohash/AbCdE/vt/frame',
        )

    def test_invalid_youtube_url_fails_validation(self):
        video = Video(
            gallery_page=self.page, title='Concert', platform=Video.YOUTUBE,
            video_url='https://example.com/not-a-video',
        )
        with self.assertRaises(ValidationError):
            video.full_clean()


class GalleryPageModelTests(TestCase):
    def test_unsaved_root_gallery_page_can_be_cleaned(self):
        page = GalleryPage(title='Concerts', slug='concerts')

        page.full_clean()

    def test_slug_path_builds_nested_gallery_url_path(self):
        root = GalleryPage.objects.create(title='Concerts', slug='concerts')
        child = GalleryPage.objects.create(title='Year 1403', slug='year-1403', parent=root)

        self.assertEqual(child.slug_path, 'concerts/year-1403')
        self.assertEqual(child.get_absolute_url(), '/gallery/concerts/year-1403/')

    def test_gallery_page_cannot_be_its_own_parent(self):
        page = GalleryPage.objects.create(title='Concerts', slug='concerts')
        page.parent = page

        with self.assertRaises(ValidationError):
            page.full_clean()

    def test_root_gallery_slug_must_be_unique(self):
        GalleryPage.objects.create(title='Concerts', slug='lr')
        duplicate_page = GalleryPage(title='Another Concerts', slug='lr')

        with self.assertRaises(ValidationError):
            duplicate_page.full_clean()

    def test_nested_gallery_slug_must_be_unique_with_same_parent(self):
        root = GalleryPage.objects.create(title='Concerts', slug='concerts')
        GalleryPage.objects.create(title='Year 1403', slug='lr', parent=root)
        duplicate_page = GalleryPage(title='Year 1404', slug='lr', parent=root)

        with self.assertRaises(ValidationError):
            duplicate_page.full_clean()

    def test_slug_is_generated_from_title_when_blank(self):
        page = GalleryPage.objects.create(title='کنسرت سال ۱۴۰۵', slug='')

        self.assertTrue(page.slug)


class GalleryViewTests(TestCase):
    def test_gallery_root_lists_active_top_level_pages(self):
        active_page = GalleryPage.objects.create(title='Concerts', slug='concerts')
        GalleryPage.objects.create(title='Hidden', slug='hidden', is_active=False)

        response = self.client.get(reverse('gallery:gallery_root'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, active_page.title)
        self.assertNotContains(response, 'Hidden')

    def test_gallery_detail_supports_nested_paths(self):
        root = GalleryPage.objects.create(title='Concerts', slug='concerts')
        child = GalleryPage.objects.create(title='Year 1403', slug='year-1403', parent=root)
        image = GalleryImage.objects.create(
            gallery_page=child,
            title='Student Performance',
            image='gallery/performance.jpg',
        )

        response = self.client.get('/gallery/concerts/year-1403/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['current_page'], child)
        self.assertEqual(response.context['breadcrumbs'], [root, child])
        self.assertContains(response, image.title)

    def test_inactive_nested_gallery_page_returns_404(self):
        root = GalleryPage.objects.create(title='Concerts', slug='concerts')
        GalleryPage.objects.create(
            title='Hidden',
            slug='hidden',
            parent=root,
            is_active=False,
        )

        response = self.client.get('/gallery/concerts/hidden/')

        self.assertEqual(response.status_code, 404)

# Create your tests here.
