from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
# Create your models here.


class Category(models.Model):
    '''Kurs kategoriyalari uchun'''
    title = models.CharField(max_length=150)

    def __str__(self) -> str:
        return self.title
    

class Instructor(models.Model):
    '''Ustozlar uchun model'''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Category, on_delete=models.PROTECT)
    profile_picture = models.ImageField(upload_to='instructors/', blank=True, null=True)

    def __str__(self) -> str:
        return self.user.username
    

class Course(models.Model):
    '''Kurs-lar uchun model'''
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    title = models.CharField(max_length=250)
    description = models.TextField()
    duration = models.CharField(max_length=100)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title
    

class Student(models.Model):
    '''O'quvchi-lar uchun model'''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.ManyToManyField('StudentGroup', related_name="students", blank=True)
    course = models.ManyToManyField(Course)
    enrolled_course = models.ManyToManyField(Course, related_name='students', blank=True)

    def __str__(self) -> str:
        return self.user.username
    

class StudentGroup(models.Model):
    '''Guruhlar uchun model'''
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    title = models.CharField(max_length=150)
    room = models.CharField(max_length=150)

    def __str__(self) -> str:
        return self.title


def validate_video(value):
    if not value.name.endswith(('.mp4', '.avi')):
        raise ValidationError('Faqat .mp4 va .avi fayl turlari qabul qilinadi!')


class Lesson(models.Model):
    '''Dars-lar uchun model'''
    group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    video = models.FileField(upload_to='media/', validators=[validate_video])
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return self.title
    

class Enrollment(models.Model):
    '''Bitiruvchilar uchun model'''
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.student.user.username


class Comments(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.student.user.username


class LikeDislike(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    vote = models.BooleanField(null=True, blank=True) 

    class Meta:
        unique_together = ('student', 'lesson')


