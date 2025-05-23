# dashboard/models.py
from django.db import models
from django.utils import timezone

class CourseData(models.Model):
    DAY_CHOICES = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    ]
    
    subject = models.CharField(max_length=50)
    course_number = models.CharField(max_length=10)
    meeting_day = models.CharField(max_length=10, choices=DAY_CHOICES)
    room_capacity = models.IntegerField()
    predicted_enrollment = models.IntegerField()
    seats_available = models.IntegerField()
    building = models.CharField(max_length=50)
    room = models.CharField(max_length=10)
    begin_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.subject} {self.course_number} - {self.get_meeting_day_display()}"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Course Prediction'
        verbose_name_plural = 'Course Predictions'