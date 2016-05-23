from django.db import models
from django.utils import timezone

class Profile(models.Model):
    user = models.ForeignKey('auth.User')
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    birthday = models.DateTimeField(
        blank=True,null=True)
    photo = models.ImageField(null=True, blank=True)

    def __str__(self):
        return "{} {}".format(self.name ,self.surname)


#from ckeditor_uploader.fields import RichTextUploadingField
class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    class Meta:
            ordering = ('-created_date',)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Like(models.Model):
    user = models.ForeignKey('auth.User')
    post =  models.ForeignKey('Post')


class Comment(models.Model):
    author = models.ForeignKey('auth.User')
    post = models.ForeignKey('Post', related_name="comments")
    text = models.TextField()
