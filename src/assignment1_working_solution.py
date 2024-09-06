from minheap import MinHeap
from graph import Graph

class CityMap:
    """
    Class description:
    The CityMap class represents a city's network of roads and friend pickup locations. It supports calculating the shortest paths 
    between locations, as well as planning routes that must include picking up a friend from an optimal pickup point with the plan method.

    - Roads are represented as undirected edges between locations (nodes), with weights representing travel time.
    - Tracks represent train routes, which only friends can use.
    - Friends are associated with specific locations, and they can only travel within 2 train hops 
      from their starting position. This constraint is taken into account when planning routes. 
    """
    def __init__(self, roads: list[tuple[int,int,int]], tracks: list[tuple[int,int,int]], friends: list[tuple[int,str]]) -> None:
        """
        Function description: 
        Same as the init of the Graph class. Initializes the graph with roads, tracks, and friends data. 
        It constructs the road graph using an adjacency list and associates friends with their respective locations, also 
        updating train hops for valid locations that are within 2 train stops.

        Input:
            roads: List of tuples (start_vertex, end_vertex, weight) representing roads.
            tracks: List of tuples (start_vertex, end_vertex, weight) representing tracks.
            friends: List of tuples (friend_name, location) representing friends and their locations.
        
        Output: None

        Time complexity: O(|R| + |T|)
        - |R| is the number of roads.
        - |T| is the number of tracks.
        
        Time complexity analysis:
        - O(|R|) to iterate over all roads and add undirected edges.
        - O(|T|) to iterate over the tracks and update the train hops.
        - We can assume that |F| <= |L| (the number of friends is at most the number of locations)
        - We can also assume that |R| >= |L| - 1 which is the definition of a graph.
        - Therefore we can infer that |R| > |F| (number of raods will always be greater than the number of friends)
        - Hence, O(|F|) is dominated by O(|R|) and thus we can ignore |F| in the complexity.


        Space complexity: O(|R|)
        
        Space complexity analysis: 
        - The space we are initialising for the adjacency list is the length of the roads list + 1, the space complexity becomes O(|R|). 
        - Since the graph is connected and simple, the number of locations |L| will not exceed |R| + 1, so the space complexity is 
        dominated by the number of roads |R|.
        """
        # define the roads, tracks and friends inputs as class variables 
        self.road_graph = Graph(roads, tracks, friends)


    def dijkstras(self, start_node: int, end_node: int = None) -> tuple[list,list] | list:
        """
        Description: 
        Implements Dijkstra's algorithm to find the shortest path from a start node to all other nodes or to a specific end node.
        It works by expanding the shortest known path at each step and updating the neighboring nodes distances when shorter paths are found.
        Input:
            - start_node: The starting vertex for the shortest path calculation.
            - end_node (optional): The destination vertex for path reconstruction. If provided, only the path to this node is returned.

        Output:
            - If end_node is provided: Returns the reconstructed path from start_node to end_node.
            - Otherwise: Returns the distance and parent arrays representing the shortest paths from start_node to all other nodes.

        Time complexity: O(|R| log |L|), where:
            - |R| is the number of roads (edges).
            - |L| is the number of locations (vertices).

        Time complexity analysis:
        - The priority queue (MinHeap) operations take log |L| time per location when we extract the min
        - The time complexty to extract the min from each location is O(|L| log |L|).
        - Each road (edge) is relaxed once, which results in O(|R| log |L|) because we are looping over all the roads |R|
        and then performing an insert into the minheap which costs log |L|. 
        - Therefore the overall complexity is O(|R| log |L| + |L| log |L|)
        - Since |R| >= |L| - 1, the value |L| becomes negligible in comparison and we can simplify the overall time 
        complexity to O(|R| log |L|).

        Space complexity: O(|R|)
        - Since we are initialising the distance and parent arrays with the length of the road graph, the space complexity of
        this becomes O(2|R|).
        - The constant 2 can be removed, so then the space complexity just becomes O(|R|)
        """
        # the *len method works bc the list items that are being initialised are immutable and therefore they are all independent copies
        distance = [float('inf')] * len(self.road_graph) # all distances are infinity
        parent = [-1] * len(self.road_graph) # all parents are -1

        distance[start_node] = 0 # the distance from the start vertex to itself is 0

        # initialise the priority queue with the start_node havinng a distance of 0
        priority_queue = MinHeap()
        priority_queue.insert(start_node, 0)

        
        # get the graph from the Graph class
        graph = self.road_graph.get_graph()

        while not priority_queue.is_empty():
            u, dist_u = priority_queue.extract_min() # extract vertex with minimum distance

            # relaxation step
            for _, v, weight in graph[u][0]: 
                if distance[u] + weight < distance[v]:
                    distance[v] = distance[u] + weight
                    parent[v] = u
                    priority_queue.insert(v, distance[v])

        # reconstructing shortest path if end node is provided
        if end_node is not None:
            path = self.route_half_reconstruction(end=end_node, parents=parent)
            return path

        # if not, then just return the distance and parent lists
        return distance, parent
    

    def route_half_reconstruction(self, end: int, parents: list[int]) -> list[int]:
        """
        Description: 
        Reconstructs a path from the given endpoint back to the start using the parent array, which is generated by Dijkstra's algorithm.
        This method traces the shortest path in reverse, starting from the end location and following the predecessors 
        recorded in the parents array until it reaches the starting location (where the parent is -1). The path is then reversed to 
        give the correct order from start to end.

        Input:
            - end: The destination location for the path reconstruction.
            - parents: The parent array, where each index stores the predecessor of the corresponding location.

        Output:
            - A list of vertices representing the reconstructed path.

        Time complexity: O(|L|), where |L| is the number of locations traversed in the path.
        - The method performs a reverse traversal of the parents array, which requires O(|L|) time, where |L| is the 
          number of locations in the graph. In the worst case, the entire path from the start to the end needs to be traced, 
          making the complexity O(|L|).

        Space complexity: O(|L|)
        - The size of the path list is at most O(|L|), as it includes all locations in the path from the start to the end.
        - Therefore, the space complexity is O(|L|).
        """
        path = []
        current = end
        while current != -1:
            path.append(current)
            current = parents[current]
        path.reverse()
        return path

    def route_full_reconstruction(self, start: int, pickup: int, destination: int) -> list[int]:
        """
        Description: 
        Reconstructs the full route from the start location to the destination location, making a stop at the pickup location.
        It combines two partial paths using the dijkstra method: one from start to the pickup location and another from pickup 
        to the destination.

        Input:
            - start: The starting location of the path.
            - pickup: The pickup location where a friend is picked up.
            - destination: The final destination location of the path.

        Output:
            - A list of locations representing the full reconstructed path, including the pickup.

        Time Complexity: O(|R| log |L|)
        - Two calls to Dijkstra's algorithm dominate the time complexity.
        - Dijkstra's algorithm runs twice, once from start to pickup and once from pickup to destination.
        - These runs have a complexity of O(|R| log |L|), where |R| is the number of roads (edges) and |L| 
        is the number of locations (vertices).
        - Reconstructing the paths is O(|L|), but this is dominated by the dijkstra method.
        - Therefore, the overall time complexity is O(|R| log |L|).

        Space Complexity: O(|R|)
        - Two arrays (distance and parent) are used in Dijkstra's algorithm, each of size |R|.
        - The priority queue (MinHeap) also stores up to |R| elements.
        - The space required for storing the reconstructed path is proportional to the number of road.
        - Overall, the space complexity is O(|R|).
        """
        route_half_1 = self.dijkstras(start_node=start, end_node=pickup)
        route_half_2 = self.dijkstras(start_node=pickup, end_node=destination)

        route_half_1.pop() # removing the pickup spot

        route = route_half_1 + route_half_2

        return route

    def plan(self, start: int, destination: int) -> tuple[int, list, str, int]: # (total_time, route, pickup_friend, pickup_location)
        """
        Description:
        Plans a route from the start location to the destination, ensuring that a friend is picked up at the most suitable location
        given the constraint that they can't travel more than 2 train hops away from their starting location.
        The method uses Dijkstra's algorithm twice to calculate the shortest paths: once from the start to all locations and 
        once from the destination to all locations. It identifies the potential pickup locations of each friend and 
        finds the distance from the start to that pickup location and from the destination to that pickup location. As it checks all
        combinations of potential pickup spots, it then compares this shortest distance value with the current shortest valid distance 
        value, and if it calculates a new combination which has a shorter path, then it updates all the information to make this the
        new shortest value. Finally, it reconstructs the complete route which includes the optimal pickup location by using 
        the route_full_reconstruction method which runs dijkstras twice.

        Input:
            - start: The starting location.
            - destination: The destination location.

        Output:
            - A tuple containing:
                - total_time: The total travel time for the journey.
                - route: A list of locations representing the complete route, including the pickup.
                - pickup_friend: The name of the friend being picked up.
                - pickup_location: The location where the friend is picked up.

        Time complexity: O(|R| log |L|)

        - To begin with, this method performs two calls to Dijkstra's algorithm, each of which has a time complexity 
        of O(|R| log |L|), where:
            - |R| is the number of roads (edges).
            - |L| is the number of locations (vertices).
        - This method then finds the potential pickup locations of the friend(s) by iterating through the each location of the graph
        which runs at most |L| times (one pickup for each location) giving time complexity of O(|L|).
        - It then iterates through these pickup locations and performs simple arithmetic to check and update the shortest path if it 
        finds one, which is done in O(|L|).
        - After finding the shortest route, it reconstructs the path using 2 runs of dijkstras at most O(2|R| log |L|)
        - Hence the total time complexity is O(4|R| log|L| + 2|L|).
        - Since |R| >= |L| - 1, the term |R| log |L| dominates and the constant 4 can be removed.
        - Therefore, the overall time complexity is O(|R| log |L|).

        Space complexity: O(|R|)
        
        - The Dijkstra's algorithm uses arrays of size |R| to store distances and parents.
        - The reconstructed route and potential pickup locations also require space proportional to |R|.
        - Therefore, the overall space complexity is O(|R|).
        """
        start_distances, start_parents = self.dijkstras(start_node=start) # finding shortest distance from start to all other nodes
        destination_distances, destination_parents = self.dijkstras(start_node=destination) # finding shortest distance from destination to all other nodes

        # initialising final values
        final_total_time = float('inf')
        route = []
        pickup_friend = None
        pickup_location = None
        final_pickup_trainhops = float('inf')

        # get the graph from the Graph class
        graph = self.road_graph.get_graph()

        potential_pickup_locations = []

        for i in range(len(graph)):
            friend_hops = graph[i][1]
            if friend_hops[0]:
                potential_pickup_locations.append(friend_hops)

        # Iterating through the potential combinations of pickup locations and updating accordingly
        for friend, pickup, hops in potential_pickup_locations:
            total_time = start_distances[pickup] + destination_distances[pickup]

            if (total_time < final_total_time) or (total_time == final_total_time and hops < final_pickup_trainhops):
                final_total_time = total_time
                pickup_friend = friend
                pickup_location = pickup
                final_pickup_trainhops = hops

        # reconstructing the route
        route = self.route_full_reconstruction(start=start, pickup=pickup_location, destination=destination)

        return final_total_time, route, pickup_friend, pickup_location



    def __str__(self) -> str:
        """
        Function description: Returns a string representation of the graph, showing each vertex and its edges.

        Input: None

        Output:
            A string representation of the graph.

        Time complexity: O(|R|)

        Time complexity analysis: Each vertex and its list of edges in the road graph are iterated over to build the string.

        Space complexity: O(|R|)
        
        Space complexity analysis: The space used for the result list is the number of elements in the road graph.
        """
        result = []
        for i, edges in enumerate(self.road_graph.get_graph()):
            result.append(f"Vertex {i}: {edges}")
        return "\n".join(result)


if __name__ == "__main__":
    roads = []
    tracks = []
    friends = [("Grizz", 0)]
    myCity = CityMap(roads, tracks, friends)
    result = myCity.plan(0, 0)
    (result, (0, [0], "Grizz", 0))

    print(result)


