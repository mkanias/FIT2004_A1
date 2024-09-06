class Graph:
    """  
    Class description: 
    This class represents a graph with roads, tracks, and friends. It is designed to take an input of roads, tracks and friends and 
    make a graph data structure in an efficient way which enables a traversal to find the shortest path given that a friend
    needs to be picked up within 2 train hops of their starting location. The graph is stored as an adjacency list, where vertices 
    represent locations, and edges represent connections between locations (roads). 
    """
    def __init__(self, roads, tracks, friends) -> None:
        """
        Function description: Initialises the graph with roads, tracks, and friends data. It constructs the road graph
        using an adjacency list and associates friends with their respective locations, also updating train hops for valid 
        locations that are within 2 train stops.

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
        
        Space complexity analysis: The space we are initialising for the adjacency list is the length of 
        the roads list + 1, the space complexity becomes O(|R|). And since the graph is connected and simple, 
        the number of locations |L| will not exceed |R| + 1, so the space complexity is dominated by the number of roads.
        """
        self.roads = roads
        self.tracks = tracks
        self.friends = friends

        size_initialisation = len(roads) + 1  # Adjust size based on the number of roads and locations

        # Initialize the adjacency list for the road graph
        self.road_graph = [[[], (None, float('inf'), float('inf'))] for _ in range(size_initialisation)] 

        self.add_edges_undirected()  # Add the undirected roads to the graph
        self.add_friend_locations()  # Update the graph with friend locations and their train hops
        self.filter_graph()  # Remove any unconnected vertices from the graph


    def add_edges_undirected(self) -> None:
        """
        Description:
        This method adds undirected edges (roads) to the graph's adjacency list. For each road, 
        it adds the edge to both the start and end vertices, ensuring that the edge is represented 
        in both directions, since the graph is undirected.

        - For each road, the method adds the edge to the adjacency list of the start vertex.
        - It then adds the reverse of the same edge to the adjacency list of the end vertex, 
        ensuring that both directions are accounted for in the undirected graph.

        Input: 
            - None

        Output: 
            - None

        Time Complexity: O(|R|), where |R| is the number of roads.

        Time Complexity Analysis:
        - The method iterates over each road once, adding edges in both directions, which results in O(|R|) complexity.

        Space Complexity: O(1)

        Space Complexity Analysis:
        - No additional space is used beyond updating the existing graph structure.
        """
        for edge in self.roads:
            start_vertex, end_vertex, weight = edge

            self.road_graph[start_vertex][0].append((start_vertex, end_vertex, weight))
            self.road_graph[end_vertex][0].append((end_vertex, start_vertex, weight))


    def add_friend_locations(self) -> None:
        """
        Description: 
        This method updates the graph to reflect the valid pickup locations of friends by calculating the number of train hops 
        needed to reach other locations within 2 train stops. It works by:
        
        1. Assigning each friend to their starting location in the graph with 0 train hops.
        2. Iterating over all the tracks and checking if there's a friend at the start of each track.
        3. If a friend is found, the method checks whether reaching the destination location via this track 
        would reduce the number of train hops.
        4. If the new number of train hops (current + 1) is less than 2 and less than the existing hops at the 
        destination, it updates the destination with the friend's name and the updated train hops.

        Input: 
            - None 
            
        Output:
            - None

        Time Complexity: O(|T| + |F|), where:
            - |T| is the number of tracks.
            - |F| is the number of friends.

        Time Complexity Analysis:
            - O(|F|) when looping through self.friends and assigning each friend to their starting location.
            - O(|T|) when iterating over all tracks and updating train hops.

        Space Complexity: O(1)
        
        Space Complexity Analysis:
            - The method uses no extra space, as it only updates the existing graph data.
        """
        # Assign each friend to their initial location with 0 train hops
        for friend, location in self.friends:
            self.road_graph[location][1] = (friend, location, 0)  # Update friend's info at their starting location

        # Iterate over all tracks to update train hops based on friends' locations
        for start_vertex, end_vertex, weight in self.tracks:
            friend_name = self.road_graph[start_vertex][1][0]  # Get the friend's name at the start vertex
            start_hops = self.road_graph[start_vertex][1][2]   # Get current hops at the start vertex
            end_hops = self.road_graph[end_vertex][1][2]       # Get current hops at the end vertex

            # If there's a friend at the start vertex and the path to the end vertex has fewer hops, update it
            if (friend_name is not None) and (start_hops + 1 <= 2) and (start_hops + 1 < end_hops):
                self.road_graph[end_vertex][1] = (friend_name, end_vertex, start_hops + 1)  # Update destination with friend and hops


    def filter_graph(self) -> None:
        """
        Function description: Removes any empty vertices from the graph that are not connected to any edges if there
        is more than 1 element already in the adjacency list.

        Input: None

        Output: None
        
        Time complexity: O(1)
        
        Time complexity analysis: Only checks the last element of the graph.

        Space complexity: O(1)
        
        Space complexity analysis: No extra space is used, it simply modifies the existing structure.
        """
        existing_element = self.road_graph[-1][0]
        if len(self.road_graph) > 1 and not existing_element:
            self.road_graph.pop()


    def get_graph(self) -> list:
        """
        Function description: Returns the graph's adjacency list structure.

        Input: None

        Output:
            The adjacency list structure of the graph.

        Time complexity: O(1)

        Space complexity: O(1)
        """
        return self.road_graph
    

    def __len__(self) -> int:
        """
        Function description: Returns the number of vertices in the graph.

        Input: None

        Output:
            The number of vertices in the graph.

        Time complexity: O(1)

        Space complexity: O(1)
        """
        return len(self.road_graph)


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
        for i, edges in enumerate(self.road_graph):
            result.append(f"Vertex {i}: {edges}")
        return "\n".join(result)

if __name__ == "__main__":
    roads = [(0,1,4), (0,3,2), (2,0,3), (3,1,2), (2,4,2), (2,5,2)]
    tracks = [(1,3,4), (3,4,2), (4,5,1), (5,1,6)]
    friends = [("Grizz", 1)]

    graph = Graph(roads, tracks, friends) # initialising the space for the adj_list O(|R|)

    print(graph)

    
    
