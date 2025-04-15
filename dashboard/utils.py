import random
from datetime import datetime, timedelta
from .models import CourseData

class ResourcePredictor:
    def predict(self, subject, course_number, meeting_day):
        # Parse course number to integer
        course_number_int = int(''.join(filter(str.isdigit, course_number)) if any(c.isdigit() for c in course_number) else 100)
        
        # Map subject to building
        building_map = {
            'CS': 'Tech Center', 
            'MATH': 'Math Hall', 
            'ENG': 'Engineering Building',
            'ART': 'Art Studio', 
            'PHYS': 'Physics Center', 
            'CHEM': 'Chemistry Building'
        }
        building = building_map.get(subject, 'General Building')
        
        # Generate random room number
        room = random.randint(100, 500)
        
        # Define possible start times (in minutes from midnight)
        start_times = [8 * 60, 8 * 60 + 30, 9 * 60, 9 * 60 + 30, 10 * 60, 10 * 60 + 30, 11 * 60, 11 * 60 + 30]
        duration_choices = [75, 90, 105]  # in minutes
        
        base_minutes = random.choice(start_times)
        duration = random.choice(duration_choices)
        end_minutes = base_minutes + duration

        # Ensure end time doesn't go past 5:00 PM (17:00 = 1020 minutes)
        if end_minutes > 17 * 60:
            end_minutes = 17 * 60

        # Convert minutes back to readable time format
        begin_time = (datetime(100, 1, 1, 0, 0) + timedelta(minutes=base_minutes)).strftime('%H:%M')
        end_time = (datetime(100, 1, 1, 0, 0) + timedelta(minutes=end_minutes)).strftime('%H:%M')
        
        # Generate capacity and enrollment
        capacity = random.randint(20, 120)
        enrollment = min(capacity + 15, random.randint(10, capacity + 15))  # Allow slight over-enroll
        seats_available = max(0, capacity - enrollment)
        
        return {
            'room_capacity': capacity,
            'predicted_enrollment': enrollment,
            'seats_available': seats_available,
            'building': building,
            'room': room,
            'begin_time': begin_time,
            'end_time': end_time,
        }
