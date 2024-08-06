# test/test_data_processing.py

import unittest
import pandas as pd
from src.data_processing import DataLoader, DataProcessor
from src.db_utils import DatabaseHandler

class TestDataProcessing(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db_handler = DatabaseHandler('sqlite:///../data/test_data.db')
        cls.db_handler.create_tables()
        cls.loader = DataLoader()
        cls.processor = DataProcessor(cls.db_handler)

    def setUp(self):
        # Mock data for testing
        self.train_data = pd.DataFrame({
            'X': [1.0, 2.0, 3.0],
            'Y1': [2.0, 3.0, 4.0],
            'Y2': [3.0, 4.0, 5.0],
            'Y3': [4.0, 5.0, 6.0],
            'Y4': [5.0, 6.0, 7.0]
        })
        self.ideal_data = pd.DataFrame({
            'X': [1.0, 2.0, 3.0],
            **{f'Y{i}': [i + 1.0, i + 2.0, i + 3.0] for i in range(1, 51)}
        })
        self.test_data = pd.DataFrame({
            'X': [1.0, 2.0, 3.0],
            'Y': [2.0, 3.0, 4.0]
        })

    def test_find_best_fit_functions(self):
        best_fit = self.processor.find_best_fit_functions(self.train_data, self.ideal_data)
        # Check that 4 best fit functions are found
        self.assertEqual(len(best_fit), 4)

    def test_map_test_data(self):
        best_fit = self.processor.find_best_fit_functions(self.train_data, self.ideal_data)
        mapped_data = self.processor.map_test_data(self.test_data, best_fit, self.ideal_data)
        # Check that mapping returns the same number of rows as test data
        self.assertEqual(len(mapped_data), len(self.test_data))

if __name__ == '__main__':
    unittest.main()
