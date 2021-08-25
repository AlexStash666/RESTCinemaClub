from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Genre, Movie, MovieShots, Actor, RatingStar, Rating, Review

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MovieAdminForm(forms.ModelForm):
    """форма с виджетом ckeditor"""
    description = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())

    class Meta:
        model: Movie
        fields: '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категория"""
    list_display = ("id", "name", "url")
    list_display_links = ("name",)


class ReviewInLine(admin.TabularInline):
    """Отзывы на странице с фильмом"""
    model = Review
    extra = 1
    readonly_fields = ('name', 'email')


class MovieShotsInLine(admin.TabularInline):
    model = MovieShots
    extra = 1

    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src= {obj.image.url} width="110px" height="130px"')

    get_image.short_description = "Изображение"


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """Фильмы"""
    list_display = ("title", "category", "url", "draft")
    list_filter = ('category', 'year')
    search_fields = ('title', 'category__name')
    inlines = [MovieShotsInLine, ReviewInLine]
    save_on_top = True
    save_as = True
    readonly_fields = ('get_poster',)
    list_editable = ('draft',)
    actions = ['publish', 'unpublish']
    form = MovieAdminForm
    fieldsets = (
        (None, {
            'fields': (('title', 'tagline'),)
        }),
        (None, {
            'fields': ('description', ('poster', 'get_poster'))
        }),
        (None, {
            'fields': (('year', 'world_premiere'), 'country')
        }),
        ('Actors', {
            'classes': ('collapse',),
            'fields': (('actors', 'directors', 'genres', 'category'),)
        }),
        (None, {
            'fields': (('budget', 'fees_in_usa', 'fees_in_world'),)
        }),
        ('Options', {
            'fields': (('url', 'draft'),)
        }),
    )

    def get_poster(self, obj):
        return mark_safe(f'<img src= {obj.poster.url} width="50px" height="60"')

    def unpublish(self, request, queryset):
        """Снять с публикации"""
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = '1 запись была обновлена'
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")

    def publish(self, request, queryset):
        """Публикация"""
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = '1 запись была опубликована'
        else:
            message_bit = f"{row_update} записей были опубликованы"
        self.message_user(request, f"{message_bit}")

    unpublish.short_description = 'Снять с публикации'
    unpublish.allowed_permissions = ('change',)

    publish.short_description = 'Опубликовать'
    publish.allowed_permissions = ('change',)

    get_poster.short_description = 'Постер'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Отзывы"""
    list_display = ('name', 'email', 'parent', 'movie', 'id')
    readonly_fields = ('name', 'email')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Жанры"""
    list_display = ('name', 'url')


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    """Кадры из фильма"""
    list_display = ('title', 'movie', 'get_image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src= {obj.image.url} width="110px" height="130px"')

    get_image.short_description = "Изображение"


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """Актеры"""
    list_display = ('name', 'age', 'get_image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src= {obj.image.url} width="50px" height="60px"')

    get_image.short_description = "Изображение"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ("movie", "ip", "star")


admin.site.register(RatingStar)

admin.site.site_title = 'CinemaClub'
admin.site.site_header = 'CinemaClub'
