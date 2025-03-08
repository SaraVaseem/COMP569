import collections

def bfs_get_neighbors(graph, node):
    # Todo: implementation-specific approach to get neighbors
    return None

def bfs_is_goal(node, goal):
    # Todo: implementation-specific approach to check goal state
    return None

def breadth_first_search(graph, start, goal):
    # Add the initial node.
    queue = collections.deque([start])

    # Keep track of the visited nodes.
    visited = set([start])

    while queue:
        # Get the first node from the queue.
        node = queue.popleft()

        # Check if the node is the goal.
        if bfs_is_goal(node, goal):
            return node

        # Get the neighbors of the node.
        neighbors = bfs_get_neighbors(graph, node)

        # Add the neighbors to the queue if they haven't been visited yet.
        for neighbor in neighbors:
            # Skip the neighbor if it has already been visited.
            if neighbor not in visited:
                # Add the neighbor to the queue.
                queue.append(neighbor)
                # Track the neighbor as having been visited.
                visited.add(neighbor)
