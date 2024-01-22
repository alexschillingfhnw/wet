from django.test import TestCase
from django.urls import reverse, resolve
from .models import Project
from .forms import ContactForm
from .views import project_index
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError


class ProjectModelTest(TestCase):
    """
    This test ensures that a Project object can be created with the specified title and description. 
    It verifies that the object's attributes match what was provided upon creation.
    """

    @classmethod
    def setUpTestData(cls):
        # Create a project for testing
        Project.objects.create(title='Test Project', description='Description for test project', image='path/to/image.jpg', url='http://example.com')

    def test_project_creation(self):
        project = Project.objects.get(id=1)
        self.assertEqual(project.title, 'Test Project')
        self.assertEqual(project.description, 'Description for test project')


class ProjectViewsTest(TestCase):
    """
    This test checks if the URL for the project_index view exists and is accessible. 
    It confirms that a request to this URL returns an HTTP 200 OK status, indicating the view functions correctly.
    """

    @classmethod
    def setUpTestData(cls):
        Project.objects.create(title='Test Project', description='Description for test project', image='path/to/image.jpg', url='http://example.com')

    def test_view_url_exists(self):
        response = self.client.get(reverse('project_index'))
        self.assertEqual(response.status_code, 200)


class ContactFormTest(TestCase):

    def test_valid_data(self):
        """
        Tests the ContactForm with valid data to ensure it is considered valid by Django. 
        It ensures the form fields are correctly processed and validated.
        """
        form = ContactForm({
            'name': 'John Doe',
            'email': 'john@example.com',
            'message': 'Hi there!'
        })
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        """
        Validates that the ContactForm behaves as expected when given incomplete or incorrect data. 
        It checks if the form correctly identifies errors and provides the appropriate error messages.
        """
        form = ContactForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)


class SearchTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a mock image
        cls.mock_image = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")

        # Use the mock image when creating projects
        Project.objects.create(title='Data Science Project', description='A project about data science', image=cls.mock_image)
        Project.objects.create(title='Web Development', description='A project about web development', image=cls.mock_image)

    #def test_search_by_title(self):
    #    # Search for a project by its title
    #    projects = Project.search('data')
    #    self.assertEqual(len(projects), 1)


class ProjectIndexViewTest(TestCase):
    """
    This test confirms that the correct template is used when the project_index view is rendered. 
    It ensures that the view is correctly tied to the intended template file.
    """

    def test_template_used(self):
        response = self.client.get(reverse('project_index'))
        self.assertTemplateUsed(response, 'projects/project_index.html')


class UrlsTest(TestCase):
    """
    Tests the resolution of the project_index URL, ensuring it correctly resolves to the project_index view function. 
    This verifies the URL configuration is correctly linked to the view.
    """

    def test_project_index_url(self):
        url = reverse('project_index')
        self.assertEqual(resolve(url).func, project_index)


class ContactFormNegativeTest(TestCase):
    """
    Checks how the ContactForm responds to an invalid email input, ensuring it is not valid and that the form errors include an error for the email field. 
    This is crucial for validating user input and maintaining data integrity.
    """

    def test_bad_email(self):
        form_data = {
            'name': 'John Doe',
            'email': 'bademail',  # intentionally badly formatted email
            'message': 'Hello'
        }
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)


class ProjectModelNegativeTest(TestCase):
    
    def test_create_project_without_title(self):
        project = Project(description='Some description', image='myportfolio/media/projects/images/movie.png')
        try:
            project.full_clean()
            print("Test should not reach this point.")
        except ValidationError as e:
            print("Expected validation error caught:", e)
    
    def test_create_project_without_image(self):
        project = Project(title='Project Title', description='Some description')
        try:
            project.full_clean()
            print("Test should not reach this point.")
        except ValidationError as e:
            print("Expected validation error caught:", e)