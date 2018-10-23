import requests
import kasak_params as kp

def post(message, image_url = None):
    payload = {"text": "{}".format(message)}
    if image_url is not None:
        payload['attachments'] = [{'fallback':'Overview of this weeks business.', 'image_url': image_url}]
    r = requests.post(url = kp.slack_webhook_url, json = payload)
    print(r.status_code, r.text)
