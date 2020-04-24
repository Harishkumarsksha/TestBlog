from django.contrib import admin

# Register your models here.
from Blog.models import Post
from Blog.models import Comment


class PostAdmin(admin.ModelAdmin):

    class Meta:
        list_display = ['title', 'slug', 'Author',
                        'publish', 'created', 'updated', 'status']

        list_fliter = ['status', 'created', 'publish', 'author']
        search_fields = ['title', 'body']
        prepopulated_fields = {'slug': ('title',)}
        raw_id_fields = ('author')
        ordering = ['status', 'publish']


class CommentAdmin(admin.ModelAdmin):
    class Meta:
        fields = '__all__'


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
