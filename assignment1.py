from minheap import MinHeap
from graph import Graph

class CityMap:
    def __init__(self, roads: list[tuple[int,int,int]], tracks: list[tuple[int,int,int]], friends: list[tuple[int,str]]) -> None:
        # define the roads, tracks and friends inputs as class variables 
        self.road_graph = Graph(roads, tracks, friends)


    def dijkstras(self, start_node: int, end_node: int = None): # optional end node parameter and edge_type
        # the * method works bc the list items that are being initialised are immutable and therefore they are all independent copies
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
        path = []
        current = end
        while current != -1:
            path.append(current)
            current = parents[current]
        path.reverse()
        return path

    def route_full_reconstruction(self, start: int, pickup: int, destination: int) -> list[int]:
        route_half_1 = self.dijkstras(start_node=start, end_node=pickup)
        route_half_2 = self.dijkstras(start_node=pickup, end_node=destination)

        route_half_1.pop() # removing the pickup spot

        route = route_half_1 + route_half_2

        return route

    def plan(self, start: int, destination: int) -> tuple: # (total_time, route, pickup_friend, pickup_location)
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
        result = []
        for i, edges in enumerate(self.road_graph.get_graph()):
            result.append(f"Vertex {i}: {edges}")
        return "\n".join(result)


if __name__ == "__main__":
    roads = []
    tracks = []
    friends = [("Grizz", 0)]
    myCity = CityMap(roads, tracks, friends)
    # result = myCity.plan(0, 0)
    # (result, (0, [0], "Grizz", 0))

    print(myCity)


