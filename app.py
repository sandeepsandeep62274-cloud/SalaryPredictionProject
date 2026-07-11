from flask import Flask, render_template, request, send_file
import pandas as pd
import joblib
import os

from reportlab.pdfgen import canvas

app = Flask(__name__)

model = joblib.load("salary_model.pkl")


# Create history file automatically

if not os.path.exists("history.csv"):

    df = pd.DataFrame(
        columns=[
            "Name",
            "Age",
            "Education",
            "Experience",
            "Salary"
        ]
    )

    df.to_csv(
        "history.csv",
        index=False
    )


@app.route('/')
def home():

    history = pd.read_csv("history.csv")

    total_predictions = len(history)

    if len(history) > 0:

        highest_salary = history["Salary"].max()

        average_salary = round(
            history["Salary"].mean(),
            2
        )

    else:

        highest_salary = 0
        average_salary = 0

    return render_template(
        "index.html",
        history=history.to_dict(
            orient="records"
        ),
        total_predictions=total_predictions,
        highest_salary=highest_salary,
        average_salary=average_salary
    )


@app.route('/predict', methods=['POST'])
def predict():

    global last_pdf

    name = request.form["name"]

    age = request.form["age"]

    education = request.form["education"]

    skills = request.form["skills"]

    experience = float(
        request.form["experience"]
    )

    prediction = model.predict(
        pd.DataFrame({
            "YearsExperience":
            [experience]
        })
    )

    salary = round(
        prediction[0],
        2
    )

    # Save History

    history = pd.read_csv(
        "history.csv"
    )

    new_row = pd.DataFrame({

        "Name":[name],

        "Age":[age],

        "Education":[education],

        "Experience":[experience],

        "Salary":[salary]

    })

    history = pd.concat(
        [history,new_row],
        ignore_index=True
    )

    history.to_csv(
        "history.csv",
        index=False
    )

    # Create PDF Report

    if not os.path.exists("reports"):
        os.makedirs("reports")

    pdf_path = "reports/report.pdf"

    pdf = canvas.Canvas(pdf_path)

    pdf.setTitle(
        "Salary Prediction Report"
    )

    pdf.drawString(
        100,
        800,
        "Salary Prediction Report"
    )

    pdf.drawString(
        100,
        760,
        f"Name: {name}"
    )

    pdf.drawString(
        100,
        730,
        f"Age: {age}"
    )

    pdf.drawString(
        100,
        700,
        f"Education: {education}"
    )

    pdf.drawString(
        100,
        670,
        f"Skills: {skills}"
    )

    pdf.drawString(
        100,
        640,
        f"Experience: {experience}"
    )

    pdf.drawString(
        100,
        610,
        f"Predicted Salary: ₹{salary}"
    )

    pdf.save()

    history = pd.read_csv(
        "history.csv"
    )

    total_predictions = len(history)

    highest_salary = history[
        "Salary"
    ].max()

    average_salary = round(
        history["Salary"].mean(),
        2
    )

    return render_template(

        "index.html",

        prediction_text=
        f"₹ {salary:,.2f}",

        history=history.to_dict(
            orient="records"
        ),

        total_predictions=
        total_predictions,

        highest_salary=
        highest_salary,

        average_salary=
        average_salary

    )


@app.route('/download')
def download():

    return send_file(
        "reports/report.pdf",
        as_attachment=True
    )


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)