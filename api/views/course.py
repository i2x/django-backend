from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.models import Course


class CourseListView(APIView):

    def get(self, request):
        """ Fetch all courses with ID and name """
        courses = Course.objects.all()
        course_data = [{"id": course.id, "name": course.name} for course in courses]
        return Response({"courses": course_data}, status=status.HTTP_200_OK)
