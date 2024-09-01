from assignment1 import CityMap
import unittest

class TestCityMap(unittest.TestCase):

    def test_spec_example_1_1(self):
        # Example 1.1, simple example
        roads = [(0,1,4), (0,3,2), (2,0,3), (3,1,2), (2,4,2), (4,5,3)]
        tracks = [(1,3,3), (3,4,2), (4,3,2), (4,5,4), (5,1,6)]
        friends = [("Grizz", 1), ("Ice", 3)]
        myCity = CityMap(roads, tracks, friends)

        got = myCity.plan(start=2, destination=5)
        expected = (5, [2,4,5], "Ice", 4)
        fail_message = f'got {got} for example 1.1, expected'
        self.assertEqual(got, expected, fail_message)

    
    def test_spec_example_1_2(self):
        # Example 1.2, meeting the friend at destination
        roads = [(0,1,4), (0,3,2), (2,0,3), (3,1,2), (2,4,2), (4,5,3)]
        tracks = [(1,3,3), (3,4,2), (4,3,2), (4,5,4), (5,1,6)]
        friends = [("Grizz", 1), ("Ice", 3)]
        myCity = CityMap(roads, tracks, friends)

        got = myCity.plan(start=0, destination=4)
        expected = (5, [0,2,4], "Ice", 4)
        fail_message = f'got {got} for example 1.2, expected {expected}'
        self.assertEqual(got, expected, fail_message)

    
    def test_spec_example_1_3(self):
        # Example 1.3
        roads = [(0,1,4), (0,3,2), (2,0,3), (3,1,2), (2,4,2), (4,5,3)]
        tracks = [(1,3,3), (3,4,2), (4,3,2), (4,5,4), (5,1,6)]
        friends = [("Grizz", 1), ("Ice", 3)]
        myCity = CityMap(roads, tracks, friends)

        got = myCity.plan(start=2, destination=1)
        expected = [(7, [2,0,1], "Grizz", 1), (7, [2,0,3,1], "Ice", 3)]
        self.assertIn(got, expected, f'got {got} for example 1.3')

    
    def test_spec_example_1_4(self):
        # Example 1.4, going beyond the destination
        roads = [(0,1,4), (0,3,2), (2,0,3), (3,1,2), (2,4,2), (4,5,3)]
        tracks = [(1,3,3), (3,4,2), (4,3,2), (4,5,4), (5,1,6)]
        friends = [("Grizz", 1), ("Ice", 3)]
        myCity = CityMap(roads, tracks, friends)

        got = myCity.plan(start=2, destination=0)
        expected = (7, [2,0,3,0], "Ice", 3)
        fail_message = f'got {got} for example 1.4, expected {expected}'
        self.assertEqual(got, expected, fail_message)
    
    
    def test_spec_example_2_1(self):
        # Example 2.1, the less train, the better
        roads = [(0,1,4), (0,3,2), (2,0,3), (3,1,2), (2,4,2), (4,5,3)]
        tracks = [(1,3,4), (3,4,2), (4,3,2), (4,5,1), (5,1,6)]
        friends = [("Grizz", 1), ("Ice", 3)]
        myCity = CityMap(roads, tracks, friends)
        
        got = myCity.plan(start=2, destination=5)
        expected = (5, [2,4,5], "Ice", 4)
        fail_message = f'got {got} for example 2.1, expected {expected}'
        self.assertEqual(got, expected, fail_message)
    
    
    def test_spec_example_2_2(self):
        # Example 2.2, a more complex scenario
        roads = [(0,1,4), (0,3,2), (2,0,3), (3,1,2), (2,4,2), (2,5,2)]
        tracks = [(1,3,4), (3,4,2), (4,5,1), (5,1,6)]
        friends = [("Grizz", 1)]
        myCity = CityMap(roads, tracks, friends)

        got = myCity.plan(start=2, destination=5)
        expected = (6, [2,4,2,5], "Grizz", 4)
        fail_message = f'got {got} for example 2.2, expected {expected}'
        self.assertEqual(got, expected, fail_message)

    # All examples below this point will be student provided    
    def test_my_example_1(self):
        roads = [(0,1,2)]
        tracks = [(0,1,3)]
        friends = [('Sarah', 0)]
        myCity = CityMap(roads, tracks, friends)

        got = myCity.plan(start=1, destination=1)
        expected = (0, [1], 'Sarah', 1)
        self.assertEqual(got, expected)
    
    
    def test_my_example_2(self):
        roads = [(0,1,2), (1,2,3), (2,3,4)]
        tracks = [(0,2,3),(2,3,4),(3,1,3)]
        friends = [('Roberta Sparrow', 0)]
        myCity = CityMap(roads, tracks, friends)

        got = myCity.plan(start=1, destination=1)
        expected = (4, [1,0,1], 'Roberta Sparrow', 0)
        self.assertEqual(got, expected)
    
    
    def test_my_example_3(self):
        roads = [(0,1,2), (1,2,3)]
        tracks = [(0,2,3)]
        friends = [('RB', 2)]
        myCity = CityMap(roads, tracks, friends)

        got = myCity.plan(start=1, destination=1)
        expected = (6, [1,2,1], 'RB', 2)
        self.assertEqual(got, expected)
    
    
    def test_my_example_4(self):
        roads = [(0,1,1), (1,2,1), (2,3,1), (3,4,1), (4,5,1)]
        tracks = []
        friends = [('Jessica Hyde', 5)]
        myCity = CityMap(roads, tracks, friends)

        got = myCity.plan(start=1, destination=1)
        expected = (8, [1,2,3,4,5,4,3,2,1], 'Jessica Hyde', 5)
        self.assertEqual(got, expected)
    
    
    def test_my_example_5(self):
        roads = [(0,1,1), (1,2,1), (2,3,1), (3,4,1), (4,5,1)]
        tracks = [(0,5,4), (1,3,1), (2,5,1)]
        friends = [('Minnie', 0), ('Mouse', 1)]
        myCity = CityMap(roads, tracks, friends)

        got = myCity.plan(start=5, destination=5)
        expected = (0, [5], 'Minnie', 5)
        self.assertEqual(got, expected)
    
    
    def test_my_example_6(self):
        roads = [(0,1,1), (1,2,1), (2,3,1), (3,4,1), (4,5,1), (0,5,10)]
        tracks = []
        friends = [('Ariel', 5)]
        myCity = CityMap(roads, tracks, friends)

        got = myCity.plan(start=0, destination=5)
        expected = (5, [0,1,2,3,4,5], 'Ariel', 5)
        self.assertEqual(got, expected)

if __name__ == '__main__':
    unittest.main()
