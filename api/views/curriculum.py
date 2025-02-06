from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.models import Curriculum, CurriculumMapping


class CurriculumCoursesView(APIView):

    def get(self, request, curriculum_id=None):
        """ Retrieve courses from a curriculum. If curriculum_id is not provided, fetch the latest curriculum. """
        if curriculum_id is None:
            curriculum = Curriculum.objects.order_by('-year', '-id').first()
            if not curriculum:
                return Response({"error": "No curriculum found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            curriculum = get_object_or_404(Curriculum, pk=curriculum_id)

        mappings = CurriculumMapping.objects.filter(curriculum=curriculum).select_related("course")

        courses = [
            {
                "id": mapping.course.id,
                "name": mapping.course.name,
                "year": mapping.year,
                "term": mapping.term
            }
            for mapping in mappings
        ]

        return Response({"curriculum": curriculum.name, "courses": courses}, status=status.HTTP_200_OK)
