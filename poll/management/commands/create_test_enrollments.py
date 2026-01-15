from django.core.management.base import BaseCommand
from poll.models import Course, Student, Enrollment
from django.utils import timezone
import random


class Command(BaseCommand):
    help = 'Create test enrollments for a specific course'

    def add_arguments(self, parser):
        parser.add_argument('--course', type=str, help='Course name (partial match)')
        parser.add_argument('--count', type=int, default=48, help='Number of enrollments to create')

    def handle(self, *args, **options):
        course_name = options.get('course') or 'Embedded'
        count = options.get('count')

        # Find the course
        try:
            course = Course.objects.get(name__icontains=course_name)
        except Course.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Course matching "{course_name}" not found'))
            return
        except Course.MultipleObjectsReturned:
            course = Course.objects.filter(name__icontains=course_name).first()

        self.stdout.write(f'Creating {count} enrollments for: {course.name}')

        # Sample names for generating students
        first_names = [
            'Arun', 'Bharath', 'Chandra', 'Deepak', 'Ezhil', 'Fathima', 'Ganesh', 'Harini',
            'Ishaan', 'Jaya', 'Karthik', 'Lakshmi', 'Mohan', 'Nithya', 'Om', 'Priya',
            'Rajan', 'Sakthi', 'Tamil', 'Uma', 'Vignesh', 'Yamini', 'Zara', 'Ajay',
            'Bala', 'Chitra', 'Dhana', 'Elango', 'Feroz', 'Gowri', 'Hari', 'Indira',
            'Jeeva', 'Kannan', 'Lavanya', 'Mani', 'Naveen', 'Oviya', 'Prabhu', 'Ramya',
            'Senthil', 'Thiru', 'Usha', 'Vasanth', 'Wilson', 'Xavier', 'Yuvan', 'Zoya'
        ]
        
        last_names = [
            'Kumar', 'Rajan', 'Krishnan', 'Venkatesh', 'Subramanian', 'Pillai', 'Naidu',
            'Sharma', 'Murugan', 'Selvam', 'Pandian', 'Raj', 'Devi', 'Lakshmi', 'Priya'
        ]

        sections = ['A', 'B', 'C']
        created_count = 0

        for i in range(count):
            roll_number = f"23ECE{str(i+1).zfill(3)}"
            
            # Check if student already exists
            if Student.objects.filter(roll_number=roll_number).exists():
                self.stdout.write(self.style.WARNING(f'Student {roll_number} already exists, skipping'))
                continue

            # Generate random student data
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            name = f"{first_name} {last_name}"
            section = random.choice(sections)
            email = f"{roll_number.lower()}@kct.ac.in"
            phone = f"98{random.randint(10000000, 99999999)}"

            # Create student
            student = Student.objects.create(
                roll_number=roll_number,
                name=name,
                email=email,
                phone=phone,
                section=section
            )

            # Create enrollment
            Enrollment.objects.create(
                student=student,
                course=course,
                status='confirmed'
            )

            created_count += 1
            self.stdout.write(f'  ✓ {roll_number} - {name} ({section})')

        self.stdout.write(self.style.SUCCESS(f'\n✅ Created {created_count} enrollments for "{course.name}"'))
        self.stdout.write(f'   Total enrolled: {course.enrolled_count} / {course.max_capacity}')
