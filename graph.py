class Graph:
    def __init__(self, roads, tracks, friends) -> None:
        size_initialisation = len(roads) + 1

        self.road_graph = [[[], (None, float('inf'), float('inf'))] for _ in range(size_initialisation)] 
        self.track_graph = [[[], (None, float('inf'), float('inf'))] for _ in range(size_initialisation)]

        self.add_edges_undirected(roads)
        self.add_edges_directed(tracks)
        self.add_friends(friends)
        self.filter_graph()


    def add_edges_undirected(self, edge_list) -> None:
        for edge in edge_list:
            start_vertex, end_vertex, weight = edge

            self.road_graph[start_vertex][0].append((start_vertex, end_vertex, weight))
            self.road_graph[end_vertex][0].append((end_vertex, start_vertex, weight))

    
    def add_edges_directed(self, edge_list) -> None:
        for edge in edge_list:
            (start_vertex, end_vertex, weight) = edge

            self.track_graph[start_vertex][0].append(edge) 


    def add_friends(self, friends) -> None:
        for friend, location in friends:
            valid_pickups_hops = self.bfs_within_two_hops(start=location)

            for pickup, hops in valid_pickups_hops:
                if hops < self.road_graph[pickup][1][1]:
                    self.road_graph[pickup][1] = (friend, pickup, hops)

    def filter_graph(self):
        empty_element = self.road_graph[-1][0]
        if not empty_element:
            self.road_graph.pop()


    def bfs_within_two_hops(self, start) -> list[int]:
        # initialise the values
        queue = [(start, 0)]  # (current_node, hops)
        visited = [False] * len(self.track_graph)  # track visited nodes
        visited[start] = True
        nodes_within_two_hops = []  # store nodes within 2 hops

        nodes_within_two_hops.append((start,0))

        while queue:
            current_node, hops = queue.pop(0)  # dequeue the first element

            # Stop if we've reached the hop limit
            if hops == 2:
                continue

            # Explore neighbors
            for node, neighbor, weight in self.track_graph[current_node][0]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append((neighbor, hops + 1))  # enqueue with incremented hops
                    nodes_within_two_hops.append((neighbor, hops + 1))

        return nodes_within_two_hops
    
    def get_graph(self):
        return self.road_graph
    

    def __len__(self):
        return len(self.road_graph)


    def __str__(self) -> str:
        result = []
        for i, edges in enumerate(self.road_graph):
            result.append(f"Vertex {i}: {edges}")
        return "\n".join(result)

if __name__ == "__main__":
    roads = [(0,1,4), (0,3,2), (2,0,3), (3,1,2), (2,4,2), (4,5,3)]
    tracks = [(1,3,3), (3,4,2), (4,3,2), (4,5,4), (5,1,6)]
    friends = [("Grizz", 1), ("Ice", 3)]    

    graph = Graph(roads, tracks, friends) # initialising the space for the adj_list O(|R|)

    print(graph)

    
    
