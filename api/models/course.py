from django.db import models

class Course(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=255)
    year = models.IntegerField()
    term = models.IntegerField()

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def __str__(self):
        return f"{self.id} - {self.name}"