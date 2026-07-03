from flask import Flask, render_template, request, send_file
import pandas as pd
import os
import shutil
from werkzeug.utils import secure_filename

from database import initialize_database, save_history, get_history, clear_history
from datetime import datetime
from validator import generate_quality_report
from cleaner import (
    remove_duplicate_rows,
    remove_empty_rows,
    remove_empty_columns,
    fill_missing_values,
    standardize_column_names,
    convert_data_types,
)

app = Flask(__name__)

initialize_database()

UPLOAD_FOLDER = "uploads"
CLEANED_FOLDER = "cleaned"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CLEANED_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["CLEANED_FOLDER"] = CLEANED_FOLDER


@app.route("/", methods=["GET", "POST"])
def home():

    preview_data = None
    total_rows = 0
    total_columns = 0
    quality_report = None
    summary = None
    error = None

    try:

        if request.method == "POST":

            uploaded_file = request.files.get("dataset")
            allowed_extensions = [".csv", ".xlsx"]

            if uploaded_file and uploaded_file.filename != "":

                extension = os.path.splitext(uploaded_file.filename)[1].lower()

                if extension not in allowed_extensions:
                    return render_template(
                        "index.html",
                        error="Please upload only CSV or Excel (.xlsx) files."
                    )

                filename = secure_filename(uploaded_file.filename)

                original_path = os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    filename
                )

                uploaded_file.save(original_path)

                for file in os.listdir(app.config["CLEANED_FOLDER"]):

                    file_path = os.path.join(
                        app.config["CLEANED_FOLDER"],
                        file
                    )

                    if os.path.isfile(file_path):
                        os.remove(file_path)

                filename_without_extension = os.path.splitext(filename)[0]
                extension = os.path.splitext(filename)[1]

                cleaned_filename = filename_without_extension + "_cleaned" + extension

                cleaned_path = os.path.join(
                    app.config["CLEANED_FOLDER"],
                    cleaned_filename
                )

                shutil.copy(original_path, cleaned_path)

            cleaned_file = request.form.get("cleaned_file")

            if cleaned_file:

                cleaned_path = os.path.join(
                    app.config["CLEANED_FOLDER"],
                    cleaned_file
                )

                if cleaned_file.endswith(".csv"):
                    dataframe = pd.read_csv(cleaned_path)
                else:
                    dataframe = pd.read_excel(cleaned_path)

                rows_before = len(dataframe)

                if "remove_duplicates" in request.form:
                    dataframe, count = remove_duplicate_rows(dataframe)
                    operation = "Duplicate Rows Removed"

                elif "remove_empty_rows" in request.form:
                    dataframe, count = remove_empty_rows(dataframe)
                    operation = "Empty Rows Removed"

                elif "remove_empty_columns" in request.form:
                    dataframe, count = remove_empty_columns(dataframe)
                    operation = "Empty Columns Removed"

                elif "fill_missing" in request.form:
                    dataframe, count = fill_missing_values(dataframe)
                    operation = "Missing Values Filled"

                elif "standardize_columns" in request.form:
                    dataframe = standardize_column_names(dataframe)
                    count = "-"
                    operation = "Column Names Standardized"

                elif "convert_types" in request.form:
                    dataframe = convert_data_types(dataframe)
                    count = "-"
                    operation = "Data Types Converted"

                rows_after = len(dataframe)

                summary = {
                    "operation": operation,
                    "rows_before": rows_before,
                    "rows_after": rows_after,
                    "count": count
                }

                save_history(
                    file_name=cleaned_file,
                    upload_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    cleaning_operation=operation,
                    final_row_count=rows_after
                )

                if cleaned_file.endswith(".csv"):
                    dataframe.to_csv(cleaned_path, index=False)
                else:
                    dataframe.to_excel(cleaned_path, index=False)

                preview_data = dataframe.head(10).to_html(
                    classes="table",
                    index=False
                )

                total_rows = len(dataframe)
                total_columns = len(dataframe.columns)

                quality_report = generate_quality_report(dataframe)

                return render_template(
                    "index.html",
                    preview_data=preview_data,
                    total_rows=total_rows,
                    total_columns=total_columns,
                    quality_report=quality_report,
                    cleaned_file=cleaned_file,
                    summary=summary,
                    error=error
                )

            files = os.listdir(app.config["CLEANED_FOLDER"])

            if files:

                latest_file = files[-1]

                cleaned_path = os.path.join(
                    app.config["CLEANED_FOLDER"],
                    latest_file
                )

                if latest_file.endswith(".csv"):
                    dataframe = pd.read_csv(cleaned_path)
                else:
                    dataframe = pd.read_excel(cleaned_path)

                preview_data = dataframe.head(10).to_html(
                    classes="table",
                    index=False
                )

                total_rows = len(dataframe)
                total_columns = len(dataframe.columns)

                quality_report = generate_quality_report(dataframe)

                return render_template(
                    "index.html",
                    preview_data=preview_data,
                    total_rows=total_rows,
                    total_columns=total_columns,
                    quality_report=quality_report,
                    cleaned_file=latest_file,
                    error=error
                )

    except Exception:
        return render_template(
            "index.html",
            error="Something went wrong while processing the dataset. Please upload a valid CSV or Excel file and try again."
        )

    return render_template("index.html")

@app.route("/history", methods=["GET", "POST"])
def history():

    if request.method == "POST":
        clear_history()

    history_data = get_history()

    return render_template(
        "history.html",
        history=history_data
    )

@app.route("/download/<filename>")
def download(filename):

    file_path = os.path.join(
        app.config["CLEANED_FOLDER"],
        filename
    )

    return send_file(
        file_path,
        as_attachment=True
    )

if __name__ == "__main__":
    app.run(debug=True)