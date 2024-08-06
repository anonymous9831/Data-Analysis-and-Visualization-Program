import os
import sqlalchemy as db
import pandas as pd
from sqlalchemy.sql import text

class DatabaseHandler:
    def __init__(self, db_url='sqlite:///data/datasets.db'):
        self.db_url = db_url
        self._ensure_directory_exists()
        self.engine = db.create_engine(self.db_url)
        self.connection = self.engine.connect()
        self.metadata = db.MetaData()

    def _ensure_directory_exists(self):
        db_path = self.db_url.replace('sqlite:///', '')
        db_dir = os.path.dirname(db_path)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
            print(f"Created directory for database: {db_dir}")
        else:
            print(f"Directory for database already exists: {db_dir}")

    def create_tables(self):
        self.metadata.drop_all(self.engine)
        print("Dropped existing tables.")

        training_data_table = db.Table('training_data', self.metadata,
            db.Column('X', db.Float, primary_key=True),
            db.Column('Y1', db.Float),
            db.Column('Y2', db.Float),
            db.Column('Y3', db.Float),
            db.Column('Y4', db.Float)
        )
        
        ideal_functions_table = db.Table('ideal_functions', self.metadata,
            db.Column('X', db.Float, primary_key=True),
            *[db.Column(f'Y{i}', db.Float) for i in range(1, 51)]
        )
        
        test_data_table = db.Table('test_data', self.metadata,
            db.Column('X', db.Float, primary_key=True),
            db.Column('Y', db.Float),
            db.Column('Delta_Y', db.Float),
            db.Column('Ideal_Function', db.String)
        )

        self.metadata.create_all(self.engine)
        print("Tables created successfully.")

    def clear_table(self, table_name):
        conn = self.engine.connect()
        conn.execute(text(f"DELETE FROM {table_name}"))
        conn.close()
        print(f"Cleared table: {table_name}")

    def insert_training_data(self, training_data):
        training_data.columns = ['X', 'Y1', 'Y2', 'Y3', 'Y4']
        training_data = training_data.drop_duplicates(subset='X')
        
        unique_x_count = training_data['X'].nunique()
        total_rows = len(training_data)
        print(f"Unique X values in training data: {unique_x_count} / {total_rows}")

        conn = self.engine.connect()
        self.clear_table('training_data')

        try:
            training_data.to_sql('training_data', conn, if_exists='append', index=False)
            print("Data inserted into training_data successfully.")
        except db.exc.IntegrityError as e:
            print(f"Error inserting data into training_data: {e}")
        finally:
            conn.close()

    def insert_ideal_functions(self, ideal_functions):
        ideal_functions.columns = ['X'] + [f'Y{i}' for i in range(1, 51)]
        ideal_functions = ideal_functions.drop_duplicates(subset='X')
        
        unique_x_count = ideal_functions['X'].nunique()
        total_rows = len(ideal_functions)
        print(f"Unique X values in ideal functions: {unique_x_count} / {total_rows}")

        conn = self.engine.connect()
        self.clear_table('ideal_functions')

        try:
            ideal_functions.to_sql('ideal_functions', conn, if_exists='append', index=False)
            print("Data inserted into ideal_functions successfully.")
        except db.exc.IntegrityError as e:
            print(f"Error inserting data into ideal_functions: {e}")
        finally:
            conn.close()
    
    def insert_test_data(self, test_data):
        test_data.columns = ['X', 'Y', 'Delta_Y', 'Ideal_Function']
        test_data = test_data.drop_duplicates(subset='X')
        
        unique_x_count = test_data['X'].nunique()
        total_rows = len(test_data)
        print(f"Unique X values in test data: {unique_x_count} / {total_rows}")

        conn = self.engine.connect()
        self.clear_table('test_data')

        try:
            test_data.to_sql('test_data', conn, if_exists='append', index=False)
            print("Data inserted into test_data successfully.")
        except db.exc.IntegrityError as e:
            print(f"Error inserting data into test_data: {e}")
        finally:
            conn.close()