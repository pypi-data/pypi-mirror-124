import numpy as np
from scipy.sparse import csr_matrix
from collections import deque


class TreeNode:

    def __init__(self, state, parent=None, distance: float = 0.0):
        self.state = state
        self.parent = parent
        self.children = []
        self.depth = 0
        self.distance = distance

        if self.parent is not None:
            self.depth = self.parent.depth + 1

def generate_tree(sparse_matrix: csr_matrix, num_nodes: int) -> []:
    # Get the arrays from the sparse matrix
    M = sparse_matrix.tocoo()

    # The from nodes -> to nodes
    from_nodes = M.row
    to_nodes = M.col
    distances = M.data

    # Create a vector of parents to store the tree
    tree = [None] * num_nodes
    tree[0] = TreeNode(0)

    # Construct the tree from the edges returned by the Kruskal/Prim's algorithm
    return orderIt(from_nodes, to_nodes, distances, tree, 0)  # Start at the root node 0


def orderIt(from_nodes: np.ndarray, to_nodes: np.ndarray, distances: np.ndarray, tree, parent: int) -> []:
    # Get the number of edges
    num_edges: int = from_nodes.size

    # Stack to check which node to check for parent next
    parent_stack = [parent]

    while parent_stack:

        # Get the parent to check for
        parent = parent_stack.pop()

        # Get all the nodes where the from are equal to the parent
        useful_to = to_nodes[from_nodes == parent]
        distances_to = distances[from_nodes == parent]

        # Create new nodes where they do not exist yet
        for i in range(useful_to.size):
            if tree[useful_to[i]] is None:
                tree[useful_to[i]] = TreeNode(useful_to[i], parent=tree[parent], distance=distances_to[i])
                tree[parent].children.append(tree[useful_to[i]])

                # Add the current node to the stack to be checked on
                parent_stack.append(useful_to[i])

        # Get all the inverse nodes
        useful_from = from_nodes[to_nodes == parent]
        distances_from = distances[to_nodes == parent]

        # Create new nodes where they do not exist yet
        for i in range(useful_from.size):
            if tree[useful_from[i]] is None:
                tree[useful_from[i]] = TreeNode(useful_from[i], parent=tree[parent], distance=distances_from[i])
                tree[parent].children.append(tree[useful_from[i]])

                # Add the current node to the stack to be checked on
                parent_stack.append(useful_from[i])

    return tree


def BFS(node: TreeNode) -> np.ndarray:
    # Create a queue to place the next nodes to check
    frontier = deque()
    frontier.append(node)

    last_node = node

    # Iterate until there are no more nodes
    while frontier:
        # Take the first element from the queue
        child = frontier.popleft()

        # Update the last node
        last_node = child

        # Put the children of this node in the queue
        frontier.extend(child.children)

    # Return the list of nodes by backtracking the children
    sequence = np.empty((last_node.depth + 1,), dtype='int')
    distances = np.empty((last_node.depth,), dtype='float')

    while last_node.parent is not None:
        sequence[last_node.depth] = last_node.state
        distances[last_node.depth-1] = last_node.distance
        last_node = last_node.parent

    sequence[last_node.depth] = last_node.state

    return sequence, distances
