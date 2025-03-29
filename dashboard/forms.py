from django import forms

class PredictionForm(forms.Form):
    SUBJECT_CHOICES = [
        ('MATH', 'Mathematics'),
        ('CS', 'Computer Science'),
        ('ENG', 'Engineering'),
        ('ART', 'Art'),
        ('PHYS', 'Physics'),
        ('CHEM', 'Chemistry'),
    ]
    
    DAY_CHOICES = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
    ]
    
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES)
    course_number = forms.CharField(max_length=10)
    meeting_day = forms.ChoiceField(choices=DAY_CHOICES)