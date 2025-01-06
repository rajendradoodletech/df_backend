from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, TemplateSerializer, CampaignSerializer, MessageSerializer, ContactSerializer, ContactGroupSerializer
from django.core.mail import send_mail
import random, csv, io, requests, time, json
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from .models import CustomUser, OTP, UserRole, Template, Campaign, Message, Contact, ContactGroup
import environ
env = environ.Env()

phone_number_id = env("PHONE_NUMBER_ID")
access_token = env("TOKEN")

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


class CreateCampaign(APIView):
    def post(self, request):
        file = request.FILES["file"]
        print(request.data)

        decoded_file = file.read().decode('utf-8')
        csv_reader = csv.reader(io.StringIO(decoded_file))
        contact_group = ContactGroup.objects.create(group_name=request.data.get("campaign_name"))

        campaign_name = request.data.get("campaign_name")
        template_name = request.data.get("template_name")
        template = Template.objects.get(id = request.data.get("template"))

        new_campaign = Campaign.objects.create(name=campaign_name, template=template, to_group=contact_group, status="Running")

        url = "https://graph.facebook.com/v21.0/219006681298210/messages"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        for contact in csv_reader:
            if contact[0] != "name":
                print(contact[1])
                name = contact[0]
                phone = contact[1]
                new_contact = Contact.objects.create(name = name, phone = phone, contact_group = contact_group
                )

                payload = {
                    "messaging_product": "whatsapp",
                    "to": phone,
                    "type": "template",
                    "template": {
                        "name": template.name,  # Your pre-approved template name
                        "language": {"code": template.language} 
                    }
                }
                
                msg_response = requests.post(url, headers=headers, json=payload)
                print(msg_response.__dict__)

        new_campaign.status = "Completed"
        new_campaign.save()
        return Response({"status: Success"})

class CreateTemplate(APIView):
    def post(self, request):
        print(request.FILES)

        data = request.data.dict()

        # Convert button fields (JSON strings) to Python objects
        for key, value in data.items():
            if 'buttons' in key:
                data[key] = json.loads(value)

        print(data)

        url = f"https://graph.facebook.com/v21.0/{phone_number_id}/message_templates"

        # Define the template payload
        template_name = data.get("templateName")
        template_name=template_name.replace(" ", "_")
        payload = {
            "name": template_name,
            "language": "en_US",
            "category": data.get("category"),
            "components": [
                {
                    "type": "HEADER",
                    "format": "TEXT",
                    "text": data.get("headerContent")
                },
                {
                    "type": "BODY",
                    "text": data.get("content")
                },
                {
                    "type": "FOOTER",
                    "text": data.get("footerContent")
                }
            ]
        }

        # Set the headers
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        # Send the POST request
        response = requests.post(url, headers=headers, data=json.dumps(payload))

        # Handle the response
        if response.status_code == 200:
            print("Message sent successfully:", response.json())
            new_template = Template()
            new_template.name = template_name
            new_template.language = data.get("language")
            new_template.category = data.get("category")
            new_template.template_type = data.get("templateType")
            new_template.body = data.get("content")
            new_template.headerType = data.get("headerType")
            if (data.get("headerContent") and data.get("headerContent") != "undefined"):
                new_template.header = data.get("headerContent")
            new_template.footer = data.get("footerContent")
            new_template.header_media = request.FILES.get("templateFile")
            if data.get("buttons[0]"):
                new_template.button1 = data.get("buttons[0]")
            if data.get("buttons[1]"):
                new_template.button2 = data.get("buttons[1]")
            if data.get("buttons[2]"):
                new_template.button3 = data.get("buttons[2]")
            if data.get("buttons[3]"):
                new_template.button4 = data.get("buttons[3]")
            new_template.save()
            return Response({"status": "Success"})
        else:
            print("Failed to send message:", response.status_code, response.json())


        return Response({"status": "Error"}, HTTP_400_BAD_REQUEST)
