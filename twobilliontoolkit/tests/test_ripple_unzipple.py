import unittest
import os
import sys
import shutil
from tempfile import TemporaryDirectory


from twobilliontoolkit.RippleUnzipple.ripple_unzipple import ripple_unzip 

class TestRecursiveUnzip(unittest.TestCase):
    
    def setUp(self):
        # Create a temporary directory for testing
        self.temp_dir = TemporaryDirectory()
        self.input_path = "twobilliontoolkit/tests/Data/TestFolder"
        self.output_path = os.path.join(self.temp_dir.name, 'output')
        self.log_path = os.path.join(self.temp_dir.name, 'log.txt')

    def tearDown(self):
        # Clean up the temporary directory
        # self.temp_dir.cleanup()
        pass
        
    def test_invalid_input_path(self):
        # Test invalid input path
        invalid_input_path = "Invalid/Path"
        self.assertFalse(os.path.exists(invalid_input_path), "Test setup issue: The specified path exists.")

        # Use assertRaises to check if ValueError is raised with the correct error message
        with self.assertRaises(ValueError) as context:
            ripple_unzip(invalid_input_path, self.output_path)

        # Check if the correct error message is raised
        expected_error_message = f"ValueError: The specified path ({invalid_input_path}) does not exist"
        self.assertEqual(str(context.exception), expected_error_message)
    
    def test_directory(self):
        # Test unzipping a directory
        ripple_unzip(self.input_path, self.output_path)
        self.assertTrue(os.path.exists(self.output_path))

    def test_archive_zip(self):
        # Test unzipping a .zip file
        ripple_unzip(self.input_path + '.zip', self.output_path)
        self.assertTrue(os.path.exists(self.output_path))

    def test_archive_7z(self):
        # Test unzipping a .7z file
        ripple_unzip(self.input_path +'.7z', self.output_path)
        self.assertTrue(os.path.exists(self.output_path))
        
    def test_unsupported(self):
        # Test unsupported input type
        unsupported_input_path = self.input_path + '.txt'

        # Use assertRaises to check if ValueError is raised with the correct error message
        with self.assertRaises(ValueError) as context:
            ripple_unzip(unsupported_input_path, self.output_path)
            
        expected_error_message = "ValueError: Unsupported input type. Please provide a directory or a compressed file."
        self.assertEqual(str(context.exception), expected_error_message)
                
    def test_recursive_unzip(self):
        # Test recursive unzipping within a directory
        # define some test paths to make sure the recursion worked
        path1 = '/TestFolder'
        path2 = '/TestFolder/Child 5.xlsx'
        path3 = '/TestFolder/Child 1/Child 1.5'
        path4 = '/TestFolder/Child 3/Child 3/Child 3.3.xlsx'
        path5 = '/TestFolder/Child 2/Child 2/Child 2.6/Child 2.6/Child 2.6.6/Child 2.6.6/Child 2.6.6.1.txt'
        
        # Test unzipping a .zip file
        ripple_unzip(self.input_path + '.zip', self.output_path)
        print(self.output_path)
        self.assertTrue(os.path.exists(self.output_path + path1))
        self.assertTrue(os.path.exists(self.output_path + path2))
        self.assertTrue(os.path.exists(self.output_path + path3))
        self.assertTrue(os.path.exists(self.output_path + path4))
        self.assertTrue(os.path.exists(self.output_path + path5))

        # Test unzipping a .7z file
        ripple_unzip(self.input_path +'.7z', self.output_path)
        self.assertTrue(os.path.exists(self.output_path + path1))
        self.assertTrue(os.path.exists(self.output_path + path2))
        self.assertTrue(os.path.exists(self.output_path + path3))
        self.assertTrue(os.path.exists(self.output_path + path4))
        self.assertTrue(os.path.exists(self.output_path + path5))

if __name__ == '__main__':
    unittest.main()
    