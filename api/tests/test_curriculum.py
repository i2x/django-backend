from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models.curriculum import Curriculum, CurriculumMapping
from api.models.course import Course

class CurriculumAPITestCase(APITestCase):
    def setUp(self):
        # Create Course objects
        self.course1 = Course.objects.create(
            id='C001',
            name='Introduction to Programming'
        )
        self.course2 = Course.objects.create(
            id='C002',
            name='Data Structures'
        )

        # Create Curriculum objects
        self.curriculum1 = Curriculum.objects.create(
            id='CURR001',
            name='Computer Science Basics',
            year=2023
        )
        self.curriculum2 = Curriculum.objects.create(
            id='CURR002',
            name='Advanced Computer Science',
            year=2023
        )

        # Create CurriculumMapping objects to associate curriculums with courses
        CurriculumMapping.objects.create(
            curriculum=self.curriculum1, course=self.course1, year=2023, term=1
        )
        CurriculumMapping.objects.create(
            curriculum=self.curriculum1, course=self.course2, year=2023, term=2
        )
        CurriculumMapping.objects.create(
            curriculum=self.curriculum2, course=self.course1, year=2023, term=1
        )

    def test_curriculum_latest_view(self):
        """
        Test that the /curriculum/ endpoint (named 'curriculum-latest')
        returns the latest curriculum's courses.
        For this test, we assume the view returns curriculum2 as the latest.
        """
        url = reverse('curriculum-latest')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        # Verify that the returned curriculum is the expected latest one.
        self.assertEqual(data['curriculum'], self.curriculum2.name)
        # For curriculum2, only course1 is mapped.
        courses = data.get('courses', [])
        self.assertEqual(len(courses), 1)
        self.assertEqual(courses[0]['id'], self.course1.id)
        self.assertEqual(courses[0]['name'], self.course1.name)

    def test_curriculum_latest_view_no_curriculum(self):
        """
        Test that if no curriculum exists, the /curriculum/ endpoint returns a 404 with an error message.
        """
        # Delete all curriculums
        Curriculum.objects.all().delete()
        url = reverse('curriculum-latest')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.json()
        self.assertIn('error', data)
        self.assertEqual(data['error'], "No curriculum found")

