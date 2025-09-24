from django.urls import path
from processor.views import ExemptConfigAPIView,ExemptRuleView


app_name = 'exempt_amt'

urlpatterns = [
    path("config/", ExemptConfigAPIView.as_view()),
    path("config/<int:pk>/", ExemptConfigAPIView.as_view()),
    path("rules/", ExemptRuleView.as_view()),        # GET all, POST
    path("rules/<int:pk>/",ExemptRuleView.as_view()),  # GET one, PUT, DELETE
]


