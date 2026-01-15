from django.urls import path
from . import views

urlpatterns = [
    # Original vote path
    path("vote/", views.vote, name='vote'),
    
    # Value-Added Course Enrollment URLs
    path("", views.enrollment_home, name='enrollment_home'),
    path("enroll/", views.enroll_student, name='enroll_student'),
    path("check-enrollment/", views.check_enrollment, name='check_enrollment'),
    path("statistics/", views.course_statistics, name='course_statistics'),
    path("dashboard/", views.enrollment_dashboard, name='enrollment_dashboard'),
    path("syllabus/<int:course_id>/", views.course_syllabus, name='course_syllabus'),
    path("students/<int:course_id>/", views.student_list_by_course, name='student_list_by_course'),
]
