from django.db import models
from django.db.models import Q
from django.utils import timezone

class Project(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/images/', blank=False, null=False)
    url = models.URLField(blank=True)
    date = models.DateTimeField(default=timezone.now)

    @classmethod
    def search(cls, query):
        return cls.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    
    # search that leads to a different page, the search should be on the django part, use a different controller for the search and send the projects back to the view
