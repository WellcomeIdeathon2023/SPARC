# app.py

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("jointplatform.html", title="Jinja and Flask")

if __name__ == "__main__":
    app.run(debug=True,port=8000)
    