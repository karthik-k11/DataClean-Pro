from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/", methods=["GET", "POST"])
def home():
    preview_data = None
    total_rows = 0
    total_columns = 0
    error = None

    if request.method == "POST":
        file = request.files.get("dataset")

        if file and file.filename != "":
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(file_path)

            try:
                if file.filename.endswith(".csv"):
                    dataframe = pd.read_csv(file_path)
                elif file.filename.endswith(".xlsx"):
                    dataframe = pd.read_excel(file_path)
                else:
                    raise ValueError("Only CSV and XLSX files are supported.")

                preview_data = dataframe.head(10).to_html(
                    classes="table",
                    index=False
                )

                total_rows = dataframe.shape[0]
                total_columns = dataframe.shape[1]

            except Exception as e:
                error = str(e)

    return render_template(
        "index.html",
        preview_data=preview_data,
        total_rows=total_rows,
        total_columns=total_columns,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)