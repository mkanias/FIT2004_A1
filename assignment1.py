from minheap import MinHeap


class CityMap:
    def __init__(self, roads: list[tuple[int,int,int]], tracks: list[tuple[int,int,int]], friends: list[tuple[int,str]]) -> None:
        # define the roads, tracks and friends inputs as class variables 
        self.roads = roads
        self.tracks = tracks
        self.friends = friends

        size_roads = len(self.roads) # findint the size of the roads |R|
        size_tracks = len(self.tracks) # findint the size of the roads |T|

        size_initialisation = max(size_roads, size_tracks) # finding which magnitude is larger

        self.adj_list = [[] for _ in range(size_initialisation)] # initialising the space for the adj_list using the larger magnitude

        # adding the roads and the tracks to the adj_list of the CityMap class
        self.add_roads()
        self.add_tracks()


    def add_roads(self) -> None:
        # looping through each road tuple
        for road in self.roads:
            start_vertex, end_vertex, time = road

            self.adj_list[start_vertex].append((end_vertex, time, "R")) # adding edge btw vertices and identfying that it's a road
            self.adj_list[end_vertex].append((start_vertex, time, "R")) # adding the opposite way coz its undirected

    
    def add_tracks(self) -> None:
        # looping through each road tuple
        for track in self.tracks:
            (start_vertex, end_vertex, time) = track

            self.adj_list[start_vertex].append((end_vertex, time, "T")) # adding edge btw vertices and identfying that it's a track which is one directional



    def dijkstras(self, start_node: int, end_node: int = None, edge_type_input: str = "R"): # optional end node parameter and edge_type
        # initialise distance and parent structues
        # the * method works bc the list items that are being initialised are immutable and therefore they are all independent copies
        distance = [float('inf')] * len(self.adj_list) # all distances are infinity
        parent = [-1] * len(self.adj_list) # all parents are -1

        distance[start_node] = 0 # the distance from the start vertex to itself is 0

        # initialise the priority queue with all vertices
        priority_queue = MinHeap()
        priority_queue.insert(start_node, 0)

        while not priority_queue.is_empty():
            u, dist_u = priority_queue.extract_min() # extract vertex with minimum distance

            # stop if the end node is reached because thats all we need to traverse
            if end_node is not None and u == end_node:
                break


            # relaxation step
            for v, weight, edge_type in self.adj_list[u]: 
                if edge_type == edge_type_input: # making sure to traverse the roads and tracks separately
                    if distance[u] + weight < distance[v]:
                        distance[v] = distance[u] + weight
                        parent[v] = u
                        priority_queue.insert(v, distance[v])

        # reconstructing shortest path if end node is provided
        if end_node is not None:
            path = []
            current = end_node
            while current != -1:
                path.append(current)
                current = parent[current]
            path.reverse()
            return distance[end_node], path

        # if not, then just return the distance and parent lists
        return distance, parent



    def __str__(self) -> str:
        result = []
        for i, edges in enumerate(self.adj_list):
            if edges: # only printing out the vertices that have values in them
                result.append(f"Vertex {i}: {edges}")
        return "\n".join(result)


    def plan(self, start: int, destination: int) -> tuple: # (total_time, route, pickup_friend, pickup_location)
        pass



if __name__ == "__main__":
    roads = [(0,1,4), (0,3,2), (2,0,3), (3,1,2), (2,4,2), (4,5,3)]
    tracks = [(1,3,3), (3,4,2), (4,3,2), (4,5,4), (5,1,6)]
    cm = CityMap(roads,tracks,friends=[])

    print(cm.dijkstras(start_node=1))


