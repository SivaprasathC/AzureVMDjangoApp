from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from .models import Vote, Course, Student, Enrollment
import json

# Original vote view
def vote(request):
    if request.method == "POST":
        selected = request.POST.get("choice")
        if selected:
            Vote.objects.create(choice=selected)

    total_votes = Vote.objects.count()

    count_a = Vote.objects.filter(choice="Option A").count()
    count_b = Vote.objects.filter(choice="Option B").count()
    count_c = Vote.objects.filter(choice="Option C").count()

    def percent(count):
        return int((count / total_votes) * 100) if total_votes > 0 else 0

    context = {
        "count_a": count_a,
        "count_b": count_b,
        "count_c": count_c,
        "percent_a": percent(count_a),
        "percent_b": percent(count_b),
        "percent_c": percent(count_c),
        "total": total_votes,
    }

    return render(request, "poll/vote.html", context)


# ============================================
# Value-Added Course Enrollment Views
# ============================================

def enrollment_home(request):
    """Main page for course enrollment"""
    courses = Course.objects.filter(is_active=True).annotate(
        confirmed_count=Count('enrollments', filter=Q(enrollments__status='confirmed'))
    )
    
    context = {
        'courses': courses,
        'page_title': 'ECE Value-Added Course Enrollment'
    }
    return render(request, 'poll/enrollment_home.html', context)


def enroll_student(request):
    """Handle student enrollment"""
    if request.method == 'POST':
        roll_number = request.POST.get('roll_number', '').strip().upper()
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        section = request.POST.get('section', '').strip()
        course_id = request.POST.get('course_id')
        
        # Validate inputs
        if not roll_number or not name or not course_id:
            return JsonResponse({
                'success': False,
                'message': 'Please fill all required fields.'
            })
        
        # Get the course
        try:
            course = Course.objects.get(id=course_id, is_active=True)
        except Course.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Selected course is not available.'
            })
        
        # Get or create student
        student, created = Student.objects.get_or_create(
            roll_number=roll_number,
            defaults={
                'name': name,
                'email': email,
                'phone': phone,
                'section': section
            }
        )
        
        # Update student info if already exists
        if not created:
            student.name = name
            if email:
                student.email = email
            if phone:
                student.phone = phone
            if section:
                student.section = section
            student.save()
        
        # Check if student already enrolled in any course
        existing_enrollment = Enrollment.objects.filter(
            student=student, 
            status='confirmed'
        ).first()
        
        if existing_enrollment:
            return JsonResponse({
                'success': False,
                'message': f'You are already enrolled in "{existing_enrollment.course.name}". Each student can only enroll in one course.',
                'already_enrolled': True,
                'enrolled_course': existing_enrollment.course.name
            })
        
        # Check course capacity
        if course.is_full:
            return JsonResponse({
                'success': False,
                'message': f'Sorry, "{course.name}" has reached maximum capacity of {course.max_capacity} students. Please choose another course.',
                'course_full': True
            })
        
        # Create enrollment
        enrollment = Enrollment.objects.create(
            student=student,
            course=course,
            status='confirmed'
        )
        
        # Get updated slot count
        remaining_slots = course.available_slots
        
        return JsonResponse({
            'success': True,
            'message': f'Successfully enrolled in "{course.name}"!',
            'enrollment_id': enrollment.id,
            'remaining_slots': remaining_slots,
            'queue_position': course.enrolled_count
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


def check_enrollment(request):
    """Check enrollment status by roll number"""
    roll_number = request.GET.get('roll_number', '').strip().upper()
    
    if not roll_number:
        return JsonResponse({
            'success': False,
            'message': 'Please enter a roll number.'
        })
    
    try:
        student = Student.objects.get(roll_number=roll_number)
        enrollment = Enrollment.objects.filter(student=student, status='confirmed').first()
        
        if enrollment:
            return JsonResponse({
                'success': True,
                'enrolled': True,
                'student_name': student.name,
                'roll_number': student.roll_number,
                'course_name': enrollment.course.name,
                'enrolled_at': enrollment.enrolled_at.strftime('%d %b %Y, %I:%M %p'),
                'queue_position': Enrollment.objects.filter(
                    course=enrollment.course,
                    status='confirmed',
                    enrolled_at__lte=enrollment.enrolled_at
                ).count()
            })
        else:
            return JsonResponse({
                'success': True,
                'enrolled': False,
                'student_name': student.name,
                'message': 'Student found but not enrolled in any course yet.'
            })
    except Student.DoesNotExist:
        return JsonResponse({
            'success': True,
            'enrolled': False,
            'message': 'No registration found for this roll number.'
        })


def course_statistics(request):
    """Get real-time course statistics"""
    courses = Course.objects.filter(is_active=True).annotate(
        confirmed_count=Count('enrollments', filter=Q(enrollments__status='confirmed'))
    )
    
    data = []
    for course in courses:
        data.append({
            'id': course.id,
            'name': course.name,
            'enrolled': course.confirmed_count,
            'capacity': course.max_capacity,
            'available': course.max_capacity - course.confirmed_count,
            'percentage': round((course.confirmed_count / course.max_capacity) * 100, 1) if course.max_capacity > 0 else 0,
            'is_full': course.confirmed_count >= course.max_capacity,
            'color': course.color
        })
    
    total_enrolled = sum(c['enrolled'] for c in data)
    total_capacity = sum(c['capacity'] for c in data)
    
    return JsonResponse({
        'success': True,
        'courses': data,
        'total_enrolled': total_enrolled,
        'total_capacity': total_capacity
    })


def enrollment_dashboard(request):
    """Dashboard to view all enrollments - for class advisors"""
    courses = Course.objects.filter(is_active=True).prefetch_related('enrollments__student')
    
    course_data = []
    for course in courses:
        enrollments = course.enrollments.filter(status='confirmed').select_related('student').order_by('enrolled_at')
        course_data.append({
            'course': course,
            'enrollments': enrollments,
            'count': enrollments.count()
        })
    
    # Get overall statistics
    total_students = Enrollment.objects.filter(status='confirmed').count()
    
    context = {
        'course_data': course_data,
        'total_students': total_students,
        'page_title': 'Enrollment Dashboard'
    }
    return render(request, 'poll/enrollment_dashboard.html', context)


def course_syllabus(request, course_id):
    """View syllabus for a specific course"""
    course = get_object_or_404(Course, id=course_id, is_active=True)
    
    context = {
        'course': course,
        'page_title': f'{course.name} - Syllabus'
    }
    return render(request, 'poll/course_syllabus.html', context)


def student_list_by_course(request, course_id):
    """Get list of students enrolled in a course"""
    course = get_object_or_404(Course, id=course_id)
    enrollments = Enrollment.objects.filter(
        course=course, 
        status='confirmed'
    ).select_related('student').order_by('enrolled_at')
    
    students = []
    for idx, enrollment in enumerate(enrollments, 1):
        students.append({
            'position': idx,
            'roll_number': enrollment.student.roll_number,
            'name': enrollment.student.name,
            'section': enrollment.student.section,
            'enrolled_at': enrollment.enrolled_at.strftime('%d %b %Y, %I:%M %p')
        })
    
    return JsonResponse({
        'success': True,
        'course_name': course.name,
        'students': students,
        'total': len(students)
    })
