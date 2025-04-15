# dashboard/forms.py (updated)
from django import forms

class PredictionForm(forms.Form):
    SUBJECT_CHOICES = [
        ('CS', 'Computer Science'),
        ('MATH', 'Mathematics'),
        ('ENG', 'Engineering'),
        ('ART', 'Art'),
        ('PHYS', 'Physics'),
        ('CHEM', 'Chemistry'),
        ('BIO', 'Biology'),
        ('ENGL', 'English'),
        ('HIST', 'History'),
        ('PSYC', 'Psychology'),
    ]
    
    DAY_CHOICES = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    ]
    
    subject = forms.ChoiceField(
        choices=SUBJECT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    course_number = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. 101, 205A'
        })
    )
    
    meeting_day = forms.ChoiceField(
        choices=DAY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )