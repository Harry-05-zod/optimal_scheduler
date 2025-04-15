# dashboard/utils.py
import random
from datetime import datetime, timedelta
from .models import CourseData

class ResourcePredictor:
    def predict(self, form_data):
        # Calculate duration in minutes
        duration = (datetime.combine(datetime.today(), form_data['end_time']) - 
                   datetime.combine(datetime.today(), form_data['begin_time'])).seconds // 60
        
        # Generate capacity based on room size (randomized for demo)
        capacity = random.randint(20, 120)
        
        # Predict enrollment based on course level (extracted from course number)
        course_num = int(''.join(filter(str.isdigit, form_data['course_number'])) if any(c.isdigit() for c in form_data['course_number']) else 100)
        if course_num < 200:
            enrollment = random.randint(15, capacity)
        elif course_num < 300:
            enrollment = random.randint(10, min(40, capacity))
        else:
            enrollment = random.randint(5, min(25, capacity))
            
        seats_available = max(0, capacity - enrollment)
        
        return {
            'room_capacity': capacity,
            'predicted_enrollment': enrollment,
            'seats_available': seats_available,
            'building': form_data['building'],
            'room': form_data['room'],
            'begin_time': form_data['begin_time'].strftime('%H:%M'),
            'end_time': form_data['end_time'].strftime('%H:%M'),
        }