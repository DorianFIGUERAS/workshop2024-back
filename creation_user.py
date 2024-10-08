from dotenv import load_dotenv
import requests
import os

load_dotenv()

API_KEY = os.getenv('API_KEY_FIREBASE')

def create_user(email, password):
    url = f'https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={API_KEY}'
    payload = {
        'email': email,
        'password': password,
        'returnSecureToken': True
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        user_data = response.json()
        return user_data['localId']
    else:
        print(f'Error creating user: {response.json().get("error", {}).get("message", "Unknown error")}')
        return None

# Example usage
# if __name__ == "__main__":
#     email = "dodofigue2205@gmail.com"
#     password = "password"
#     uid = create_user(email, password)
#     if uid:
#         print(f'User UID: {uid}')
#     else:
#         print('User creation failed')
