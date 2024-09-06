from src.assignment1 import CityMap
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

   #Self Edge Cases:-

    def test_case_1(self):
        # Edge Case 1: No roads or tracks, only one location with a friend
        roads = []
        tracks = []
        friends = [("Grizz", 0)]
        myCity = CityMap(roads, tracks, friends)
        result = myCity.plan(0, 0)
        self.assertEqual(result, (0, [0], "Grizz", 0))
        # print("# Edge Case 1: No roads or tracks, only one location with a friend")
        # print(result)  # Expected output: (0, [0], "Grizz", 0)
    #     # print()
        
    # ###
    # ### INVALID TESTCASE: Every city is connected by road
    # ### 
    # def test_case_2(self):
    #     # Edge Case 2: Only tracks, no roads, disconnected locations
    #     roads = []
    #     tracks = [(0, 1, 2), (1, 2, 2)]
    #     friends = [("Grizz", 0)]
    #     myCity = CityMap(roads, tracks, friends)
    #     result = myCity.plan(0, 2)
    #     self.assertEqual(result,(-1, [], None, None))
    #     # print("# Edge Case 2: Only tracks, no roads, disconnected locations")
    #     # print(result)  # Expected output: (-1, [], None, None) or a valid route if possible
    #     # print()

    # ###
    # ### INVALID TESTCASE: Every city is connected by road
    # ### 
    # def test_case_3(self):
    #     # Edge Case 3: Isolated location with no connections
    #     roads = [(0, 1, 2), (1, 2, 2)]
    #     tracks = []
    #     friends = [("Grizz", 3)]
    #     myCity = CityMap(roads, tracks, friends)
    #     result = myCity.plan(0, 2)
    #     self.assertEqual(result,(-1, [], None, None))
    #     # print("# Edge Case 3: Isolated location with no connections")
    #     # print(result)  # Expected output: (-1, [], None, None)
    #     # print()

    ###
    ### INVALID TESTCASE: Every city is connected by road
    ### MODIFIED TESTCASE: Made city 1 connected to city 2, 3 with 1000 minutes
    ### 
    def test_case_4(self):
        # Edge Case 4: Multiple equidistant friends
        roads = [(0, 1, 2), (1, 2, 2), (1,3,1000), (1,4,1000)]
        tracks = [(0, 3, 2), (3, 2, 2), (0, 4, 2), (4, 2, 2)]
        friends = [("Grizz", 3), ("Ice", 4)]
        myCity = CityMap(roads, tracks, friends)
        result = myCity.plan(0, 2)
        self.assertIn(result, ((4, [0, 1, 2], 'Grizz', 2),
                               (4, [0, 1, 2], 'Ice', 2)))
        # print("# Edge Case 4: Multiple equidistant friends")
        # print(result)  # Expected output: Should pick either "Grizz" or "Ice"
        # print()


    ###
    ### INVALID TESTCASE: Every city is connected by road
    ### MODIFIED TESTCASE: Made city 2 connected to city 3 with 1000 minutes
    ### 
    def test_case_5(self):
        # Edge Case 5: Circular tracks
        roads = [(0, 1, 2), (1, 2, 2), (2, 3, 1000)]
        tracks = [(2, 3, 2), (3, 2, 2)]
        friends = [("Grizz", 3)]
        myCity = CityMap(roads, tracks, friends)
        result = myCity.plan(0, 2)
        self.assertEqual(result,(4, [0, 1, 2], 'Grizz', 2))
        # print("# Edge Case 5: Circular tracks")
        # print(result)  # Expected output: Should not result in infinite loop
        # print()

    def test_case_6(self):
        # Edge Case 6: Dense road network
        
        # roads looks like this 
        # roads = [(0, 1, 1), (0, 2, 1), (0, 3, 1), (0, 4, 1), 
        #          (1, 2, 1), (1, 3, 1), (1, 4, 1), 
        #          (2, 3, 1), (2, 4, 1), 
        #          (3, 4, 1)]
        roads = [(i, j, 1) for i in range(5) for j in range(i + 1, 5)]
        tracks = [(0, 1, 2), (1, 2, 2), (2, 3, 2), (3, 4, 2)]
        friends = [("Grizz", 4)]
        myCity = CityMap(roads, tracks, friends)
        result = myCity.plan(0, 4)
        self.assertEqual(result,(1, [0, 4], 'Grizz', 4))
        # print("# Edge Case 6: Dense road network")
        # print(result)  # Expected output: Ensure that the dense network is handled efficiently
        # print()

    def test_case_7(self):
        # Edge Case 7: Friend at destination
        roads = [(0, 1, 2), (1, 2, 2)]
        tracks = [(0, 2, 3)]
        friends = [("Grizz", 2)]
        myCity = CityMap(roads, tracks, friends)
        result = myCity.plan(0, 2)
        self.assertEqual(result,(4, [0, 1, 2], 'Grizz', 2))
        # print("# Edge Case 7: Friend at destination")
        # print(result)  # Expected output: (4, [0, 1, 2], "Grizz", 2)
        # print()

    def test_case_8(self):
        # Edge Case 8: Destination before friend’s location
        roads = [(0, 1, 2), (1, 2, 2), (2, 3, 2)]
        tracks = [(1, 3, 2)]  ###  T: I am not sure if this is meant to be (3,1,2)
        friends = [("Grizz", 3)]
        myCity = CityMap(roads, tracks, friends)
        result = myCity.plan(0, 2)
        self.assertEqual(result,(8, [0, 1, 2, 3, 2], 'Grizz', 3))
        # print("# Edge Case 8: Destination before friend’s location")
        # print(result)  # Expected output: Should consider whether going to pick up Grizz is optimal
        # print()

    def test_case_9(self):
        # Edge Case 9: Large input sizes
        roads = [(i, (i + 1) % 100, 1) for i in range(100)]
        tracks = [(i, (i + 2) % 100, 1) for i in range(100)]
        friends = [("Grizz", 50), ("Ice", 99)]
        myCity = CityMap(roads, tracks, friends)
        result = myCity.plan(0, 99)
        self.assertEqual(result,(1, [0, 99], 'Ice', 99))
        # print("# Edge Case 9: Large input sizes")
        # print(result)
        # print()


    def test_example_1(self):
        roads = [(3, 4, 2), (4, 0, 5), (2, 4, 2), (0, 2, 2), (1, 0, 3)]
        tracks = []
        friends = [('Seulgi', 4)]
        myCity = CityMap(roads, tracks, friends)

        path = myCity.plan(start=0, destination=1)
        expected = (11, [0, 2, 4, 2, 0, 1], 'Seulgi', 4)
        error_message = f'Current wrong path: {path}'
        self.assertEqual(path, expected, error_message)

        path = myCity.plan(start=3, destination=1)
        expected = (9, [3, 4, 2, 0, 1], 'Seulgi', 4)
        error_message = f'Current wrong path: {path}'
        self.assertEqual(path, expected, error_message)

        path = myCity.plan(start=4, destination=4)
        expected = (0, [4], 'Seulgi', 4)
        error_message = f'Current wrong path: {path}'
        self.assertEqual(path, expected, error_message)

        path = myCity.plan(start=4, destination=3)
        expected = (2, [4, 3], 'Seulgi', 4)
        error_message = f'Current wrong path: {path}'
        self.assertEqual(path, expected, error_message)
        
        path = myCity.plan(start=2, destination=1)
        expected = (9, [2, 4, 2, 0, 1], 'Seulgi', 4)
        error_message = f'Current wrong path: {path}'
        self.assertEqual(path, expected, error_message)

        path = myCity.plan(start=1, destination=0)
        expected = (11, [1, 0, 2, 4, 2, 0], 'Seulgi', 4)
        error_message = f'Current wrong path: {path}'
        self.assertEqual(path, expected, error_message)

    def test_example_2(self):
        roads = [(4, 0, 3), (0, 2, 4), (2, 3, 2), (4, 2, 2), (3, 0, 4), (1, 2, 1)]
        tracks = [(2, 3, 3), (4, 0, 1), (0, 1, 2)]
        friends = [('Winter', 0), ('Joy', 3), ('Irene', 2), ('CH', 3), ('Karina', 4)]
        myCity = CityMap(roads, tracks, friends)

        path = myCity.plan(start=4, destination=0)
        expected = [(3, [4, 0], 'Winter', 0), (3, [4, 0], 'Karina', 4)]
        error_message = f'Current wrong path: {path}'
        self.assertIn(path, expected, error_message)

        path = myCity.plan(start=1, destination=1)
        expected = (0, [1], 'Winter', 1)
        error_message = f'Current wrong path: {path}'
        self.assertEqual(path, expected, error_message)

    def test_example_3(self):
        roads = [(1, 0, 5), (4, 0, 5), (2, 4, 4), (0, 3, 4), (4, 1, 5)]
        tracks = [(1, 3, 1), (1, 0, 3), (4, 0, 2), (1, 4, 3)]
        friends = [('Winter', 1), ('Bebe', 4), ('Wendy', 3)]
        myCity = CityMap(roads, tracks, friends)

        path = myCity.plan(start=0, destination=0)
        expected = [(0, [0], 'Bebe', 0), (0, [0], 'Winter', 0)]
        error_message = f'Current wrong path: {path}'
        self.assertIn(path, expected, error_message)

        path = myCity.plan(start=0, destination=3)
        expected = (4, [0, 3], 'Wendy', 3)
        error_message = f'Current wrong path: {path}'
        self.assertEqual(path, expected, error_message)

        path = myCity.plan(start=1, destination=0)
        expected = (5, [1, 0], 'Winter', 1)
        error_message = f'Current wrong path: {path}'
        self.assertEqual(path, expected, error_message)

    def test_example_4(self):
        roads = [(1, 0, 1), (1, 3, 3), (3, 0, 1), (2, 4, 1), (1, 2, 5), (0, 4, 3)]
        tracks = [(2, 0, 5), (4, 0, 4), (0, 1, 3), (4, 1, 5)]
        friends = [('Winter', 4), ('CH', 2)]
        myCity = CityMap(roads, tracks, friends)
    
        path = myCity.plan(start=1, destination=3)
        expected = [(2, [1, 0, 3], 'Winter', 1), (2, [1, 0, 3], 'Winter', 0), (2, [1, 0, 3], 'CH', 0)]
        error_message = f'Current wrong path: {path}'
        self.assertIn(path, expected, error_message)

        path = myCity.plan(start=2, destination=0)
        expected = [(4, [2, 4, 0], 'Winter', 4), (4, [2, 4, 0], 'CH', 2)]
        error_message = f'Current wrong path: {path}'
        self.assertIn(path, expected, error_message)
        
        path = myCity.plan(start=4, destination=4)
        expected = (0, [4], 'Winter', 4)
        error_message = f'Current wrong path: {path}'
        self.assertEqual(path, expected, error_message)

if __name__ == '__main__':
    unittest.main()
