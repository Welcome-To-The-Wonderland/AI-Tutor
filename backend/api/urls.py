from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
from .views import get_questions, get_feedback, get_ai_assistant, log_response, completion_view, get_enrichment_questions, evaluate_question

urlpatterns = [
    path("", views.get_routes),
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('questions/', get_questions, name='get_questions'),
    path('get_feedback/', get_feedback, name='get_feedback'),
    path('api/get_ai_assistant/', get_ai_assistant, name='get_ai_assistant'),
    path('log_response/', log_response, name='log_response'),
    path('completion/', completion_view, name='completion_view'),
    path('enrichment_questions/', get_enrichment_questions,
         name='get_enrichment_questions'),
    path('evaluate_question/', evaluate_question, name='evaluate_question')
]
