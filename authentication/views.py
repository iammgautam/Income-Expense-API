
import jwt
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.models import User
from authentication.serializers import RegisterSerializer, emailVerificationSerializer
from authentication.utils import Utils
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
#class for registering account 
class RegistraterViews(generics.GenericAPIView):
    #using the custom serializer for api calls
    serializer_class = RegisterSerializer

    #if the api call is POST method...
    def post(self, request):
        
        #take the data given by user and serializer it in JSON format for API calls
        user = request.data
        serializer = self.serializer_class(data=user)
        #check if the user data is valid or not
        serializer.is_valid(raise_exception=True)
        #if it's valid then save it
        serializer.save()
        #take the data from the serializer and store it in user_data
        user_data = serializer.data

        #use 'user' variable to store email of the user.
        user = User.objects.get(email=user_data['email'])

        #token created manually and for ever refresh it add new JWT on tp of it and will also access the token.
        token = RefreshToken.for_user(user).access_token

        #get the current site domain name
        current_site = get_current_site(request).domain
        #reverse the link of the verifyEmail function
        relativeLink = reverse('email-verify')
        
        #get a overall link for verification of the email and store it in absurl
        absurl = 'http://' + current_site + relativeLink + "?token="+str(token)
        #email_body for the Email Sent to the registered User
        email_body = 'Hi, ' + user.username + ', use the below link to verify your Email.\n' + absurl
        data = {
            'email_body':email_body,
            'email_to':user.email,
            'email_subject':'Verify Your Email',
        }
        Utils.send_email(data)

        return Response(user_data, status = status.HTTP_201_CREATED)

#this class with verify the link that wwas sent in the email
class VerifyEmail(views.APIView):

    serializer_class = emailVerificationSerializer

    token_param_config = openapi.Parameter('token',in_=openapi.IN_QUERY, descriptor='Description', type=openapi.TYPE_STRING)
    @swagger_auto_schema(manual_parameters = [token_param_config])
    def get(self,request):
        #store the token from the link in the token variable
        token = request.GET.get('token')
        #if token is available
        try:
            #decode the token and confirm it with the SECRET_KEY of the 
            payload = jwt.decode(token, settings.SECRET_KEY,algorithms='HS256')
            #get the user by it user_id
            user = User.objects.get(id=payload['user_id'])
            #checks if the user is_verified or not
            if not user.is_verified:
                #if not then verify it
                user.is_verified = True
                #and save the user
                user.save()

            return Response({'email':'Successfully Activated'}, status=status.HTTP_200_OK)

        #if the token linked expired
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error':'Activation Linked Expired'}, status=status.HTTP_408_REQUEST_TIMEOUT)

        #if the token link is invalid
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error':'Invalid Token'}, status=status.HTTP_409_CONFLICT)
