from django.db import models

# Create your models here.

class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    content = models.TextField()
    image = models.ImageField(blank=True, null=False)

    def __str__(self):
        return self.title

class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False)
    image = models.ImageField(upload_to='images/', blank=True, null=False)

    def __str__(self):
        return self.post.title

