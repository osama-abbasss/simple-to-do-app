from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


class ToDo(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    title = models.CharField(max_length = 40)
    content = models.TextField()
    time = models.TimeField()
    date = models.DateField()
    status = models.BooleanField(default=False)
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        elif self.slug != slugify(self.title):
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)


    class Meta:
        unique_together = ('user', 'title')
        verbose_name = 'to do'
        verbose_name_plural = 'to do'
