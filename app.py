from flask import Flask, render_template, request
import os
import jsonify
import requests
import joblib
import numpy as np
import sklearn

TEMPLATE_DIR = os.path.abspath("./templates")
STATIC_DIR = os.path.abspath("./static")

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
model = joblib.load(open("ParkinsonsDiseaseModel.joblib", "rb"))
print("Model loaded successfully")


@app.route("/", methods=["GET", "POST"])
def Home():
    return render_template("index.html")


@app.route("/predict", methods=["POST", "GET"])
def predict():
    if request.method == "POST":
        MDVP_F0 = float(request.form["MDVP:Fo(Hz)"])
        MDVP_Fhi = float(request.form["MDVP:Fhi(Hz)"])
        MDVP_Flo = float(request.form["MDVP:Flo(Hz)"])
        MDVP_Jitter_per = float(request.form["MDVP:Jitter(%)"])
        MDVP_Jitter_abs = float(request.form["MDVP:Jitter(Abs)"])
        MDVP_RAP = float(request.form["MDVP:RAP"])
        MDVP_PPQ = float(request.form["MDVP:PPQ"])
        Jitter_DDP = float(request.form["Jitter:DDP"])
        MDVP_Shimmer = float(request.form["MDVP:Shimmer"])
        MDVP_Shimmer_dB = float(request.form["MDVP:Shimmer(dB)"])
        Shimmer_APQ3 = float(request.form["Shimmer:APQ3"])
        Shimmer_APQ5 = float(request.form["Shimmer:APQ5"])
        MDVP_APQ = float(request.form["MDVP:APQ"])
        Shimmer_DDA = float(request.form["Shimmer:DDA"])
        NHR = float(request.form["NHR"])
        HNR = float(request.form["HNR"])
        RPDE = float(request.form["RPDE"])
        DFA = float(request.form["DFA"])
        spread1 = float(request.form["spread1"])
        spread2 = float(request.form["spread2"])
        D2 = float(request.form["D2"])
        PPE = float(request.form["PPE"])

        predict = model.predict(
            [
                [
                    MDVP_F0,
                    MDVP_Fhi,
                    MDVP_Flo,
                    MDVP_Jitter_per,
                    MDVP_Jitter_abs,
                    MDVP_RAP,
                    MDVP_PPQ,
                    Jitter_DDP,
                    MDVP_Shimmer,
                    MDVP_Shimmer_dB,
                    Shimmer_APQ3,
                    Shimmer_APQ5,
                    MDVP_APQ,
                    Shimmer_DDA,
                    NHR,
                    HNR,
                    RPDE,
                    DFA,
                    spread1,
                    spread2,
                    D2,
                    PPE,
                ]
            ]
        )

        output = round(predict[0])
        if output == 0:
            return render_template(
                "index.html", prediction_text="NO DETECTION of Parkinson's Disease"
            )
        else:
            return render_template(
                "index.html", prediction_text="Parkinson's Disease DETECTED"
            )
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
