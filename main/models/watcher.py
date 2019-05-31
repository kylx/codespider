from django.db import models

class WatcherManager(models.Manager):
    def get_relationship_list(self):
        return [[rel.pk, rel.relationship] for rel in super().get_queryset()]
        
    def get_filtered_relationships(self, term):
        return [
            {'pk': rel.pk, 'relationship': rel.relationship}
            for rel in super().get_queryset().filter(relationship__icontains=term)
        ]

class Watcher(models.Model):
    objects = WatcherManager()
    relationship = models.CharField(max_length=15)
    def __str__(self):
        return self.relationship
