from django.conf import settings
from django.test import TestCase
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.management import call_command


class TestDjangoPluginWhitenoise(TestCase):
    def test_simple_view_works(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Hello world")

    def test_toolbar_middleware_injected(self):
        self.assertEqual(
            settings.MIDDLEWARE[:2],
            [
                "django.middleware.security.SecurityMiddleware",
                "whitenoise.middleware.WhiteNoiseMiddleware",
            ],
        )

    def test_static_files_settings(self):
        self.assertIsNotNone(settings.STATIC_ROOT)
        self.assertIsNotNone(settings.STATIC_URL)
        self.assertEqual(
            "whitenoise.storage.CompressedManifestStaticFilesStorage",
            settings.STORAGES["staticfiles"]["BACKEND"],
        )
        self.assertEqual("whitenoise.runserver_nostatic", settings.INSTALLED_APPS[0])

    def test_serve_static_file(self):
        """Even this minimal test proves that WhiteNoise is working.

        Django's static file serving is disabled during tests (DEBUG=False), so if we can
        access the static file it must be WhiteNoise serving it.
        """
        call_command("collectstatic", interactive=False, verbosity=0)
        hashed_filename = staticfiles_storage.stored_name("test.txt")
        resp = self.client.get(f"{settings.STATIC_URL}{hashed_filename}")
        self.assertEqual(resp.status_code, 200)
