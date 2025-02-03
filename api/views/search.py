from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.http import JsonResponse


# ✅ Search Files API (No authentication required)
class SearchFilesView(APIView):
    permission_classes = [IsAuthenticated]  # ✅ Requires login

    def get(self, request):
        file_name = request.GET.get('name', '').strip().lower()

        # Mock file data (Replace this with database queries in the future)
        mock_files = [
            {"id": 1, "name": "project_report.pdf"},
            {"id": 2, "name": "design_mockup.png"},
            {"id": 3, "name": "meeting_notes.txt"},
            {"id": 4, "name": "budget_plan.xlsx"},
            {"id": 5, "name": "presentation.pptx"},



        ]

        # If file_name exists, filter results
        filtered_files = [file for file in mock_files if file_name in file["name"].lower()] if file_name else mock_files

        return JsonResponse(filtered_files, safe=False)