from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CourseViewSet, LessonViewSet, 
                    StudentViewSet, StudentGroupViewSet, EnrollmentViewSet,
                    CommentsViewSet, UserRegistrationViewSet, LikeDislikeViewSet)


router = DefaultRouter()
router.register('category', CategoryViewSet, basename="category")
router.register('course', CourseViewSet, basename="course")
router.register('lesson', LessonViewSet)
router.register('student', StudentViewSet)
router.register('student-group', StudentGroupViewSet)
router.register('enrollment', EnrollmentViewSet)
router.register('comments', CommentsViewSet, basename="comments")
router.register('register', UserRegistrationViewSet, basename="register")
router.register('likes-dislikes', LikeDislikeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]