from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Replace with your actual Facebook App ID and App Secret
FACEBOOK_APP_ID = '1235591774301394'
FACEBOOK_APP_SECRET = 'd70f93af8fcd1725f35924feea04e76f'

@app.route('/')
def index():
    return render_template('fblogin.html')  # Serve the frontend page
    
FB_GRAPH_API_URL = "https://graph.facebook.com/v12.0"

@app.route('/instagram-data', methods=['GET', 'POST'])
def instagram_data():
    if request.method == 'GET':
        # Render a template for GET requests
        return render_template('login.html')
    
    if request.method == 'POST':
        try:
            access_token = request.json.get('access_token')
    
            if not access_token:
                return jsonify({"error": "Access token is required"}), 400
    
            pages_url = f"{FB_GRAPH_API_URL}/me/accounts"
            pages_response = requests.get(pages_url, params={'access_token': access_token})
    
            if pages_response.status_code != 200:
                return jsonify({"error": "Failed to fetch Facebook Pages"}), pages_response.status_code
    
            pages_data = pages_response.json()
            instagram_business_id = None
            for page in pages_data.get('data', []):
                if 'instagram_business_account' in page:
                    instagram_business_id = page['instagram_business_account']['id']
                    break
    
            if not instagram_business_id:
                return jsonify({"error": "No Instagram Business Account linked to Facebook Pages"}), 404
    
            instagram_media_url = f"{FB_GRAPH_API_URL}/{instagram_business_id}/media"
            media_response = requests.get(instagram_media_url, params={'access_token': access_token})
    
            if media_response.status_code != 200:
                return jsonify({"error": "Failed to fetch Instagram Media"}), media_response.status_code
    
            media_data = media_response.json()
    
            return jsonify({
                "instagram_media": media_data,
                "message": "Successfully retrieved Instagram media."
            }), 200
    
        except Exception as e:
            return jsonify({"error": str(e)}), 500


        
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

    # Respond with user info
    return jsonify({
        "success": True,
        "message": f"Welcome, {user_info['name']}",
        "user": user_info
    })

if __name__ == '__main__':
    app.run(debug=True)


