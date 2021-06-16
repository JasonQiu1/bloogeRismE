from django.db import models
from django.utils import timezone

from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class Post(models.Model):
    pub_date = models.DateTimeField('date published')
    hidden = models.BooleanField(default=False)
    title_text = models.CharField(max_length=300)
    slug = models.SlugField(allow_unicode=True, unique=True, primary_key=True)
    body = RichTextUploadingField()
    def __str__(self):
        return self.slug
    def isVisible():
        if pub_date < timezone.now():
            return True
        return False
