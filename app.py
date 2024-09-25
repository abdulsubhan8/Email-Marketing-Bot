from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Facebook Graph API URL for user profile info
FACEBOOK_GRAPH_API_URL = 'https://graph.facebook.com/me'

# Facebook App Secret (replace with your credentials)
FACEBOOK_APP_SECRET = 'YOUR_APP_SECRET'

@app.route('/facebook_login', methods=['POST'])
def facebook_login():
    # Get the access token from the frontend
    data = request.json
    access_token = data.get('access_token')

    if access_token:
        # Verify the access token and get user profile data
        user_info_url = f'{FACEBOOK_GRAPH_API_URL}?fields=id,name,email&access_token={access_token}'
        response = requests.get(user_info_url)
        user_data = response.json()

        if 'error' in user_data:
            return jsonify({'error': 'Invalid access token'}), 400

        return jsonify(user_data), 200
    else:
        return jsonify({'error': 'Access token is missing'}), 400

if __name__ == '__main__':
    app.run(debug=True)
