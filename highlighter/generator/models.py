from django.db import models

# Create your models here.
class HighlightImage(models.Model):
    created = models.DataTimeField(auto_now_add=True)
    youtube_link = models.CharField(max_length=100)
    start_time = models.int() # in seconds
    end_time = models.IntegerField()
    image_file = models.CharField(max_length=100)
    failed_to_create = models.BooleanField(default=False)

    class Meta:
        ordering = ['created']