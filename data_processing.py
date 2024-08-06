# src/data_processing.py

import pandas as pd
import numpy as np
from src.base_classes import BaseLoader
from src.custom_exceptions import DataProcessingError, DataMappingError

class DataLoader(BaseLoader):
    def load_csv(self, file_path: str) -> pd.DataFrame:
        """Load a CSV file and return a DataFrame."""
        try:
            return pd.read_csv(file_path)
        except FileNotFoundError:
            raise DataProcessingError(f"File not found: {file_path}")

class DataProcessor:
    def __init__(self, db_handler):
        self.db_handler = db_handler

    def find_best_fit_functions(self, training_data, ideal_functions):
        best_fit_functions = {}
        for train_col in training_data.columns[1:]:
            y_train = training_data[train_col]
            deviations = {}
            for ideal_col in ideal_functions.columns[1:]:
                y_ideal = ideal_functions[ideal_col]
                deviation = np.sum((y_train - y_ideal) ** 2)
                deviations[ideal_col] = deviation
            best_fit = min(deviations, key=deviations.get)
            best_fit_functions[train_col] = best_fit
        return best_fit_functions

    def map_test_data(self, test_data, best_fit_functions, ideal_functions):
        # Ensure correct column names in test data
        if 'x' in test_data.columns and 'y' in test_data.columns:
            test_data.rename(columns={'x': 'X', 'y': 'Y'}, inplace=True)
        elif 'X' not in test_data.columns or 'Y' not in test_data.columns:
            print("Error: 'X' or 'Y' column not found in test data.")
            print(f"Test data columns: {test_data.columns}")
            return pd.DataFrame()  # Return an empty DataFrame

        mapped_data = []

        print("Ideal functions 'X' column data type and sample:")
        print(ideal_functions['X'].dtype, ideal_functions['X'].head())
        print("Test data 'X' column data type and sample:")
        print(test_data['X'].dtype, test_data['X'].head())

        for _, row in test_data.iterrows():
            x, y = row['X'], row['Y']
            print(f"Processing test data row: X={x}, Y={y}")

            # Use np.isclose to match floating point numbers accurately
            ideal_row = ideal_functions[np.isclose(ideal_functions['X'], x, atol=1e-9)]

            if ideal_row.empty:
                print(f"Warning: No matching X value found in ideal functions for X={x}")
                continue

            deviations = {}
            for col in best_fit_functions.values():
                if col not in ideal_row.columns:
                    print(f"Warning: Ideal function {col} not found in ideal functions for X={x}")
                    continue
                ideal_value = ideal_row[col].values[0]
                deviation = np.abs(y - ideal_value)
                deviations[col] = deviation

            if not deviations:
                print(f"Warning: No valid deviations found for X={x}")
                continue

            best_fit = min(deviations, key=deviations.get)
            mapped_data.append({'X': x, 'Y': y, 'Delta_Y': deviations[best_fit], 'Ideal_Function': best_fit})

        if not mapped_data:
            print("Warning: No test data could be mapped to ideal functions.")
            return pd.DataFrame()

        return pd.DataFrame(mapped_data)
