from django.db import models
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager  # ใช้ django-taggit สำหรับ tags

User = get_user_model()

class Note(models.Model):
    name = models.CharField(
        max_length=255,
        db_index=True,  # เพิ่ม index เพื่อค้นหาชื่อได้เร็วขึ้น
        help_text="ชื่อของโน้ต"
    )

    file_url = models.URLField(
        unique=True,
        help_text="URL ของไฟล์โน้ต (ห้ามว่าง)"
    )

    thumbnail_url = models.URLField(
        blank=True,
        null=True,
        help_text="URL ของ thumbnail (ถ้ามี)"
    )

    account = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notes",
        db_index=True,
        help_text="เจ้าของโน้ต"
    )

    tags = TaggableManager(
        help_text="แท็กสำหรับค้นหาและจัดกลุ่มโน้ต"
    )  # ใช้ django-taggit สำหรับแท็ก

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text="เวลาสร้าง"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="เวลาอัปเดตล่าสุด"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Note"
        verbose_name_plural = "Notes"
        indexes = [
            models.Index(fields=['name']),  # Index เพื่อค้นหาตามชื่อ
            models.Index(fields=['account', 'created_at']),  # ค้นหาโน้ตตาม account + วันที่สร้าง
        ]

    def __str__(self):
        return f"{self.name} - {self.account.username}"

    @classmethod
    def search(cls, query):
        """ ค้นหาโน้ตตามชื่อหรือแท็ก """
        return cls.objects.filter(
            models.Q(name__icontains=query) |
            models.Q(tags__name__icontains=query)  # ค้นหาตามแท็กแบบ ManyToMany
        ).distinct()
