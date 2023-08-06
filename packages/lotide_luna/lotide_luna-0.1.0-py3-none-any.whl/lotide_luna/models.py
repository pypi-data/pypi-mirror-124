from django.db import models


class Community(models.Model):
    name = models.CharField(max_length=50, unique=True)
    local = models.BooleanField()
    host = models.CharField(max_length=50)
    remote_url = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    description_html = models.TextField(blank=True)
    description_text = models.TextField(blank=True)
    # feed is omitted

    def __str__(self):
        return self.name


class Post(models.Model):
    _id = models.IntegerField()
    title = models.CharField(max_length=100)
    remote_url = models.URLField()
    href = models.CharField(max_length=100, blank=True)
    content_text = models.TextField(blank=True)
    content_html = models.TextField(blank=True)
    author = models.ForeignKey('User', on_delete=models.PROTECT, null=True)
    created = models.DateTimeField()
    community = models.ForeignKey('Community', on_delete=models.CASCADE)
    score = models.IntegerField()
    sticky = models.BooleanField()
    content_markdown = models.TextField(blank=True)
    approved = models.BooleanField()
    local = models.BooleanField()


class User(models.Model):
    _id = models.IntegerField()
    username = models.CharField(max_length=50, unique=True)
    local = models.BooleanField()
    host = models.CharField(max_length=50)
    remote_url = models.CharField(max_length=100)
    is_bot = models.BooleanField()
    suspended = models.BooleanField()

    def __str__(self):
        return self.username
