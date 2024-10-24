""" channels routing for candidates analysis"""

from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path('ws/analisar-candidaturas/<uuid:vid>/<int:num_documents>/',
         consumers.CandidateAnalysisConsumer.as_asgi()),
]
