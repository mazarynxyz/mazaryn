# import json
# from asgiref.sync import async_to_sync
# from channels.layers import get_channel_layer
# from django.http import JsonResponse

# from notifications.serializers import NotificationSerializer
# from notifications.models import CustomNotification

# from .models import Profile, Relationship, Follow, Block
# from .utils import validate_email
# from .serializers import BlockSerializer, FollowSerializer, RegistrationSerializer, ProfileSerializer, ChangePasswordSerializer

# from rest_framework import status
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.generics import UpdateAPIView
# from rest_framework.authtoken.models import Token
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import generics, mixins
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.decorators import api_view, permission_classes, authentication_classes


# # Register
# # URL: https://<your-domain>/register/
# # @permission_classes([permissions.AllowAny, ])
# @api_view(['POST', ])
# def registration_view(request):
#     data = {}
#     email = request.data.get('email', '0').lower()
#     if validate_email(email) != None:
#         data['error_message'] = 'This email is already in use.'
#         data['response'] = 'Error'
#         return Response(data)

#     # username = request.data.get('username', '0')
#     # if validate_username(username) != None:
#     #     data['error_message'] = 'This username is already taken.'
#     #     data['response'] = 'Error'
#     #     return Response(data)

#     serializer = RegistrationSerializer(data=request.data)

#     if serializer.is_valid():
#         profile = serializer.save()
#         data['response'] = 'Succesfully registered'
#         data['email'] = profile.email
#         data['username'] = profile.username
#         data['id'] = profile.id
#         token = Token.objects.get(user=profile).key
#         data['token'] = token

#     else:
#         data = serializer.errors

#     return Response(data)


# # LOGIN
# # URL: http://<your-domain>/login/
# class LoginView(APIView):
#     '''Logins in an authenticated user with assigned tokens'''
#     authentication_classes = []
#     permission_classes = []

#     def post(self, request):
#         context = {}

#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         profile = authenticate(email=email, password=password)
#         if profile:
#             try:
#                 token = Token.objects.get(user=profile)
#             except Token.DoesNotExist:
#                 token = Token.objects.create(user=profile)
#             context['response'] = 'Successfully authenticated.'
#             context['id'] = profile.id
#             context['email'] = email.lower()
#             context['token'] = token.key
#         else:
#             context['response'] = 'Error'
#             context['error_message'] = 'Invalid credentials'

#         return Response(context)


# @api_view(['GET', ])
# @permission_classes([])
# @authentication_classes([])
# def does_account_exist_view(request):

#     email = request.GET['email'].lower()
#     data = {}
#     try:
#         profile = Profile.objects.get(email=email)
#         data['response'] = email
#     except Profile.DoesNotExist:
#         data['response'] = "Profile does not exist"
#     return Response(data)


# # class MyProfileView(APIView):
#     '''Returns logged in user profile instance.'''

#     def get_object(self, user):
#         try:
#             return Profile.objects.get(user=self.request.user)
#         except Profile.objects.DoesNotExist:
#             return Response({"error": "The profile does not exist"}, status=404)

#     def get(self, request, user=None):
#         instance = self.get_object(user)
#         serializer = ProfileSerializer(instance)
#         return Response(serializer.data)


# # Account update
# # URL: https://<your-domain>/profiles/myprofile/update/
# # Headers: Authorization: Token <token>
# @api_view(['PUT', ], )
# @permission_classes([IsAuthenticated, ])
# def update_profile_view(request):
#     '''Returns the logged in user profile with pre-data populated ready for update.'''
#     try:
#         profile = request.user
#     except Profile.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     serializer = ProfileSerializer(profile, data=request.data)
#     data = {}
#     if serializer.is_valid():
#         serializer.save()
#         data['response'] = 'Profile update success'
#         return Response(data=data)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ChangePasswordView(UpdateAPIView):

#     model = Profile
#     serializer_class = ChangePasswordSerializer
#     permission_classes = (IsAuthenticated,)
#     authentication_classes = (TokenAuthentication,)

#     def get_object(self, queryset=None):
#         obj = self.request.user
#         return obj

#     def update(self, request, *args, **kwargs):
#         object = self.get_object()
#         serializer = self.get_serializer(data=request.data)

#         if serializer.is_valid():
#             # Check old password
#             if not object.check_password(serializer.data.get("old_password")):
#                 return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

#             # confirm the new passwords match
#             new_password = serializer.data.get("new_password")
#             confirm_new_password = serializer.data.get("confirm_new_password")
#             if new_password != confirm_new_password:
#                 return Response({"new_password": ["New passwords must match"]}, status=status.HTTP_400_BAD_REQUEST)

#             # set_password also hashes the password that the user will get
#             object.set_password(serializer.data.get("new_password"))
#             object.save()
#             return Response({"response": "Successfully changed password"}, status=status.HTTP_200_OK)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)