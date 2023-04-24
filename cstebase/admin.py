from django.contrib import admin
from .models import Question,Comment,AboutPage,teamMember


class CommentAdmin(admin.StackedInline):
    model = Comment
    extra = 0



class QuestionsAdmin(admin.ModelAdmin):
    list_display = ("title","tag_list",)
#     prepopulated_fields = {"slug": ("title",)}  # new
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())
    inlines = [CommentAdmin]


admin.site.register(Question,QuestionsAdmin)
admin.site.register(Comment)
admin.site.register(teamMember)
admin.site.register(AboutPage)