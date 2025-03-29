from django.db import models

class CourseData(models.Model):
    subject = models.CharField(max_length=50)
    course_number = models.CharField(max_length=10)
    meeting_day = models.CharField(max_length=10)
    room_capacity = models.IntegerField()
    predicted_enrollment = models.IntegerField()
    seats_available = models.IntegerField()
    building = models.CharField(max_length=50)
    room = models.CharField(max_length=10)
    begin_time = models.CharField(max_length=10)
    end_time = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} {self.course_number}"
