from celery import shared_task
import requests
import logging

AUTH_SERVICE_URL = "http://auth:8000/api/auth/token/validate/"

@shared_task
def verify_token(token):
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(
            AUTH_SERVICE_URL, 
            json={"token": token},
            headers=headers
        )
        
        logging.info(f"Auth service response: Status={response.status_code}, Body={response.text}")
        
        if response.status_code == 200:
            return response.json()
        
        logging.error(f"Token validation failed: {response.status_code}, {response.text}")
        return None
    except Exception as e:
        logging.error(f"Error in verify_token task: {str(e)}")
        return None