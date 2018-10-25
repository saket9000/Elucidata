from django.db import models

# Create your models here.
class File(models.Model):
	media = models.FileField(upload_to='files', null=True)
