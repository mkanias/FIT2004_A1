
class Graph:
    def __init__(self, roads, tracks, friends) -> None:
        self.roads = roads
        self.tracks = tracks
        self.friends = friends

        size_initialisation = len(roads) + 1

        self.road_graph = [[[], (None, float('inf'), float('inf'))] for _ in range(size_initialisation)] 

        self.add_edges_undirected()
        self.add_friend_locations()
        self.filter_graph()


    def add_edges_undirected(self) -> None:
        for edge in self.roads:
            start_vertex, end_vertex, weight = edge

            self.road_graph[start_vertex][0].append((start_vertex, end_vertex, weight))
            self.road_graph[end_vertex][0].append((end_vertex, start_vertex, weight))

    
    def add_friend_locations(self) -> None:
        for friend, location in self.friends:
            self.road_graph[location][1] = (friend, location, 0)  # Update the friend's own location

        for edge in self.tracks:
            (start_vertex, end_vertex, weight) = edge

            friend_name = self.road_graph[start_vertex][1][0]
            start_pickup_hops = self.road_graph[start_vertex][1][2]
            end_pickup_hops = self.road_graph[end_vertex][1][2]

            if (friend_name is not None) and (start_pickup_hops < end_pickup_hops) and (start_pickup_hops + 1 <= 2):
                self.road_graph[end_vertex][1] = (friend_name, end_vertex, start_pickup_hops + 1)


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
    roads = [(0,1,4), (0,3,2), (2,0,3), (3,1,2), (2,4,2), (2,5,2)]
    tracks = [(1,3,4), (3,4,2), (4,5,1), (5,1,6)]
    friends = [("Grizz", 1)]

    graph = Graph(roads, tracks, friends) # initialising the space for the adj_list O(|R|)

    print(graph)

    
    
