from django.db import models
from .course import Course

class Curriculum(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=255)  

    class Meta:
        verbose_name = "Curriculum"
        verbose_name_plural = "Curriculums"

    def __str__(self):
        return f"{self.id} - {self.name}"
    
class CurriculumMapping(models.Model):  
    curriculum = models.ForeignKey(
        Curriculum, 
        on_delete=models.CASCADE, 
        related_name="curriculum_mappings"
    )  
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE, 
        related_name="curriculum_mappings"
    )  

    class Meta:
        verbose_name = "Curriculum Mapping"
        verbose_name_plural = "Curriculum Mappings"
        unique_together = ('curriculum', 'course')  # ป้องกันการเพิ่มซ้ำ

    def __str__(self):
        return f"{self.curriculum.name} - {self.course.name}"
    
    # 🔹 ฟังก์ชันทดลอง: ดึงหลักสูตรที่วิชานี้อยู่
    @classmethod
    def get_curriculums_for_course(cls, course_id):
        return Curriculum.objects.filter(curriculum_mappings__course=course_id)