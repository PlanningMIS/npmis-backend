# views.py
from dj_rest_auth.views import LoginView as RESTLoginView
from .serializers import JWTSerializer


class LoginView(RESTLoginView):
    serializer_class = JWTSerializer
