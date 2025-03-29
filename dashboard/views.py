# dashboard/views.py
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .forms import PredictionForm
from .utils import ResourcePredictor
from .models import CourseData
import logging

logger = logging.getLogger(__name__)

class HomeView(View):
    template_name = 'dashboard/home.html'

    def get(self, request):
        try:
            recent_predictions = CourseData.objects.all().order_by('-created_at')[:10]
            logger.info(f"Fetched {len(recent_predictions)} recent predictions")
            
            context = {
                'recent_predictions': recent_predictions,
            }
            return render(request, self.template_name, context)
            
        except Exception as e:
            logger.error(f"Error in HomeView: {str(e)}")
            messages.error(request, "An error occurred while loading the dashboard.")
            return render(request, self.template_name, {'recent_predictions': []})

class InsightsView(View):
    template_name = 'dashboard/insights.html'

    def get(self, request):
        try:
            # Tableau visualization parameters
            tableau_visualizations = [
                {
                    'title': 'Enrollment Trends',
                    'embed_url': 'https://public.tableau.com/views/SchoolEnrollmentTrends/Dashboard1',
                    'width': '100%',
                    'height': '600px'
                },
                {
                    'title': 'Room Utilization',
                    'embed_url': 'https://public.tableau.com/views/RoomUtilization/Dashboard2',
                    'width': '100%',
                    'height': '600px'
                },
                {
                    'title': 'Course Demand Analysis',
                    'embed_url': 'https://public.tableau.com/views/CourseDemand/Dashboard3',
                    'width': '100%',
                    'height': '800px'
                }
            ]
            
            context = {
                'visualizations': tableau_visualizations,
                'active_page': 'insights'
            }
            return render(request, self.template_name, context)
            
        except Exception as e:
            logger.error(f"Error in InsightsView: {str(e)}")
            messages.error(request, "An error occurred while loading insights.")
            return render(request, self.template_name, {'visualizations': []})

class PredictionView(View):
    template_name = 'dashboard/prediction.html'
    predictor = ResourcePredictor()

    def get(self, request):
        try:
            form = PredictionForm()
            recent_predictions = CourseData.objects.all().order_by('-created_at')[:5]
            
            context = {
                'form': form,
                'recent_predictions': recent_predictions,
            }
            return render(request, self.template_name, context)
            
        except Exception as e:
            logger.error(f"Error in PredictionView GET: {str(e)}")
            messages.error(request, "An error occurred while loading the prediction form.")
            return render(request, self.template_name, {'form': PredictionForm()})

    def post(self, request):
        try:
            form = PredictionForm(request.POST)
            recent_predictions = CourseData.objects.all().order_by('-created_at')[:5]
            
            if form.is_valid():
                subject = form.cleaned_data['subject']
                course_number = form.cleaned_data['course_number']
                meeting_day = form.cleaned_data['meeting_day']
                
                logger.info(f"Making prediction for {subject} {course_number} on {meeting_day}")
                
                # Get prediction
                prediction = self.predictor.predict(subject, course_number, meeting_day)
                logger.info(f"Prediction result: {prediction}")
                
                # Save to database
                try:
                    CourseData.objects.create(
                        subject=subject,
                        course_number=course_number,
                        meeting_day=meeting_day,
                        room_capacity=prediction['room_capacity'],
                        predicted_enrollment=prediction['predicted_enrollment'],
                        seats_available=prediction['seats_available'],
                        building=prediction['building'],
                        room=prediction['room'],
                        begin_time=prediction['begin_time'],
                        end_time=prediction['end_time']
                    )
                    logger.info("Successfully saved prediction to database")
                except Exception as e:
                    logger.error(f"Error saving to database: {str(e)}")
                    messages.warning(request, "Prediction was successful but couldn't save to history.")
                
                context = {
                    'form': form,
                    'prediction': prediction,
                    'subject': subject,
                    'course_number': course_number,
                    'meeting_day': meeting_day,
                    'recent_predictions': recent_predictions,
                }
                return render(request, self.template_name, context)
            
            logger.warning("Invalid form submission")
            messages.error(request, "Please correct the errors in the form.")
            return render(request, self.template_name, {
                'form': form,
                'recent_predictions': recent_predictions,
            })
            
        except Exception as e:
            logger.error(f"Error in PredictionView POST: {str(e)}")
            messages.error(request, "An error occurred while processing your prediction.")
            return render(request, self.template_name, {
                'form': PredictionForm(request.POST),
                'recent_predictions': recent_predictions,
            })