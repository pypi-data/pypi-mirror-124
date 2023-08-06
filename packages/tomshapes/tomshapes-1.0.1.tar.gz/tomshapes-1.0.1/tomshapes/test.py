import unittest

from Circle import Circle

class TestCircleClass(unittest.TestCase):
    def setUp(self):
        self.circle = Circle('red', 5)

    def test_initialization(self): 
        self.assertEqual(self.circle.color, 'red', 'incorrect mean')
        self.assertEqual(round(self.circle.get_area(),2), 78.54, 'incorrect mean')

    
if __name__ == '__main__':
    unittest.main()