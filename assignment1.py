from minheap import MinHeap


class CityMap:
    def __init__(self, roads: list[tuple[int,int,int]], tracks: list[tuple[int,int,int]], friends: list[tuple[int,str]]) -> None:
        # define the roads, tracks and friends inputs as class variables 
        self.roads = roads
        self.tracks = tracks
        self.friends = friends

        size_initialisation = len(self.roads) + 1 # O(|R|) + O(1) => O(|R|)

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
            path = []
            current = end_node
            while current != -1:
                path.append(current)
                current = parent[current]
            path.reverse()
            return distance[end_node], path

        # if not, then just return the distance and parent lists
        return distance, parent, train_hops
    

    def get_valid_pickup_locations(self, dist_parent_tuple: tuple[list[int], list[int]]) -> list[tuple]:
        distance, parent, train_hops = dist_parent_tuple
        valid_pickuplocation_distance_trainhops = []
        for i in range(len(distance)):
            if not distance[i] == float('inf'):
                valid_pickuplocation_distance_trainhops.append((i, distance[i], train_hops[i]))

        return valid_pickuplocation_distance_trainhops



    def plan(self, start: int, destination: int) -> tuple: # (total_time, route, pickup_friend, pickup_location)
        final_route_time = float('inf') # (total_time, route, pickup_friend, pickup_location, train_stops)
        train_stations_travelled_to = float('inf')
        final_distance_from_friend = 0

        for friend_location in self.friends:
            friend, initial_location = friend_location

            # get the valid routes for the first friend
            location_dist_nodedist = self.get_valid_pickup_locations(self.dijkstras(start_node=initial_location, edge_type_input="T"))

            for pickup_location, distance_from_friend, nodedistance in location_dist_nodedist:
                distance_pickup, path_pickup = self.dijkstras(start_node=start, end_node=pickup_location)
                distance_to_end, path_to_end = self.dijkstras(start_node=pickup_location, end_node=destination)

                total_time = distance_pickup + distance_to_end + distance_from_friend


                if (total_time < final_route_time) or ((total_time == final_route_time) and (nodedistance < train_stations_travelled_to)):
                    final_route_time = total_time
                    path_pickup.pop() # popping the pickup location so it isnt repeated in the final route
                    route = path_pickup + path_to_end
                    pickup_friend = friend
                    final_pickup_location = pickup_location
                    final_distance_from_friend = distance_from_friend 

        final_route_time = final_route_time - final_distance_from_friend # update the final route time to not include the time travelled by friend on train

        return final_route_time, route, pickup_friend, final_pickup_location


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
    
    print(myCity.plan(start=2, destination=5))


