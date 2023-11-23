from django.test import TestCase
from django.urls import reverse, resolve
from .models import Project
from .forms import ContactForm
from .views import project_index
from django.core.files.uploadedfile import SimpleUploadedFile


# Model tests
class ProjectModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a project for testing
        Project.objects.create(title='Test Project', description='Description for test project', image='path/to/image.jpg', url='http://example.com')

    def test_project_creation(self):
        project = Project.objects.get(id=1)
        self.assertEqual(project.title, 'Test Project')
        self.assertEqual(project.description, 'Description for test project')

# View tests
class ProjectViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Project.objects.create(title='Test Project', description='Description for test project', image='path/to/image.jpg', url='http://example.com')

    def test_view_url_exists(self):
        response = self.client.get(reverse('project_index'))
        self.assertEqual(response.status_code, 200)

# Form tests
class ContactFormTest(TestCase):

    def test_valid_data(self):
        form = ContactForm({
            'name': 'John Doe',
            'email': 'john@example.com',
            'message': 'Hi there!'
        })
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        form = ContactForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)  # Assuming name, email, and message are required

# Search tests
class SearchTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a mock image
        cls.mock_image = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")

        # Use the mock image when creating projects
        Project.objects.create(title='Data Science Project', description='A project about data science', image=cls.mock_image)
        Project.objects.create(title='Web Development', description='A project about web development', image=cls.mock_image)

# Template tests
class ProjectIndexViewTest(TestCase):

    def test_template_used(self):
        response = self.client.get(reverse('project_index'))
        self.assertTemplateUsed(response, 'projects/project_index.html')

# URL tests
class UrlsTest(TestCase):

    def test_project_index_url(self):
        url = reverse('project_index')
        self.assertEqual(resolve(url).func, project_index)
