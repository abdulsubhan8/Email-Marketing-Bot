from flask import Flask, request, jsonify
from flask import Flask, request, jsonify, redirect, url_for
import requests

app = Flask(__name__)

# Replace with your actual Facebook App ID and App Secret
FACEBOOK_APP_ID = '1235591774301394'
FACEBOOK_APP_SECRET = 'd70f93af8fcd1725f35924feea04e76f'
FACEBOOK_REDIRECT_URI = 'https://email-marketing-bot.vercel.app/facebook/callback'  # Replace with your actual redirect URI

@app.route('/')
def home():
    return 'Facebook Login Home. Frontend with Facebook button is served separately.'

# Endpoint to handle the Facebook token received from frontend
@app.route('/facebook/callback', methods=['POST'])
def facebook_callback():
    data = request.json
    access_token = data.get('token')

    if not access_token:
        return jsonify({"error": "No token provided"}), 400

    # Verify the access token with Facebook's API
    token_debug_url = f"https://graph.facebook.com/debug_token?input_token={access_token}&access_token={FACEBOOK_APP_ID}|{FACEBOOK_APP_SECRET}"
    token_response = requests.get(token_debug_url)
    token_info = token_response.json()

    if 'error' in token_info['data']:
        return jsonify({"error": "Invalid token"}), 400

    # Get user info from Facebook's Graph API
    user_info_url = f"https://graph.facebook.com/me?fields=id,name,email&access_token={access_token}"
    user_info_response = requests.get(user_info_url)
    user_info = user_info_response.json()

    if 'error' in user_info:
        return jsonify({"error": "Failed to retrieve user info"}), 400

    # Respond with user info or handle further logic (save to DB, etc.)
    return jsonify({
        "success": True,
        "message": f"Welcome, {user_info['name']}",
        "user": user_info
    })

if __name__ == '__main__':
    app.run(debug=True)
