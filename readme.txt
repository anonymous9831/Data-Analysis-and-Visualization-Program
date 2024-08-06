Data Analysis and Visualization Program

Overview
This Python program is designed to process, analyze, and visualize data from training datasets, ideal functions, and test data. The program identifies the best fit ideal functions for training data, maps test data to these functions, and visualizes the results. It utilizes Python's Pandas library for data manipulation, SQLAlchemy for database interactions, and Bokeh for data visualization.

Features

Data Loading: Load data from CSV files into pandas DataFrames.
Data Processing: Identify the best fit ideal functions for training data using the least-squares method.
Data Mapping: Map test data to the identified ideal functions and calculate deviations.
Database Storage: Store training data, ideal functions, and test data in a SQLite database.
Data Visualization: Visualize the relationships between training data, ideal functions, and test data.
Error Handling: Custom exceptions for specific error cases in data processing and database operations.
Unit Testing: Comprehensive unit tests to validate the functionality of all components.
Installation

1) Clone the Repository:
"git clone <repository-url>
cd <repository-directory>
"
2) Set Up a Virtual Environment:
"python -m venv venv
source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
"
3) Install Required Packages:
"pip install -r requirements.txt
"
Usage
Running the Program

Prepare Your Data:
Place your training, ideal, and test datasets in CSV format in the data directory.
Update the file paths in main.py if necessary.
Run the Program:
"python main.py
"
The program will process the data, store it in the database, map the test data, and display visualizations.
Running Tests
To run the unit tests, execute the following command:
"python -m unittest discover -s test
"
This will run all the tests in the test directory.

Project Structure

src/: Contains the core program modules.
base_classes.py: Base classes for common functionality.
data_processing.py: Classes for data loading and processing.
db_utils.py: Database interaction and management.
visualization.py: Data visualization using Bokeh.
custom_exceptions.py: Custom exceptions for specific error handling.
data/: Directory for storing the dataset CSV files.
test/: Contains the unit tests for the program.
test_data_processing.py: Tests for data loading and processing.
test_db_utils.py: Tests for database operations.
test_visualization.py: Tests for data visualization.
requirements.txt: Lists all the required Python packages.
main.py: The main entry point for the program.
Troubleshooting

Integrity Errors: If you encounter IntegrityError warnings, ensure that your data does not contain duplicate entries for primary key fields (e.g., X values).
File Not Found: Make sure the file paths specified in the program match the locations of your data files.
Data Type Mismatches: Ensure that the data types in your CSV files are consistent with the expected types (e.g., numerical values for coordinates).
Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any feature additions or bug fixes.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgements
This project uses open-source libraries, including Pandas, SQLAlchemy, and Bokeh. Special thanks to the developers and maintainers of these libraries.
