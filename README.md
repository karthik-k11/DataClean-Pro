# DataClean Pro

A web-based data cleaning and quality analysis tool built with Flask and Pandas.

DataClean Pro allows users to upload CSV or Excel datasets, inspect data quality, apply common cleaning operations, and download the cleaned dataset.

## Features

- Upload CSV and XLSX datasets
- Preview uploaded datasets
- View dataset row and column counts
- Detect missing values
- Detect duplicate rows
- Detect empty columns
- View column data types
- View null percentages
- Remove duplicate rows
- Remove empty rows
- Remove empty columns
- Fill missing values
- Standardize column names
- Convert data types
- View before/after cleaning summaries
- Save cleaning operation history
- Clear cleaning history
- Download cleaned datasets

## Tech Stack

- Python
- Flask
- Pandas
- SQLite
- HTML
- CSS
- JavaScript

## Project Structure

```text
DataClean-Pro/
│
├── app.py
├── cleaner.py
├── validator.py
├── database.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── templates/
│   ├── index.html
│   └── history.html
│
├── static/
│   └── style.css
│
├── uploads/
├── cleaned/
└── database/