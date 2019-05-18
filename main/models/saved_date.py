from django.db import models

class Saved_Date(models.Model):
    saved = models.NullBooleanField()
    last_modified = models.DateTimeField()