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
                form_data = form.cleaned_data
                
                logger.info(f"Making prediction for {form_data['subject']} {form_data['course_number']}")
                
                # Get prediction
                prediction = self.predictor.predict(form_data)
                logger.info(f"Generated prediction: {prediction}")
                
                # Save to database
                try:
                    CourseData.objects.create(
                        subject=form_data['subject'],
                        course_number=form_data['course_number'],
                        meeting_day=form_data['meeting_day'],
                        room_capacity=prediction['room_capacity'],
                        predicted_enrollment=prediction['predicted_enrollment'],
                        seats_available=prediction['seats_available'],
                        building=form_data['building'],
                        room=form_data['room'],
                        begin_time=form_data['begin_time'],
                        end_time=form_data['end_time']
                    )
                    logger.info("Successfully saved prediction to database")
                except Exception as e:
                    logger.error(f"Error saving to database: {str(e)}")
                    messages.warning(request, "Prediction was generated but couldn't save to history.")
                
                context = {
                    'form': form,
                    'prediction': prediction,
                    'subject': form_data['subject'],
                    'course_number': form_data['course_number'],
                    'meeting_day': form_data['meeting_day'],
                    'building': form_data['building'],
                    'room': form_data['room'],
                    'begin_time': prediction['begin_time'],
                    'end_time': prediction['end_time'],
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
            messages.error(request, "An error occurred while generating your prediction.")
            return render(request, self.template_name, {
                'form': PredictionForm(request.POST),
                'recent_predictions': recent_predictions,
            })