from flask import Flask, render_template
from socket import gethostname


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    if 'liveconsole' not in gethostname():
        app.run(debug=True)
