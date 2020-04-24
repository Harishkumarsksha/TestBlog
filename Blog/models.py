from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager


class CustomManeger(models.Manager):

    def get_query(self):
        return super.get_query.filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (('draft', 'Draft'), ('published', 'Published'))
    title = models.CharField(max_length=264)
    slug = models.SlugField(max_length=264, unique_for_date='publish')
    author = models.CharField(max_length=264)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=264, choices=STATUS_CHOICES, default='draft')
    objects = CustomManeger()
    tags = TaggableManager()

    # to get all taggs post.tags.all()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.publish.year,
                                            self.publish.strftime('%m'), self.publish.strftime('%d'), self.slug])

    # by using the reverse method we will get canonical urls


class Comment(models.Model):
    post = models.ForeignKey(
        Post, related_name='comment', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Commented by {} on {}'.format(self.name, self.created)
