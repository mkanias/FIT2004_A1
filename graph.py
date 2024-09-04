from collections import deque


class Graph:
    def __init__(self, roads, tracks, friends) -> None:
        size_initialisation = len(roads) + 1

        self.road_graph = [[[], (None, float('inf'), float('inf'))] for _ in range(size_initialisation)] 
        self.track_graph = [[[], (None, float('inf'), float('inf'))] for _ in range(size_initialisation)]

        self.add_edges_undirected(roads)
        self.add_edges_directed(tracks)
        self.multi_source_bfs(friends)
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


    def multi_source_bfs(self, friends):
        queue = deque()
        visited = [False] * len(self.track_graph)

        # Initialize the BFS queue with all friend locations
        for friend, location in friends:
            queue.append((location, 0))  # (node, hops)
            visited[location] = True
            self.road_graph[location][1] = (friend, location, 0)  # Update the friend's own location

        # Perform BFS
        while queue:
            current_node, hops = queue.popleft()

            # Stop if we've reached the hop limit
            if hops == 2:
                continue

            # Explore neighbors
            for _, neighbor, weight in self.track_graph[current_node][0]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append((neighbor, hops + 1))
                    if hops + 1 < self.road_graph[neighbor][1][2]:
                        self.road_graph[neighbor][1] = (self.road_graph[current_node][1][0], neighbor, hops + 1)


    def filter_graph(self):
        empty_element = self.road_graph[-1][0]
        if not empty_element:
            self.road_graph.pop()

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

    graph.multi_source_bfs(friends)
    print(graph)

    
    
