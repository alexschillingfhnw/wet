from django.db import models
from django.db.models import Q

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/images/')
    url = models.URLField(blank=True)

    @classmethod
    def search(cls, query):
        return cls.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
