from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published', 'created_at')
    list_filter = ('published', 'created_at')
    search_fields = ('title', 'content')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')
    actions = ['publish_posts', 'unpublish_posts']

    @admin.action(description='Publicar posts selecionados')
    def publish_posts(self, request, queryset):
        queryset.update(published=True)

    @admin.action(description='Despublicar posts selecionados')
    def unpublish_posts(self, request, queryset):
        queryset.update(published=False)
