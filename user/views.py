from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import *


class LoginView(APIView):
    """
    LoginView handles POST requests for user authentication.

    """
    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            
            user = authenticate(username=username, password=password)
            if user:

                # Generate a refresh token for the authenticated user
                refresh = RefreshToken.for_user(user)

                # Return the access token in the response
                return Response({"status":True,
                    'access_token': str(refresh.access_token),
                })
            else:
                return Response({'Status':False,'error': 'Invalid credentials'}, 
                                status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print(e)
            return Response({'Status':False,'Message':'Something unexpected occured'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProjectUserCreate(APIView):
    """
    ProjectUserCreate handles POST requests to create a new project user.

    """
    def post(self, request):
        try:
            serializer = ProjectUserSerializer(data=request.data)

            # Check if the provided data is valid
            if serializer.is_valid():
                serializer.save()
                return Response({'Status':True,"Message":"User created successfully"},
                                status=status.HTTP_201_CREATED)
            return Response({'Status':False,"Message":serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'Status':False,'Message':'Something unexpected occured'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)