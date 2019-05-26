from django.db import models


class Extension(models.Model):
    visit = models.ForeignKey("Visit", on_delete=models.CASCADE)
    old_assigned_end_date = models.DateTimeField()

    def __str__(self):
        return self.old_assigned_end_date
