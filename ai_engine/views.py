from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
import os
from django.core.files.storage import default_storage

# Import our ML engines
from .ml_core.rag_pipeline import rag_system
from .ml_core.vision_agent import vision_agent

@api_view(['POST'])
def generate_strategy(request):
    """Endpoint for the text-based RAG queries."""
    query = request.data.get("query")
    if not query:
        return Response({"error": "Query is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Fetch context and generate prompt via RAG
    strategy = rag_system.retrieve_strategy(query)
    
    return Response({
        "query": query,
        "strategy": strategy,
        "status": "success"
    })

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def analyze_competitor_image(request):
    """Endpoint for uploading and analyzing flyers/storefronts via OpenCV."""
    file = request.FILES.get('image')
    if not file:
        return Response({"error": "Image file is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Save file temporarily to disk so OpenCV can read it
    file_name = default_storage.save(file.name, file)
    file_path = default_storage.path(file_name)

    try:
        # Run computer vision analysis
        analysis_results = vision_agent.process_image(file_path)
    finally:
        # Clean up the temporary file
        if os.path.exists(file_path):
            os.remove(file_path)

    return Response({
        "analysis": analysis_results,
        "status": "success"
    })