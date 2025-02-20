from django.contrib import admin
from .models import Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'check_in', 'check_out')
    list_filter = ('date',)
    search_fields = ('employee__firstname', 'employee__lastname')