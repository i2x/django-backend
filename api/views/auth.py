import requests
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

# ✅ Helper Function to Generate Tokens
def generate_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }

# ✅ Google
def get_user_from_google_token(token):
    google_url = f"https://www.googleapis.com/oauth2/v3/tokeninfo?id_token={token}"
    response = requests.get(google_url)

    if response.status_code != 200:
        return None

    return response.json()


# ✅ Google Login API with Profile Picture
class GoogleLoginView(APIView):
    def post(self, request):
        token = request.data.get('token')
        data = get_user_from_google_token(token)

        if not data:
            return Response({'error': 'Invalid Google token'}, status=400)

        name = data.get('name')  # ✅ Get the user's name
        picture = data.get('picture')  # ✅ Get the profile picture URL

        if not name:
            return Response({'error': 'Name not found in Google response'}, status=400)

        user, created = User.objects.get_or_create(
            username=name,
            defaults={'email': f"{name.replace(' ', '').lower()}@example.com"}  # Use a dummy email
        )

        if created:
            user.role = 'member'
            user.save()

        tokens = generate_tokens_for_user(user)

        return Response({
            'refresh': tokens["refresh"],
            'access': tokens["access"],
            'user': {
                'id': user.id,
                'username': user.username,  # ✅ Use name instead of email
                'role': user.role,
                'picture': picture  # ✅ Return the Google profile picture
            }
        })
