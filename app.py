from flask import Flask, jsonify, request
import post_to_marketplace
import scrape_listings

app = Flask(__name__)

# Add your endpoints here

@app.route('/scrape_listings', methods=['GET'])
def scrape_listings_fn():
    result = scrape_listings.scrape_listings() 
    return jsonify(result)

@app.route('/post_to_marketplace', methods=['GET']) # Change method to POST later
def post_fb_fn():
    # You can extract data from the request if needed
    data = request.args
    username = data.get('username')
    password = data.get('password')

    result = post_to_marketplace.post_fb(username, password)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
