from django.db import models
from django.utils import timezone

# Original Vote model
class Vote(models.Model):
    choice = models.CharField(max_length=50)

    def __str__(self):
        return self.choice


# Value-Added Course Enrollment Models
class Course(models.Model):
    """Model for Value-Added Courses"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    syllabus = models.TextField(blank=True, help_text="Course syllabus content")
    max_capacity = models.PositiveIntegerField(default=50)
    icon = models.CharField(max_length=50, default='📚', help_text="Emoji or icon for the course")
    color = models.CharField(max_length=7, default='#6366f1', help_text="Hex color for the course card")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def enrolled_count(self):
        return self.enrollments.filter(status='confirmed').count()

    @property
    def available_slots(self):
        return max(0, self.max_capacity - self.enrolled_count)

    @property
    def is_full(self):
        return self.enrolled_count >= self.max_capacity


class Student(models.Model):
    """Model for Student Information"""
    roll_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    section = models.CharField(max_length=10, blank=True)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['roll_number']

    def __str__(self):
        return f"{self.roll_number} - {self.name}"


class Enrollment(models.Model):
    """Model for Course Enrollments"""
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('waitlist', 'Waitlist'),
        ('transferred', 'Transferred'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    enrolled_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['enrolled_at']
        unique_together = ['student', 'course']

    def __str__(self):
        return f"{self.student.name} - {self.course.name} ({self.status})"

    def save(self, *args, **kwargs):
        # Check if this is a new enrollment
        if not self.pk:
            # Check if course is full
            if self.course.enrolled_count >= self.course.max_capacity:
                self.status = 'waitlist'
        super().save(*args, **kwargs)
