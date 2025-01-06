import requests, json

access_token = "EAAQzrLYZAd5wBOxRIYXuaWXgf2X7ZBwounf78RJeTZCd407ABHpe0BTpKZCF1VQK6qZAAqavt67RDKGQsIEwnprr067NxRgyqonjGBFSxFyGc99dcdnsOlkR4qHvhehLCDezCcLT4uPTqZAtlZBLwE1a7xa7p84EE5Lkuh1zzQY0qteadnakSQb56Qm7CCFB8H6WZAVHyuLlJIbFhb8pqTmmZAFCZADEgZD"
phone_number_id = "235724502953428"


# url = f"https://graph.facebook.com/v21.0/{phone_number_id}/message_templates"

# # Define the template payload
# payload = {
#     "name": "otp",
#     "language": "en_US",
#     "category": "MARKETING",
#     "components": [
#         {
#             "type": "HEADER",
#             "format": "TEXT",
#             "text": "Order Confirmation"
#         },
#         {
#             "type": "BODY",
#             "text": "Hi, your order has been confirmed. It will be delivered soon."
#         },
#         {
#             "type": "FOOTER",
#             "text": "Thank you for shopping with us!"
#         }
#     ]
# }

# # Set the headers
# headers = {
#     "Authorization": f"Bearer {access_token}",
#     "Content-Type": "application/json"
# }

# # Send the POST request
# response = requests.get(url, headers=headers)

# # Print the response
# if response.status_code == 200:
#     print("Template created successfully:", response.json())
# else:
#     print("Failed to create template:", response.status_code, response.json())


# url = "https://graph.facebook.com/v21.0/219006681298210/messages"

# # # Data payload
# data = {
#     "messaging_product": "whatsapp",
#     "to": "917416334738",  # Replace with the target phone number
#     "type": "template",
#     "template": {
#         "name": "order_status",  # Replace with the actual template name
#         "language": {
#             "code": "en_US"  # Replace with the desired language code
#         }
#     }
# }

# headers = {
#     "Authorization": f"Bearer {access_token}",
#     "Content-Type": "application/json"
# }

# # Send POST request
# response = requests.post(url, headers=headers, data=json.dumps(data))

# # Handle the response
# if response.status_code == 200:
#     print("Message sent successfully:", response.json())
# else:
#     print("Failed to send message:", response.status_code, response.json())

# url = f"https://graph.facebook.com/v21.0/me/businesses?access_token={access_token}"

# # Set headers
# headers = {
#     "Authorization": f"Bearer {access_token}"
# }

# # Send GET request
# response = requests.get(url, headers=headers)

# print(response.json())

# url = f'https://graph.facebook.com/v21.0/{phone_number_id}/message_templates'

# # Set headers
# headers = {
#     "Authorization": f"Bearer {access_token}"
# }

# # Send GET request
# response = requests.get(url, headers=headers)

# # Handle response
# if response.status_code == 200:
#     templates = response.json().get("data", [])
#     print("Message Templates:")
#     for template in templates:
#         print(f"- Name: {template['name']}, Status: {template['status']}, Language: {template['language']}")
# else:
#     print("Failed to retrieve templates:", response.status_code, response.json())


url = f"https://graph.facebook.com/v21.0/{phone_number_id}/message_templates?access_token={access_token}"

headers = {
    "Authorization": f"Bearer {access_token}"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print(response.json())
else:
    print(response.status_code, response.json())

# url = f"https://graph.facebook.com/v21.0/{phone_number_id}/whatsapp_business_accounts"

# headers = {
#     "Authorization": f"Bearer {access_token}"
# }

# response = requests.get(url, headers=headers)

# if response.status_code == 200:
#     print("WhatsApp Business Accounts:", response.json())
# else:
#     print("Failed to retrieve WhatsApp Business Accounts:", response.status_code, response.json())


# url = f"https://graph.facebook.com/v20.0/1521042571411729/whatsapp_business_accounts?access_token={access_token}"

# response = requests.get(url)

# if response.status_code == 200:
#     print("WhatsApp Business Accounts:", response.json())
# else:
#     print("Failed to retrieve WhatsApp Business Accounts:", response.status_code, response.json())
