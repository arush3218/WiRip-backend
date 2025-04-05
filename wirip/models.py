from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.text import slugify
from django.utils import timezone
# Create your models here.

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_img", blank=True, null=True)
    # profile_picture_url = models.URLField(blank=True, null=True)
    job_title = models.CharField(max_length=50, blank=True, null=True)

    facebook = models.URLField(max_length=255, blank=True, null=True)
    youtube = models.URLField(max_length=255, blank=True, null=True)
    instagram = models.URLField(max_length=255, blank=True, null=True)
    twitter = models.URLField(max_length=255, blank=True, null=True)
    linkedin = models.URLField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return self.username

class Blog(models.Model):
    
    CATEGORY = (
        ("Artist Spotlights", "Artist Spotlights"),
        ("Album Reviews", "Album Reviews"),
        ("Hip-Hop News", "Hip-Hop News"),
        ("Mixtape Madness", "Mixtape Madness"),
        ("Lyric Breakdowns", "Lyric Breakdowns"),
        ("Throwback Thursdays", "Throwback Thursdays"),
        ("Bars of the Week", "Bars of the Week"),
        ("Video Drops", "Video Drops"),
        ("Hip-Hop Culture", "Hip-Hop Culture"),
        ("Behind the Beat", "Behind the Beat"),
        ("Podcasts & Interviews", "Podcasts & Interviews"),
        ("Rap Battles & Cyphers", "Rap Battles & Cyphers"),
        ("Rising Stars", "Rising Stars"),
        )

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='blogs',null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_time = models.DateTimeField(blank=True, null=True)  # Changed from published_date
    is_draft = models.BooleanField(default=True)
    category = models.CharField(max_length=50,choices= CATEGORY ,blank=True, null=True)
    featured_image = models.ImageField(upload_to="blog_img", blank=True, null=True)
    
    class Meta:
        ordering = ['-published_time']  # Changed from published_date
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        base_slug = slugify(self.title)
        slug = base_slug
        num=1
        while Blog.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{num}"
            num += 1
        self.slug = slug
        
        if not self.is_draft and self.published_time is None:  # Changed from published_date
            self.published_time = timezone.now()
            
        super().save(*args, **kwargs)