from django.template.defaultfilters import slugify
from django.db import models
import uuid


class Movie(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    # optional fields for filtering
    director = models.CharField(max_length=255)
    writer = models.CharField(max_length=255)
    language = models.CharField(max_length=64)
    country = models.CharField(max_length=64)

    slug = models.SlugField(max_length=32, default='', blank=True)
    parent = models.ForeignKey('self', blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Movies'


class Comment(models.Model):
    author = models.CharField(max_length=64)
    content = models.TextField()
    movie = models.ForeignKey(Movie)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Author: %s, movie: %s" % (self.author, self.movie)

    class Meta:
        verbose_name_plural = 'Comments'
