from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

# Load model
model = pickle.load(open("model.pkl", "rb"))

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    try:
        data = {
            "airline": request.form["airline"],
            "source_city": request.form["source_city"],
            "departure_time": request.form["departure_time"],
            "stops": request.form["stops"],
            "arrival_time": request.form["arrival_time"],
            "destination_city": request.form["destination_city"],
            "class": request.form["class"],
            "duration": float(request.form["duration"]),
            "days_left": int(request.form["days_left"])
        }

        input_df = pd.DataFrame([data])

        prediction = model.predict(input_df)[0]

        return render_template(
            "index.html",
            prediction_text=f"Predicted Flight Price: ₹ {round(prediction,2)}"
        )

    except Exception as e:
        return render_template(
            "index.html",
            prediction_text="Error in input. Please check values."
        )


if __name__ == "__main__":
    app.run(debug=True)
