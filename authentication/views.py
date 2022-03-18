from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render
from django.urls import reverse

from rest_framework import generics, status
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from authentication.models import User
from authentication.serializers import RegisterSerializer
from authentication.utils import Utils

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

class VerifyEmail(generics.GenericAPIView):
    def get(self):
        pass
