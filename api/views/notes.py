from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from ..models import Note, Course
from django.contrib.auth.decorators import login_required


# 🎯 GET /api/notes/ → Fetch all notes
# 🎯 POST /api/notes/ → Create a new note
@method_decorator(csrf_exempt, name="dispatch")
class NoteListCreateView(View):
    def get(self, request):
        """ Fetch all notes, ordered by creation date. """
        notes = Note.objects.all().order_by("-created_at")
        notes_data = [
            {
                "id": note.id,
                "name": note.name,
                "file_url": note.file_url,
                "course_id": note.course.id,
                "course_name": note.course.name,
                "user": note.user.username,
                "tags": note.tags,
                "created_at": note.created_at,
                "updated_at": note.updated_at,
            }
            for note in notes
        ]
        return JsonResponse({"notes": notes_data})

    def post(self, request):
        """ Create a new note. Requires JSON body with name, file_url, course_id, and optional tags. """
        try:
            data = json.loads(request.body)
            course = get_object_or_404(Course, id=data["course_id"])
            user = request.user  # Requires authentication

            new_note = Note.objects.create(
                name=data["name"],
                file_url=data["file_url"],
                course=course,
                user=user,
                tags=data.get("tags", ""),
            )

            return JsonResponse(
                {"note": {"id": new_note.id, "name": new_note.name, "file_url": new_note.file_url}},
                status=201,
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


# 🎯 GET /api/notes/<id>/ → Get a single note
# 🎯 PUT /api/notes/<id>/ → Update a note
# 🎯 DELETE /api/notes/<id>/ → Delete a note
@method_decorator(csrf_exempt, name="dispatch")
class NoteDetailView(View):
    def get(self, request, pk):
        """ Retrieve a single note by its ID. """
        note = get_object_or_404(Note, id=pk)
        note_data = {
            "id": note.id,
            "name": note.name,
            "file_url": note.file_url,
            "course_id": note.course.id,
            "course_name": note.course.name,
            "user": note.user.username,
            "tags": note.tags,
            "created_at": note.created_at,
            "updated_at": note.updated_at,
        }
        return JsonResponse(note_data)

    def put(self, request, pk):
        """ Update an existing note. Requires JSON body with updated fields. """
        try:
            data = json.loads(request.body)
            note = get_object_or_404(Note, id=pk)
            note.name = data.get("name", note.name)
            note.file_url = data.get("file_url", note.file_url)
            note.tags = data.get("tags", note.tags)

            if "course_id" in data:
                note.course = get_object_or_404(Course, id=data["course_id"])

            note.save()
            return JsonResponse({"message": "Note updated successfully!"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def delete(self, request, pk):
        """ Delete a note by its ID. """
        note = get_object_or_404(Note, id=pk)
        note.delete()
        return JsonResponse({"message": "Note deleted successfully!"}, status=200)


# 🎯 GET /api/notes/search/?q=example&field=name → Search notes
class NoteSearchView(View):
    def get(self, request):
        """ Search notes by name, tags, or course. Requires query parameter 'q' and optional 'field'. """
        query = request.GET.get("q", "")
        field = request.GET.get("field", "name")  # Default: Search by name

        if not query:
            return JsonResponse({"error": "Missing query parameter 'q'"}, status=400)

        allowed_fields = ["name", "tags", "course__name"]
        if field not in allowed_fields:
            return JsonResponse({"error": f"Invalid search field '{field}'"}, status=400)

        filter_kwargs = {f"{field}__icontains": query}
        notes = Note.objects.filter(**filter_kwargs)

        notes_data = [
            {
                "id": note.id,
                "name": note.name,
                "file_url": note.file_url,
                "course_id": note.course.id,
                "course_name": note.course.name,
                "user": note.user.username,
                "tags": note.tags,
                "created_at": note.created_at,
                "updated_at": note.updated_at,
            }
            for note in notes
        ]

        return JsonResponse({"results": notes_data})
