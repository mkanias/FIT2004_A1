from minheap import MinHeap


class CityMap:
    def __init__(self, roads: list[tuple[int,int,int]], tracks: list[tuple[int,int,int]], friends: list[tuple[int,str]]) -> None:
        # define the roads, tracks and friends inputs as class variables 
        self.roads = roads
        self.tracks = tracks
        self.friends = friends

        size_initialisation = len(self.roads) + 1 # O(|R|) + O(1) => O(|R|)

        self.adj_list = [[] for _ in range(size_initialisation)] # initialising the space for the adj_list O(|R|)

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
        # the * method works bc the list items that are being initialised are immutable and therefore they are all independent copies
        distance = [float('inf')] * len(self.adj_list) # all distances are infinity
        parent = [-1] * len(self.adj_list) # all parents are -1
        train_hops = [0] * len(self.adj_list) # keeping track of the train hops to ensure that the pickup location doesnt exceed 2 stop away

        distance[start_node] = 0 # the distance from the start vertex to itself is 0

        # initialise the priority queue with the start_node havinng a distance of 0
        priority_queue = MinHeap()
        priority_queue.insert(start_node, 0)

        while not priority_queue.is_empty():
            u, dist_u = priority_queue.extract_min() # extract vertex with minimum distance

            # stop if the end node is reached because thats all we need to traverse
            if end_node is not None and u == end_node:
                break

            # relaxation step
            for v, weight, edge_type in self.adj_list[u]: 
                if edge_type_input == edge_type: # making sure to traverse the roads and tracks separately

                    if edge_type == "T" and train_hops[u] < 2: # checking if the pickup node in within 2 nodes distance
                        if distance[u] + weight < distance[v]:
                            distance[v] = distance[u] + weight
                            parent[v] = u
                            train_hops[v] = train_hops[u] + 1 # incrementing the train_hops
                            priority_queue.insert(v, distance[v])

                    elif edge_type != "T": # traversing just the roads
                        if distance[u] + weight < distance[v]:
                            distance[v] = distance[u] + weight
                            parent[v] = u
                            priority_queue.insert(v, distance[v])

        # reconstructing shortest path if end node is provided
        if end_node is not None:
            path = self.route_reconstruction(start=end_node, parents=parent)
            return distance[end_node], path

        # if not, then just return the distance and parent lists
        return distance, parent, train_hops
    

    def route_reconstruction(self, start: int, parents: list[int]) -> list[int]:
        path = []
        current = start
        while current != -1:
            path.append(current)
            current = parents[current]
        path.reverse()
        return path
    

    def get_valid_pickup_locations(self, dist_parent_tuple: tuple[list[int], list[int]]) -> list[tuple[int]]:
        distance, parent, train_hops = dist_parent_tuple
        pickuplocation_distance_trainhops = []
        for i in range(len(distance)):
            if not distance[i] == float('inf'):
                pickuplocation_distance_trainhops.append((i, distance[i], train_hops[i]))

        return pickuplocation_distance_trainhops



    def plan(self, start: int, destination: int) -> tuple: # (total_time, route, pickup_friend, pickup_location)
        start_distances, start_parents, _ = self.dijkstras(start_node=start) # finding shortest distance from start to all other nodes
        destination_distances, destination_parents, _ = self.dijkstras(start_node=destination) # finding shortest distance from destination to all other nodes

        # initialising final values
        final_total_time = float('inf')
        route = []
        pickup_friend = None
        pickup_location = None
        final_dist_pickup_from_friend = None
        final_pickup_trainhops = float('inf')

        for friend, friend_location in self.friends:
            dist_parent_trainhop = self.dijkstras(start_node=friend_location, edge_type_input="T") # finding distances from friend location to all other locations
            friendpickup_distpickup_trainhops_tuple = self.get_valid_pickup_locations(dist_parent_tuple=dist_parent_trainhop)

            for friend_valid_pickup_location, dist_pickup_from_friend, pickup_trainhops in friendpickup_distpickup_trainhops_tuple:
                total_time = start_distances[friend_valid_pickup_location] + destination_distances[friend_valid_pickup_location] + dist_pickup_from_friend

                if (total_time < final_total_time) or (total_time == final_total_time and pickup_trainhops < final_pickup_trainhops):
                    final_total_time = total_time
                    pickup_friend = friend
                    pickup_location = friend_valid_pickup_location
                    final_pickup_trainhops = pickup_trainhops
                    final_dist_pickup_from_friend = dist_pickup_from_friend

                    route_start_pickup = self.route_reconstruction(start=pickup_location, parents=start_parents)
                    route_pickup_destination = self.route_reconstruction(start=destination, parents=destination_parents)                        
                    
                    # reconstructing the final route
                    _, route_pickup_destination = self.dijkstras(start_node=pickup_location, end_node=destination)
                    route = route_start_pickup[:-1] + route_pickup_destination

        # getting rid of the distance of pickup from final time
        final_total_time = final_total_time - final_dist_pickup_from_friend

        return final_total_time, route, pickup_friend, pickup_location



    def __str__(self) -> str:
        result = []
        for i, edges in enumerate(self.adj_list):
            if edges: # only printing out the vertices that have values in them
                result.append(f"Vertex {i}: {edges}")
        return "\n".join(result)


if __name__ == "__main__":
    roads = [(0,1,4), (0,3,2), (2,0,3), (3,1,2), (2,4,2), (4,5,3)]
    tracks = [(1,3,3), (3,4,2), (4,3,2), (4,5,4), (5,1,6)]
    friends = [("Grizz", 1), ("Ice", 3)]

    myCity = CityMap(roads,tracks,friends)
    
    print(myCity)
