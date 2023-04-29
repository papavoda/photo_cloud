from django.contrib import admin
from django.utils.safestring import mark_safe
# from . import models
from .models import *
from mptt.admin import MPTTModelAdmin

admin.site.register(
    Category,
    MPTTModelAdmin,
    list_display=(
        'pk',
        'slug',
        'name',
        'parent',

        # ...more fields if you feel like it...
    ),
    list_editable=['slug'],
    list_display_links=(
        'name',
    ),
    prepopulated_fields={'slug': ('name',)}  # new
)

admin.site.register(Tag)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("name", "image", 'get_image')

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="110" height="80"')

    get_image.short_description = "Миниатюра"


class ImageInline(admin.StackedInline):
    model = Image
    max_num = 20
    extra = 0
    list_display = ("name", "image", 'get_image')
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="110" height="80"')


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("name", "video")


class VideoInline(admin.StackedInline):
    model = Video
    max_num = 4
    extra = 0
    list_display = ("name", "video",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['created', 'title', 'slug', 'get_image', 'author', 'status']
    list_editable = ['status',]
    readonly_fields = ("get_image",)
    inlines = [ImageInline, VideoInline, ]

    # prepopulated_fields = {'slug': ('title',)}  # new

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.main_image.url} width="110" height="80"')