from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from api.models import Note, Course
from rest_framework.permissions import AllowAny


class NoteBaseView(APIView):
    """ Base View with authentication and common helper methods """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def _serialize_note(self, note):
        """ Helper method to serialize note data """
        return {
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

    def _get_note_or_403(self, request, pk):
        """ Helper method to get a note and check ownership """
        note = get_object_or_404(Note, id=pk)
        if note.user != request.user:
            return Response({"error": "You do not have permission for this note."}, status=status.HTTP_403_FORBIDDEN)
        return note


class NoteListCreateView(NoteBaseView):
    """ Handles listing and creating notes """

    def get(self, request):
        """ Fetch only the notes of the logged-in user """
        notes = Note.objects.filter(user=request.user).order_by("-created_at")
        return Response({"notes": [self._serialize_note(note) for note in notes]}, status=status.HTTP_200_OK)

    def post(self, request):
        """ Create a new note (Only for logged-in users) """
        data = request.data
        course = get_object_or_404(Course, id=data["course_id"])

        new_note = Note.objects.create(
            name=data["name"],
            file_url=data["file_url"],
            course=course,
            user=request.user,
            tags=data.get("tags", ""),
        )

        return Response({"note": self._serialize_note(new_note)}, status=status.HTTP_201_CREATED)


class NoteDetailView(NoteBaseView):
    """ Handles retrieving, updating, and deleting a note """

    def get(self, request, pk):
        """ Retrieve a single note (Only owner can view) """
        note = self._get_note_or_403(request, pk)
        return Response(self._serialize_note(note))

    def put(self, request, pk):
        """ Update a note (Only owner can update) """
        note = self._get_note_or_403(request, pk)
        data = request.data

        # Update note fields
        note.name = data.get("name", note.name)
        note.file_url = data.get("file_url", note.file_url)
        note.tags = data.get("tags", note.tags)

        if "course_id" in data:
            note.course = get_object_or_404(Course, id=data["course_id"])

        note.save()
        return Response({"message": "Note updated successfully!", "note": self._serialize_note(note)}, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        """ Delete a note (Only owner can delete) """
        note = self._get_note_or_403(request, pk)
        note.delete()
        return Response({"message": "Note deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)


class NoteSearchView(NoteBaseView):
    """ Handles public searching of notes (All users can search) """
    
    permission_classes = [AllowAny]  # 🔥 Make search public

    def get(self, request):
        """ Public search for notes across all users """
        query = request.GET.get("q", "").strip()
        field = request.GET.get("field", "name")

        if not query:
            return Response({"error": "Missing query parameter 'q'"}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ Only allow searching in these fields to prevent SQL injection
        allowed_fields = ["name", "tags", "course__name","user__username"]
        if field not in allowed_fields:
            return Response({"error": f"Invalid search field '{field}'"}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ Perform search across all users' notes (removed user filter)
        filter_kwargs = {f"{field}__icontains": query}
        notes = Note.objects.filter(**filter_kwargs)

        return Response({"results": [self._serialize_note(note) for note in notes]}, status=status.HTTP_200_OK)
