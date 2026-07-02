import pandas as pd


def remove_duplicate_rows(dataframe):

    cleaned_dataframe = dataframe.drop_duplicates()

    duplicates_removed = len(dataframe) - len(cleaned_dataframe)

    return cleaned_dataframe, duplicates_removed


def remove_empty_rows(dataframe):

    cleaned_dataframe = dataframe.dropna(how="all")

    rows_removed = len(dataframe) - len(cleaned_dataframe)

    return cleaned_dataframe, rows_removed


def remove_empty_columns(dataframe):
    columns_before = dataframe.shape[1]

    cleaned_dataframe = dataframe.dropna(axis=1, how="all")

    columns_after = cleaned_dataframe.shape[1]

    columns_removed = columns_before - columns_after

    return cleaned_dataframe, columns_removed


def fill_missing_values(dataframe):
    """
    Fill missing values.
    """

    cleaned_dataframe = dataframe.copy()

    missing_values_fixed = 0

    for column in cleaned_dataframe.columns:

        # Skip completely empty columns
        if cleaned_dataframe[column].isnull().all():
            continue

        count = cleaned_dataframe[column].isnull().sum()

        if pd.api.types.is_numeric_dtype(cleaned_dataframe[column]):
            cleaned_dataframe[column] = cleaned_dataframe[column].fillna(
                cleaned_dataframe[column].mean()
            )
        else:
            cleaned_dataframe[column] = cleaned_dataframe[column].fillna(
                "Unknown"
            )

        missing_values_fixed += count

    return cleaned_dataframe, int(missing_values_fixed)

def standardize_column_names(dataframe):

    cleaned_dataframe = dataframe.copy()

    cleaned_dataframe.columns = [
        column.strip().lower().replace(" ", "_")
        for column in cleaned_dataframe.columns
    ]

    return cleaned_dataframe


def convert_data_types(dataframe):

    cleaned_dataframe = dataframe.convert_dtypes()

    return cleaned_dataframe