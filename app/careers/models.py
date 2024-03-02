from django.db import models

from app.core.models import BaseModel


class Career(BaseModel):
    username = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    content = models.TextField()
    is_private = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Career'
        verbose_name_plural = 'Careers'