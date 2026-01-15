from django.contrib import admin
from .models import Vote, Course, Student, Enrollment

# Original Vote Admin
@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'choice')
    list_filter = ('choice',)
    search_fields = ('choice',)


# Course Admin
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'enrolled_count', 'max_capacity', 'available_slots', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    readonly_fields = ('enrolled_count', 'available_slots', 'created_at', 'updated_at')
    fieldsets = (
        ('Course Information', {
            'fields': ('name', 'description', 'syllabus')
        }),
        ('Display Settings', {
            'fields': ('icon', 'color')
        }),
        ('Capacity', {
            'fields': ('max_capacity', 'enrolled_count', 'available_slots')
        }),
        ('Status', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )


# Student Admin
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('roll_number', 'name', 'section', 'email', 'phone', 'registered_at')
    list_filter = ('section', 'registered_at')
    search_fields = ('roll_number', 'name', 'email')
    readonly_fields = ('registered_at',)
    ordering = ('roll_number',)


# Enrollment Admin
@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'status', 'enrolled_at')
    list_filter = ('course', 'status', 'enrolled_at')
    search_fields = ('student__name', 'student__roll_number', 'course__name')
    readonly_fields = ('enrolled_at', 'updated_at')
    raw_id_fields = ('student', 'course')
    date_hierarchy = 'enrolled_at'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('student', 'course')
