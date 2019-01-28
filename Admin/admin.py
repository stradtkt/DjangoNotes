# based on a course list app

# python manage.py createsuperuser

#change the templates in admin django/contrib/admin/templates/admin in the source code name the files the same and put it in a folder called admin

from django.contrib import admin
from . import models


class TextInline(admin.StackedInline):
    model = models.Text


class QuizInline(admin.StackedInline):
    model = models.Quiz


class AnswerInline(admin.StackedInline):
    model = models.Answer

class YearListFilter(admin.SimpleListFilter):
    title = 'year created'
    parameter_name = 'year'

    def lookups(self, request, model_admin):
        return (
            ('2015', '2015'),
            ('2016', '2016'),
        )
    
    def queryset(self, request, queryset):
        if self.value() == '2015':
            return queryset.filter(created_at__gte=date(2015, 1, 1), created_at__lte=date(2015, 12, 31))
        if self.value() == '2016':
            return queryset.filter(created_at__gte=date(2016, 1, 1), created_at__lte=date(2016, 12, 31))


class CourseAdmin(admin.ModelAdmin):
    inlines = [TextInline, QuizInline]
    search_fields = ['title', 'description']
    list_filter = ['created_at', 'is_live', YearListFilter]
    list_display = ['title', 'created_at', 'is_live', 'time_to_complete']
    
    
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline,]
    search_fields = ['prompt']
    
    
class QuizAdmin(admin.ModelAdmin):
    fields = ['course', 'title', 'description', 'order', 'total_questions']
    list_display = ['prompt', 'quiz', 'order']
    list_editable = ['quiz', 'order']
    
    
class TextAdmin(admin.ModelAdmin):
    fields = ['course', 'title', 'order', 'description']


admin.site.register(models.Course, CourseAdmin)
admin.site.register(models.Text, TextAdmin)
admin.site.register(models.Quiz, QuizAdmin)
admin.site.register(models.MultipleChoiceQuestion, QuestionAdmin)
admin.site.register(models.TrueFalseQuestion, QuestionAdmin)
