from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, TemplateSerializer, CampaignSerializer, MessageSerializer, ContactSerializer, ContactGroupSerializer
from django.core.mail import send_mail
import random
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from .models import CustomUser, OTP, UserRole, Template, Campaign, Message, Contact, ContactGroup

# Create your views here.

def generateOTP(digits, chars):
    otp = ""
    for index in range(digits):
        otp+=random.choice(chars)

    return otp

class GetUserData(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            user_data = UserSerializer(request.user)
            return Response(user_data.data)
        return Response("Not loggedin")
    
class ForgorPassword(APIView):
    def get(self, request):
        email = request.GET.get("email")
        if email and CustomUser.objects.filter(email = email).exists():
            generated_otp = generateOTP(6,"1234567890")
            user = CustomUser.objects.get(email = email)
            OTP.objects.filter(user = user).delete()
            OTP.objects.create(otp = generated_otp, user = user)
            send_mail(
                'Reset password OTP',
                f'OTP - {generated_otp}',
                'rajendra@gmail.com',
                [email,],
                fail_silently=False,
            )
            return Response({"detail": "Check your mail to get the OTP"})
        return Response({"detail": "Email not found, Enter valid Email"}, HTTP_404_NOT_FOUND)
        
    
    def post(self, request):
        otp = request.data.get("otp")
        password = request.data.get("password")
        confirm_password = request.data.get("confirm_password")
        email = request.data.get("email")
        user = CustomUser.objects.get(email = email)

        otp_obj = OTP.objects.filter(user = user, otp = otp)
        if otp_obj.exists():
            user.set_password(password)
            user.save()
            return Response({"detail": "Password reset Successfull."})
        return Response({"detail": "Invalid OTP. Please enter valid OTP."}, HTTP_400_BAD_REQUEST)
    

class Register(APIView):
    def post(self, request):
        email = request.data.get("email")
        if CustomUser.objects.filter(email = email).exists():
            return Response({"detail": "Email ID already exists"}, HTTP_400_BAD_REQUEST)
        password = request.data.get("password")
        user_role = UserRole.objects.get(role = "Customer Admin")
        user = CustomUser.objects.create(email = email, role = user_role)
        user.set_password(password)
        user.save()

        return Response({"detail": "Registered Successfully"})
    
class TemplateListCreateView(generics.ListCreateAPIView):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    permission_classes = [permissions.AllowAny]
    
class TemplateDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    permission_classes = [permissions.AllowAny]
    
class CampaignListCreateView(generics.ListCreateAPIView):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    permission_classes = [permissions.AllowAny]
    
class CampaignDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    permission_classes = [permissions.AllowAny]
    
class MessageListCreateView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.AllowAny]
    
class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.AllowAny]
    
class ContactListCreateView(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.AllowAny]
    
class ContactDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.AllowAny]
    
class ContactGroupListCreateView(generics.ListCreateAPIView):
    queryset = ContactGroup.objects.all()
    serializer_class = ContactGroupSerializer
    permission_classes = [permissions.AllowAny]
    
class ContactGroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ContactGroup.objects.all()
    serializer_class = ContactGroupSerializer
    permission_classes = [permissions.AllowAny]