import pandas as pd


def generate_quality_report(dataframe):

    report = {
        "missing_values": dataframe.isnull().sum().to_dict(),

        "duplicate_rows": int(dataframe.duplicated().sum()),

        "empty_columns": dataframe.columns[
            dataframe.isnull().all()
        ].tolist(),

        "data_types": dataframe.dtypes.astype(str).to_dict(),

        "null_percentage": (
            dataframe.isnull().mean() * 100
        ).round(2).to_dict()
    }

    return report