from django.shortcuts import render

from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated


from .models import (Course, Student, StudentGroup, Lesson, Category, Enrollment, Instructor, LikeDislike, Comments)

from .serializers import (CategorySerializer, CourseSerializer, LessonSerializer, 
                          EnrollmentSerializer, InstructorSerializer, StudentSerializer,
                          StudentGroupSerializer, CommentsSerializer, UserRegistrationSerializer,
                          LikeDislikeSerializer)

# Create your views here.


"""Category-lar uchun ViewSet"""
class CategoryViewSet(ViewSet):
    def list(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category)
            return Response(serializer.data)
        except Category.DoesNotExist:
            return Response({"message": f"Category with ID {pk} not found!"})
    
    def create(self, request, pk=None):
        if not pk:
            serializer = CategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.errors)
        return Response({"message": f"CREATE method does not require an ID!"})

    def update(self, request, pk=None):
        if pk:
            try:
                category = Category.objects.get(pk=pk)
                serializer = CategorySerializer(category, data=request.data)
                return Response(serializer.data)
            except Category.DoesNotExist:
                return Response({"message": f"Object with ID {pk} not found!"})
        else:
            return Response({"message": f"UPDATE method does not require an ID!"})
        
    def destroy(self, request, pk=None):
        if pk:
            try:
                category = Category.objects.get(pk=pk)
                category.delete()
                return Response({"message": f"Successfully deleted!"})
            except Category.DoesNotExist:
                return Response({"message": f"Object with ID {pk} not found!"})
        return Response({"message": f"DELETE method requires an ID"})
    
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminUser()]
        else:
            return [IsAuthenticatedOrReadOnly()]


"""Course-lar uchun ViewSet"""
class CourseViewSet(ViewSet):
    def list(self, request):
        course = Course.objects.all()
        serializer = CourseSerializer(course, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        try:
            course = Course.objects.get(pk=pk)
            serializer = CourseSerializer(course)
            return Response(serializer.data)
        except Course.DoesNotExist:
            return Response({"message": f"Object with ID {pk} not found!"})
    
    def create(self, request, pk=None):
        if not pk:
            serializer = CourseSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.errors)
        return Response({"message": f"CREATE method does not require an ID!"})

    def update(self, request, pk=None):
        if pk:
            try:
                course = Course.objects.get(pk=pk)
                serializer = CourseSerializer(course, data=request.data)
                return Response(serializer.data)
            except Course.DoesNotExist:
                return Response({"message": f"Object with ID {pk} not found!"})
        else:
            return Response({"message": f"UPDATE method does not require an ID!"})
        
    def destroy(self, request, pk=None):
        if pk:
            try:
                course = Course.objects.get(pk=pk)
                course.delete()
                return Response({"message": f"Successfully deleted!"})
            except Course.DoesNotExist:
                return Response({"message": f"Object with ID {pk} not found!"})
        return Response({"message": f"DELETE method requires an ID"})
    
    def get_permissions(self):
        if self.request.method in ["POST", "DELETE", "PUT"]:
            return [IsAdminUser()]
        else:
            return [IsAuthenticatedOrReadOnly()]
        

"""Lesson-lar uchun ViewSet"""
class LessonViewSet(ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method in ["POST", "DELETE", "PUT"]:
            return [IsAdminUser()]
        else:
            return [IsAuthenticatedOrReadOnly()]
        
    def get_queryset(self):
        title = self.request.query_params.get("title")
        if title:
            return Lesson.objects.filter(title=title)
        return Lesson.objects.all()


"""Student-lar uchun ViewSet"""
class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_permissions(self):
        if self.request.method in ["POST", "DELETE", "PUT"]:
            return [IsAdminUser(), IsAuthenticated()]
        else:
            return [IsAuthenticatedOrReadOnly()]
        

"""Group-lar uchun ViewSet"""
class StudentGroupViewSet(ModelViewSet):
    queryset = StudentGroup.objects.all()
    serializer_class = StudentGroupSerializer

    def get_permissions(self):
        if self.request.method in ["POST", "DELETE", "PUT"]:
            return [IsAdminUser()]
        else:
            return [IsAuthenticatedOrReadOnly()]


"""Ustozlar uchun ViewSet"""
class InstructorViewSet(ModelViewSet):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer

    def get_permissions(self):
        if self.request.method in ["POST", "DELETE", "PUT"]:
            return [IsAdminUser()]
        else:
            return [IsAuthenticatedOrReadOnly()]


"""Bitiruvchilik uchun ViewSet"""
class EnrollmentViewSet(ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    depth = 2

    def get_permissions(self):
        if self.request.method in ["POST", "DELETE", "PUT"]:
            return [IsAdminUser()]
        else:
            return [IsAuthenticatedOrReadOnly()]


class CommentsViewSet(ViewSet):
    def list(self, request):
        comments = Comments.objects.all()
        serializer = CommentsSerializer(comments, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        try:
            comment = Comments.objects.get(pk=pk)
            serializer = CommentsSerializer(comment)
            return Response(serializer.data)
        except Course.DoesNotExist:
            return Response({"message": f"Object with ID {pk} not found!"})
    
    def create(self, request, pk=None):
        if not pk:
            serializer = CommentsSerializer(data=request.data)
            if serializer.is_valid():
                student = Student.objects.get(user=request.user)
                lesson_id = serializer.validated_data['lesson']
                lesson = Lesson.objects.get(id=lesson_id)
                serializer.save(student=student, lesson=lesson)
            return Response(serializer.errors)
        return Response({"message": f"CREATE method does not require an ID!"})

    def update(self, request, pk=None):
        if pk:
            try:
                comments = Comments.objects.get(pk=pk)
                serializer = CommentsSerializer(comments, data=request.data)
                return Response(serializer.data)
            except Course.DoesNotExist:
                return Response({"message": f"Object with ID {pk} not found!"})
        else:
            return Response({"message": f"UPDATE method does not require an ID!"})
        
    def destroy(self, request, pk=None):
        if pk:
            try:
                comments = Comments.objects.get(pk=pk)
                comments.delete()
                return Response({"message": f"Successfully deleted!"})
            except Course.DoesNotExist:
                return Response({"message": f"Object with ID {pk} not found!"})
        return Response({"message": f"DELETE method requires an ID"})

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        else:
            return [AllowAny()]


"""Like/Dislike ViewSet"""
class LikeDislikeViewSet(ModelViewSet):
    queryset = LikeDislike.objects.all()
    serializer_class = LikeDislikeSerializer

    def create(self, request, *args, **kwargs):
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            return Response({'detail': 'Student profile not found.'}, status=404)
        
        lesson_id = request.data.get('lesson')
        vote = request.data.get('vote')

        lesson = Lesson.objects.filter(id=lesson_id).first()
        if not lesson:
            return Response({"message": "Lesson not found!"})
        
        if vote is True: 
            lesson.likes += 1
            lesson.dislikes -= 1  
        elif vote is False:  
            lesson.dislikes += 1
            lesson.likes -= 1
        
        lesson.save() 
        
        like_dislike, _ = LikeDislike.objects.update_or_create(
            student = student,
            lesson = lesson,
            defaults={'vote': vote}
        )
        return Response({"message": "Vote Recorded"})


"""User Registration"""
class UserRegistrationViewSet(ViewSet):
    def create(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'username': user.username, 'email': user.email})
        return Response(serializer.errors)