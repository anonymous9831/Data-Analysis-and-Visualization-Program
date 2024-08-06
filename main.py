import os
import pandas as pd
from src.data_processing import DataLoader, DataProcessor
from src.db_utils import DatabaseHandler
from src.visualization import Visualizer
from src.custom_exceptions import DataProcessingError, DataMappingError, DatabaseError

def main():
    # File paths (update with actual paths to your CSV files)
    train_data_files = ['data/train.csv']
    ideal_functions_file = 'data/ideal.csv'
    test_data_file = 'data/test.csv'
    db_path = 'sqlite:///data/datasets.db'

    try:
        # Initialize components
        data_loader = DataLoader()
        db_handler = DatabaseHandler(db_path)
        data_processor = DataProcessor(db_handler)
        visualizer = Visualizer()

        # Create tables in the database
        db_handler.create_tables()

        # Load and insert training data into the database
        for train_file in train_data_files:
            try:
                training_data = data_loader.load_csv(train_file)
                db_handler.insert_training_data(training_data)
                print(f"Training data from {train_file} inserted successfully.")
            except Exception as e:
                print(f"Failed to load or insert training data from {train_file}: {e}")

        # Load and insert ideal functions into the database
        try:
            ideal_functions = data_loader.load_csv(ideal_functions_file)
            db_handler.insert_ideal_functions(ideal_functions)
            print("Ideal functions inserted successfully.")
        except Exception as e:
            print(f"Failed to load or insert ideal functions: {e}")
            return

        # Find best fit ideal functions for each training dataset
        try:
            best_fit_functions = data_processor.find_best_fit_functions(training_data, ideal_functions)
            print("Best fit functions found:", best_fit_functions)
        except Exception as e:
            print(f"Failed to find best fit functions: {e}")
            return

        # Load and insert test data, and map to ideal functions
        try:
            test_data = data_loader.load_csv(test_data_file)
            mapped_data = data_processor.map_test_data(test_data, best_fit_functions, ideal_functions)
            db_handler.insert_test_data(mapped_data)
            print("Test data mapped and inserted successfully.")
        except Exception as e:
            print(f"Failed to load, map, or insert test data: {e}")
            return

        # Visualize the data
        try:
            visualizer.plot_data(training_data, test_data, ideal_functions, mapped_data)
            print("Data visualization completed.")
        except Exception as e:
            print(f"Failed to visualize data: {e}")

    except (DataProcessingError, DataMappingError, DatabaseError) as specific_error:
        print(f"An error occurred: {specific_error}")
    except Exception as general_error:
        print(f"An unexpected error occurred: {general_error}")

if __name__ == '__main__':
    main()