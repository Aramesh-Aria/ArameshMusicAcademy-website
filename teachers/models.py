from django.db import models
from django.urls import reverse


class Instrument(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Teacher(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    instruments = models.ManyToManyField(Instrument, related_name='teachers')
    date_of_birth = models.DateField()
    birth_province = models.CharField(max_length=100)
    birth_city = models.CharField(max_length=100)
    education = models.CharField(max_length=255)
    biography = models.TextField()
    profile_image = models.ImageField(upload_to='teachers/')
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'last_name', 'first_name']

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        return reverse('teachers:teacher_detail', kwargs={'pk': self.pk})
