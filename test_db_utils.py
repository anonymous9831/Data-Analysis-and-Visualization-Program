# test/test_db_utils.py

import unittest
import pandas as pd
from sqlalchemy import create_engine
from src.db_utils import DatabaseHandler

DATABASE_URI = 'sqlite:///../data/test_data.db'

class TestDBUtils(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db_handler = DatabaseHandler(DATABASE_URI)
        cls.db_handler.create_tables()

    def setUp(self):
        self.engine = create_engine(DATABASE_URI)
        self.connection = self.engine.connect()
        # Clear tables before each test to ensure a clean state
        self.db_handler.clear_table('training_data')
        self.db_handler.clear_table('ideal_functions')
        self.db_handler.clear_table('test_data')

    def tearDown(self):
        self.connection.close()

    def test_insert_training_data(self):
        data = pd.DataFrame({
            'X': [1.0, 2.0, 3.0],
            'Y1': [2.0, 3.0, 4.0],
            'Y2': [3.0, 4.0, 5.0],
            'Y3': [4.0, 5.0, 6.0],
            'Y4': [5.0, 6.0, 7.0]
        })
        self.db_handler.insert_training_data(data)
        result = pd.read_sql_table('training_data', self.connection)
        self.assertEqual(len(result), 3)

    def test_insert_ideal_functions(self):
        data = pd.DataFrame({
            'X': [1.0, 2.0, 3.0],
            **{f'Y{i}': [i + 1.0, i + 2.0, i + 3.0] for i in range(1, 51)}
        })
        self.db_handler.insert_ideal_functions(data)
        result = pd.read_sql_table('ideal_functions', self.connection)
        self.assertEqual(len(result), 3)

    def test_insert_test_data(self):
        # Test data should match the format after data processing
        data = pd.DataFrame({
            'X': [1.0, 2.0, 3.0],
            'Y': [2.0, 3.0, 4.0],
            'Delta_Y': [0.5, 0.6, 0.7],
            'Ideal_Function': ['Y1', 'Y2', 'Y3']
        })
        self.db_handler.insert_test_data(data)
        result = pd.read_sql_table('test_data', self.connection)
        self.assertEqual(len(result), 3)

if __name__ == '__main__':
    unittest.main()
