n = 7

graph = [[0, -1, -1, -1, -1, -1, -1],
         [4, 0, -1, -1, -1, -1, -1],
         [5, 6, 0, 3, -1, -1, -1],
         [-1, 3, 4, 0, 4, -1, -1],
         [-1, 10, -1, 6, 0, 2, -1],
         [-1, -1, 9, 3, 3, 0, -1],
         [-1, -1, -1, -1, 2, 2, 0]]

min_distance_graph = [[-1 for i in range(n)] for j in range(n)]
min_distance_graph_direction = [-1 for i in range(n)]


def bellman_ford(source, sink, previous_nodes=[]):
    print(source + 1)

    #Returns the halt situation
    if source == sink:
        min_distance_graph[source][sink] = 0
        return 0

    neighbors = []
    node_distance_to_neighbors = graph[source]

    #Finds the node's neighbors that have not been iterated through
    for distance_to_immediate_nodes_index in range(len(node_distance_to_neighbors)):
        if node_distance_to_neighbors[distance_to_immediate_nodes_index] >= 0:
            if not (distance_to_immediate_nodes_index in previous_nodes):
                if distance_to_immediate_nodes_index != source:
                    neighbors.append(distance_to_immediate_nodes_index)

    distance_to_source_from_neighbors = []
    new_previous_nodes = previous_nodes.copy()
    new_previous_nodes.append(source)

    #Finds the distance to the sink from neighbors
    for neighbor in neighbors:
        min_distance_value = min_distance_graph[neighbor][sink]
        if min_distance_value < 0:
            distance_to_source_from_one_neighbor = bellman_ford(neighbor, sink, new_previous_nodes)
        else:
            distance_to_source_from_one_neighbor = min_distance_value

        if distance_to_source_from_one_neighbor != -1:
            distance_to_source_from_neighbors.append(distance_to_source_from_one_neighbor + node_distance_to_neighbors[neighbor])
        else:
            distance_to_source_from_neighbors.append(-1)


    distance_from_neighbors_that_are_connected = []
    for distance in distance_to_source_from_neighbors:
        if distance >= 0:
            distance_from_neighbors_that_are_connected.append(distance)


    if len(distance_from_neighbors_that_are_connected) == 0:
        return -1

    #Set the direction for each node, so we can know how the shortest path graph looks like
    min_distance = min(distance_from_neighbors_that_are_connected)
    min_distance_index = distance_to_source_from_neighbors.index(min_distance)
    min_distance_graph_direction[source] = neighbors[min_distance_index]


    #Saves the data so it does not need to iterate again
    min_distance_graph[source][sink] = min_distance

    #Corrects the saved data from neighbors if their minimum distance is through this node
    for neighbor in neighbors:
        if graph[neighbor][source] != -1:
            neighbor_min_distance_from_this_node = min_distance + graph[neighbor][source]
            if neighbor_min_distance_from_this_node < min_distance_graph[neighbor][sink]:
                min_distance_graph[neighbor][sink] = neighbor_min_distance_from_this_node
                min_distance_graph_direction[neighbor] = source

    return min_distance


def report_min_distance_results(sink):

    distance_to_sink = []

    for distance_to_neighbors in min_distance_graph:
        distance_to_sink.append(distance_to_neighbors[sink])

    for distance_index in range(len(distance_to_sink)):
        distance_to_sink_for_node = distance_to_sink[distance_index]
        minimum_distance_path_to_sink = min_distance_graph_direction[distance_index]
        if distance_to_sink_for_node == -1:
            print("Distance from node " + str(distance_index + 1) + " to " + str(sink + 1) + " has not been evaluated.")
        else:
            print("Distance from node " + str(distance_index + 1) + " to " + str(sink + 1) + " is " + str(distance_to_sink_for_node) + ("." if minimum_distance_path_to_sink < 0 else (", the goes through node " + str(minimum_distance_path_to_sink + 1) + ".")))


if __name__ == "__main__":
    source = 3
    sink = 2

    minimum_distance = bellman_ford(source - 1, sink - 1)

    if minimum_distance != -1:
        print("Minimum distance from node " + str(source) + " to " + str(sink) + " is " + str(minimum_distance))
    else:
        print("There is no way from source to sink.")

    report_min_distance_results(sink - 1)



