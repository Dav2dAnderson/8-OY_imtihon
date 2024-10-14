from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *
# Register your models here.

class CourseInline(admin.TabularInline):
    model = Course
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'instructor', 'price', 'duration')


@admin.register(StudentGroup)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('title', )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', )

    inlines = [
        CourseInline,
    ]


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'view_image')

    def view_image(self, instructor):
        return mark_safe(f'<img src="{instructor.profile_picture.url}" witdh="60" height="60" />')
    view_image.short_description = "Picture"


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'group', 'likes', 'dislikes')


@admin.register(Enrollment)
class Enrollment(admin.ModelAdmin):
    list_display = ('student',  'course', 'group')


@admin.register(LikeDislike)
class LikeDislike(admin.ModelAdmin):
    list_display = ('student', 'lesson', 'vote')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', )


@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('student', 'lesson')