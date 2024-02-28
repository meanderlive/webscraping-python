from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from django.template.defaultfilters import slugify


class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Listing(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    expiry_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=150, null=True, blank=True)
    slug = models.SlugField()

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='listings'
    )
    created_at = models.DateTimeField(default=timezone.now)

    flagged = models.BooleanField(default=False)
    flagged_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    flagged_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)

        return super(Listing, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('listing',
                       args=[self.slug])
    

class Heading(models.Model):
    TYPE_CHOICES = (
        ('h1', 'Heading 1'),
        ('h2', 'Heading 2'),
        ('h3', 'Heading 3'),
        ('h4', 'Heading 4'),
        ('h5', 'Heading 5'),
        ('h6', 'Heading 6'),
    )
    type = models.CharField(max_length=2, choices=TYPE_CHOICES)
    text = models.CharField(max_length=255)

class Paragraph(models.Model):
    text = models.TextField()