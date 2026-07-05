from flask import Flask
from routes.url_routes import url_bp

app = Flask(__name__)

app.register_blueprint(url_bp)

@app.route("/")
def home():
    return "Async URL Shortener API is Running!"


if __name__ == "__main__":
    app.run(debug=True)