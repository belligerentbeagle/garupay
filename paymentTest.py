import requests
import json
from datetime import datetime, timezone

url = "https://api-m.sandbox.paypal.com/v1/payments/payouts"


def settlepayment(amount, receipient_email):
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
            {
                "recipient_type": "EMAIL",
                "amount": {
                    "value": amount,
                    "currency": "SGD"
                },
                "note": "Thanks for your patronage!",
                "sender_item_id": "201403140001",
                "receiver": receipient_email,
                "notification_language": "en-US"
            },
        ]
    })
    headers = {
        'Content-Type': 'application/json',
        'PayPal-Request-Id': 'a47f6599-1923-44b8-9217-8af9c4fd8834',
        'Authorization': 'Basic QVpuWDdIMHNBZlpkdk1VVUViYkcwUG54TWpsbWJVdjB0NlBsSk5aT2lqWlJOZ1ZJQWx'
                         '6SEJoSFBCOUU3SWFlazM1dW9TQVBkWmkxM25OUkE6RUJfYU56UUw5dHNzeTE0Y3c0dVRWYzVnL'
                         'TE1N2dYeTBRVzEwb05VSmJ3WmJFX2Jza3psUlhDZTFmcm5hOU9RcnZncVd1VDV1NmgyeDZuSEI='
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


if __name__ == "__main__":
    amount = 20
    receipient_email = "sb-9o77p27200738@personal.example.com"
    settlepayment(amount, receipient_email)
