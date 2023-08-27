# import requests
# import json

# url = "https://api.ocbc.com:8243/transactional/paynow/1.0"
# # JSON data with the required parameters
# data = {
#     "Amount": 2.00,
#     "ProxyType": "MSISDN",
#     "ProxyValue": "+6591234691", #Ruiheng: +6597862985
#     "FromAccountNo": "628499451001"
# }

# headers = {
#     "Content-Type": "application/json"
# }

# # Convert the JSON data to a string
# json_data = json.dumps(data)

# response = requests.post(url, data=json_data, headers=headers)

# # Parse the JSON response
# parsed_response = json.loads(response.text)

# # Display the JSON response nicely with indentation
# formatted_response = json.dumps(parsed_response, indent=4)
# print(response)
# print(formatted_response)

##PAYPAL

import requests
import json
from datetime import datetime, timezone

url = "https://api-m.sandbox.paypal.com/v1/payments/payouts"

def main(receiptient_number, amount):
    ##Process

    # Get the current timestamp in ISO 8601 format with timezone information
    current_timestamp = datetime.now(timezone.utc).isoformat()
    senderbatchid = "Payouts_" + current_timestamp
    payload = json.dumps({
    "sender_batch_header": {
        "sender_batch_id": senderbatchid,
        "email_subject": "You have a payout!",
        "email_message": "You have received a payout! Thanks for using our service!"
    },
    "items": [
        # {
        # "recipient_type": "EMAIL",
        # "amount": {
        #     "value": "10.00",
        #     "currency": "SGD"
        # },
        # "note": "Thanks for your patronage!",
        # "sender_item_id": "201403140001",
        # "receiver": "sb-9o77p27200738@personal.example.com",
        # "notification_language": "en-US"
        # },
        {
        "recipient_type": "PHONE",
        "amount": {
            "value": amount,
            "currency": "SGD"
        },
        "note": "Thanks for your support!",
        "sender_item_id": "201403140002",
        "receiver": receiptient_number,
        }
    ]
    })
    headers = {
    'Content-Type': 'application/json',
    'PayPal-Request-Id': 'a47f6599-1923-44b8-9217-8af9c4fd8834',
    'Authorization': 'Basic QVpuWDdIMHNBZlpkdk1VVUViYkcwUG54TWpsbWJVdjB0NlBsSk5aT2lqWlJOZ1ZJQWx6SEJoSFBCOUU3SWFlazM1dW9TQVBkWmkxM25OUkE6RUJfYU56UUw5dHNzeTE0Y3c0dVRWYzVnLTE1N2dYeTBRVzEwb05VSmJ3WmJFX2Jza3psUlhDZTFmcm5hOU9RcnZncVd1VDV1NmgyeDZuSEI='
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

if __name__ == "__main__":
    main(receiptient_number, amount)