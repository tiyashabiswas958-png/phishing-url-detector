from flask import Flask, render_template, request
import pickle
import re

app = Flask(__name__)

vector = pickle.load(open("vectorizer.pkl", "rb"))
model = pickle.load(open("phishing.pkl", "rb"))

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]

        cleaned_url = re.sub(r"^https?://(www\.)?", "", url)

        predict = model.predict(vector.transform([cleaned_url]))[0]

        if predict == "bad":
            predict = "This is a Phishing website !!"
        else:
            predict = "This is a Safe website !!"

        return render_template("index.html", predict=predict)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)