from flask import Flask, request, jsonify, render_template
import os
from supabase import create_client
from dotenv import load_dotenv
import main
import json5

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_API")
supabase = create_client(url, key)

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/v1/WeatherRecognitionModel/', methods=['POST'])
async def weather_recognition_model():
    data = json5.loads(request.data.decode('utf-8'))

    if "email" not in data:
        return jsonify({"error": "Missing 'email' field"}), 400
    if "password" not in data:
        return jsonify({"error": "Missing 'password' field"}), 400
    if "image_url" not in data:
        return jsonify({"error": "Missing 'image_url' field"}), 400

    email = data["email"]
    image_url = data["image_url"]
    password = data["password"]

    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        }).model_dump()

        if not response["user"]:
            return jsonify({"error": "Invalid credentials"}), 401

        pred = main.makePrediction(image_url)
        return jsonify({"Message": "Success", "Prediction": pred})
    except Exception as e:
        return jsonify({"message": "error occurred", "error": str(e)}), 500


# @app.route('/api/v1/signinwithemail/', methods=['POST'])
# def signinwithemail():
#     data = json5.loads(request.get_data().decode('utf8')))
#     if 'email' not in data:
#         return jsonify({"error": "Missing 'email' field"}), 400
#     if 'password' not in data:
#         return jsonify({"error": "Missing 'password' field"}), 400

#     email = data['email']
#     password = data['password']


@app.route('/api/v1/signup/', methods=['POST'])
def signup():
    data = json5.loads(request.get_data().decode('utf-8'))

    if 'email' not in data:
        return jsonify({"error": "Missing 'email' field"}), 400
    if 'password' not in data:
        return jsonify({"error": "Missing 'password' field"}), 400

    email = data['email']
    password = data['password']

    response = supabase.auth.sign_up({
        "email": email,
        "password": password
    })

    return jsonify(dict(response.model_dump_json()))


@app.route('/api/v1/signupwithphone', methods=['POST'])
def signupwithphone():
    print(request.data.decode('utf-8'))
    data = json5.loads(request.get_data().decode('utf8'))
    if 'phone' not in data:
        return jsonify({"error": "Missing 'phone' field"}), 400
    if 'password' not in data:
        return jsonify({"error": "Missing 'password' field"}), 400
    phone = data['phone']
    password = data['password']

    response = supabase.auth.sign_up({
        "phone": phone,
        "password": password
    })

    return jsonify(dict(response.model_dump_json()))


@app.route('/api/v1/signin/', methods=['POST'])
async def signin():
    data = json5.loads(request.data.decode('utf-8'))
    if 'email' not in data:
        return jsonify({"error": "Missing 'email' field"}), 400
    if 'password' not in data:
        return jsonify({"error": "Missing 'password' field"}), 400
    email = data['email']
    password = data['password']
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        return jsonify({"Message": "Success", "Response": response.model_dump()})

        """
                {
                    "session": {
                        "access_token": "",
                        "expires_at": 1726216278,
                        "expires_in": 3600,
                        "provider_refresh_token": null,
                        "provider_token": null,
                        "refresh_token": "RvBF9fDmVl6lL-OsX0f_2A",
                        "token_type": "bearer",
                        "user": {
                            "action_link": null,
                            "app_metadata": {
                                "provider": "email",
                                "providers": [
                                    "email"
                                ]
                            },
                            "aud": "authenticated",
                            "confirmation_sent_at": "2024-09-13T07:11:09.845047Z",
                            "confirmed_at": "2024-09-13T07:11:31.446348Z",
                            "created_at": "2024-09-13T07:11:09.811336Z",
                            "email": "tirthrdesai05@gmail.com",
                            "email_change_sent_at": null,
                            "email_confirmed_at": "2024-09-13T07:11:31.446348Z",
                            "factors": null,
                            "id": "556c7615-ea88-4b44-a82e-64d855e6502e",
                            "identities": [{
                                "created_at": "2024-09-13T07:11:09.832794Z",
                                "id": "556c7615-ea88-4b44-a82e-64d855e6502e",
                                "identity_data": {
                                    "email": "tirthrdesai05@gmail.com",
                                    "email_verified": false,
                                    "phone_verified": false,
                                    "sub": "556c7615-ea88-4b44-a82e-64d855e6502e"
                                },
                                "identity_id": "e2efb8dd-abf1-4f09-8247-f3bf90fcab37",
                                "last_sign_in_at": "2024-09-13T07:11:09.832738Z",
                                "provider": "email",
                                "updated_at": "2024-09-13T07:11:09.832794Z",
                                "user_id": "556c7615-ea88-4b44-a82e-64d855e6502e"
                            }],
                            "invited_at": null,
                            "is_anonymous": false,
                            "last_sign_in_at": "2024-09-13T07:31:18.864448Z",
                            "new_email": null,
                            "new_phone": null,
                            "phone": "",
                            "phone_confirmed_at": null,
                            "recovery_sent_at": null,
                            "role": "authenticated",
                            "updated_at": "2024-09-13T07:31:18.867777Z",
                            "user_metadata": {
                                "email": "tirthrdesai05@gmail.com",
                                "email_verified": false,
                                "phone_verified": false,
                                "sub": "556c7615-ea88-4b44-a82e-64d855e6502e"
                            }
                        }
                    },
                    "user": {
                        "action_link": null,
                        "app_metadata": {
                            "provider": "email",
                            "providers": [
                                "email"
                            ]
                        },
                        "aud": "authenticated",
                        "confirmation_sent_at": "2024-09-13T07:11:09.845047Z",
                        "confirmed_at": "2024-09-13T07:11:31.446348Z",
                        "created_at": "2024-09-13T07:11:09.811336Z",
                        "email": "tirthrdesai05@gmail.com",
                        "email_change_sent_at": null,
                        "email_confirmed_at": "2024-09-13T07:11:31.446348Z",
                        "factors": null,
                        "id": "556c7615-ea88-4b44-a82e-64d855e6502e",
                        "identities": [{
                            "created_at": "2024-09-13T07:11:09.832794Z",
                            "id": "556c7615-ea88-4b44-a82e-64d855e6502e",
                            "identity_data": {
                                "email": "tirthrdesai05@gmail.com",
                                "email_verified": false,
                                "phone_verified": false,
                                "sub": "556c7615-ea88-4b44-a82e-64d855e6502e"
                            },
                            "identity_id": "e2efb8dd-abf1-4f09-8247-f3bf90fcab37",
                            "last_sign_in_at": "2024-09-13T07:11:09.832738Z",
                            "provider": "email",
                            "updated_at": "2024-09-13T07:11:09.832794Z",
                            "user_id": "556c7615-ea88-4b44-a82e-64d855e6502e"
                        }],
                        "invited_at": null,
                        "is_anonymous": false,
                        "last_sign_in_at": "2024-09-13T07:31:18.864448Z",
                        "new_email": null,
                        "new_phone": null,
                        "phone": "",
                        "phone_confirmed_at": null,
                        "recovery_sent_at": null,
                        "role": "authenticated",
                        "updated_at": "2024-09-13T07:31:18.867777Z",
                        "user_metadata": {
                            "email": "tirthrdesai05@gmail.com",
                            "email_verified": false,
                            "phone_verified": false,
                            "sub": "556c7615-ea88-4b44-a82e-64d855e6502e"
                        }
                    }
                }
            """

    except Exception as e:
        return jsonify({"error": str(e)}), 401


if __name__ == '__main__':
    os.system('cls')
    app.run(debug=True, port=3000)
