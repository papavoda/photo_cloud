# from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth import get_user_model
from autoslug import AutoSlugField
from django.template.defaultfilters import slugify
from django.urls import reverse
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Category(MPTTModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, null=False, unique=True)
    parent = TreeForeignKey(
        'self',
        related_name="children",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        # '<slug:slug>/<slug:post_slug>'
        return reverse("category_detail", kwargs={'pk': self.pk})


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = AutoSlugField(populate_from='name', unique=True)

    def get_absolute_url(self):
        return reverse('tag_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name


def upload_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'articles/{instance.author}/{instance.slug}/{filename}'


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    keywords = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=500, default='')
    title = models.CharField(max_length=500)
    # slug = models.SlugField(max_length=64, null=True, blank=True)
    # TODO check autoslug
    slug = AutoSlugField(populate_from='title', unique=True)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    main_image = models.ImageField(verbose_name='Изображение', upload_to=upload_directory_path, blank=True, null=True)
    # image = models.ImageField(upload_to='articles/%Y/%m/%d/%pk', null=True, blank=True)
    # RichTextField -> for ckeditor
    text = RichTextField(max_length=8000)

    category = models.ForeignKey(Category, related_name="post",
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 )
    tags = models.ManyToManyField(Tag, verbose_name='Метки', related_name="post")
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')

    class Meta:
        ordering = ('-created',)

    app_name = __package__

    def get_absolute_url(self):
        return reverse("post_detail",
                       kwargs={'app_name': self.app_name, 'cat_slug': self.category.slug, 'slug': self.slug})

    def get_tags(self):
        return self.tags.all()

    def get_images(self):
        return self.images.all()

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.category} - {self.title}'


# for Image upload
def image_upload_directory(instance, filename):
    # file will be uploaded to MEDIA_ROOT/instance.post.author/instance.post.slug/<filename>
    return f'articles/{instance.post.author}/{instance.post.slug}/{filename}'


class Image(models.Model):
    name = models.CharField(max_length=50, default='')  # alt
    post = models.ForeignKey(Post, related_name='images', on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to=image_upload_directory)

    def __str__(self):
        return f'{self.name} - {self.image}'


class Video(models.Model):
    name = models.CharField(max_length=250, default='', blank=True, null=True)
    post = models.ForeignKey(Post, related_name='videos', on_delete=models.SET_NULL, null=True)
    video = models.FileField(upload_to=image_upload_directory)

    def __str__(self):
        if self.name:
            return f'{self.name} - {self.video}'
