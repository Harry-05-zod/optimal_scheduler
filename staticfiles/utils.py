import pandas as pd
import numpy as np
import joblib
import os
from django.conf import settings
from sklearn.pipeline import Pipeline

class ResourcePredictor:
    def __init__(self):
        self.model = self.load_model()
        self.features = [
            'Subject', 'CourseNumber', 'StudentLevel', 'College_of_the_Student',
            'Major', 'Course_Location', 'Building', 'Room',
            'SSRMEET_MON_DAY', 'SSRMEET_TUE_DAY', 'SSRMEET_WED_DAY',
            'SSRMEET_THU_DAY', 'SSRMEET_FRI_DAY', 'SSRMEET_SAT_DAY', 
            'SSRMEET_SUN_DAY', 'BeginTime', 'EndTime'
        ]

    def load_model(self):
        model_path = os.path.join(settings.BASE_DIR, 'dashboard', 'models', 'resource_model.pkl')
        try:
            model = joblib.load(model_path)
            if not isinstance(model, Pipeline):
                raise ValueError("Loaded model is not a scikit-learn Pipeline")
            return model
        except FileNotFoundError:
            print(f"No model file found at {model_path}")
            raise
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            raise

    def predict(self, subject, course_number, meeting_day):
        try:
            # Extract numeric part from course number
            try:
                course_num = int(''.join(filter(str.isdigit, course_number)))
            except ValueError:
                course_num = 100  # Default if conversion fails

            # Create input data based on the provided details
            base_time = 800 + (sum(ord(c) for c in subject) % 400)
            input_data = {
                'Subject': subject,
                'CourseNumber': course_num,
                'StudentLevel': ('Freshman' if course_num < 200 else 
                            'Sophomore' if course_num < 300 else 
                            'Junior' if course_num < 400 else 'Senior'),
                'College_of_the_Student': (
                    'Natural Sciences' if subject in ['MATH', 'PHYS', 'CHEM'] else
                    'Fine Arts' if subject in ['ART', 'MUS', 'THEA'] else
                    'Engineering' if subject in ['CS', 'ENG'] else 'Arts and Sciences'),
                'Major': f"{subject} Major",
                'Course_Location': 'Main Campus',
                'Building': (
                    'Science Center' if subject in ['MATH', 'PHYS', 'CHEM'] else
                    'Arts Building' if subject in ['ART', 'MUS', 'THEA'] else
                    'Engineering Hall' if subject in ['CS', 'ENG'] else 'Main Building'),
                'Room': 100 + (course_num % 50),
                'BeginTime': base_time,
                'EndTime': base_time + 90
            }

            # Populate day columns correctly
            day_cols = ['SSRMEET_MON_DAY', 'SSRMEET_TUE_DAY', 'SSRMEET_WED_DAY', 
                        'SSRMEET_THU_DAY', 'SSRMEET_FRI_DAY', 'SSRMEET_SAT_DAY', 
                        'SSRMEET_SUN_DAY']
            for day_col in day_cols:
                input_data[day_col] = 1 if day_col == f'SSRMEET_{meeting_day}_DAY' else 0

            # Create a DataFrame with proper data types
            input_df = pd.DataFrame([input_data])
            for col in ['CourseNumber', 'Room', 'BeginTime', 'EndTime'] + day_cols:
                if col in input_df.columns:
                    input_df[col] = input_df[col].astype(int)
            
            # Ensure the features are in the correct order
            input_df = input_df[self.features]

            # Make prediction
            prediction = self.model.predict(input_df)

            capacity = int(prediction[0][0])
            enrollment = int(prediction[0][1])
            seats = int(prediction[0][2])

            enrollment = min(capacity, max(5, int(enrollment * {
                'CS': 1.3, 'MATH': 1.2, 'ENG': 1.1, 'ART': 0.8
            }.get(subject, 1.0))))

            return {
                'room_capacity': capacity,
                'predicted_enrollment': enrollment,
                'seats_available': capacity - enrollment,
                'building': input_data['Building'],  # Remove .values[0]
                'room': input_data['Room'],          # Remove .values[0]
                'begin_time': f"{base_time//100:02d}:{base_time%100:02d}",
                'end_time': f"{(base_time + 90)//100:02d}:{(base_time + 90)%100:02d}",
            }
        except Exception as e:
            print(f"Prediction error: {str(e)}")
            raise