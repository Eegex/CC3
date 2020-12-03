"""
Last modified on Tue Nov 24 15:33 2020
@author: jpoeppel
"""

# Import of the provided graph class. You would
# need to change this line if you plan to use your
# own graph class!

# If you change this, make sure you also import you Graph
# with that name, e.g. if you want to use the assignment1.py file
# directly your import could look like:
# from assignment1.py import DGraph as Graph
# Also make sure to submit your assignment1.py (or whatever you end up)
# calling it, alongside this file so that the imports work!
from ccbase.graph import Graph


###
# Note: If you use your own graph implementation, take care
# that the parameters may be either a node's name or a node's
# object. You do however not need to worry about implementing both
# return types. It will be enough as long as the functions return either
# node objects or the node names (or lists thereof).
###

def find_forks(dg):
    """
        Computes all forks within the given graph.
        
        Parameters
        ----------
        dg: ccbase.graph.Graph
            The graph whose forks are to be computed.
            
        Returns
        ----------
        list of ccbase.nodes.Node or Strings
            A list containing all Nodes (either object or their name/id) that
            represent forks in the network.
    """
    raise NotImplementedError("TODO Exercise 1.1")

def find_colliders(dg):
    """
        Computes all colliders within the given graph.
        
        Parameters
        ----------
        dg: ccbase.graph.Graph
            The graph whose colliders are to be computed.
            
        Returns
        ----------
        list of ccbase.nodes.Node or Strings
            A list containing all Nodes (either object or their name/id) that
            represent colliders in the network.
    """
    raise NotImplementedError("TODO Exercise 1.2")

def get_paths(dg, node_x, node_y):
    """
        Computes all undirected paths between node_x and node_y within
        the graph.

        Parameters
        ----------
        dg: ccbase.graph.Graph
            The graph in which to compute the paths.
        node_x: ccbase.nodes.Node or String
            The node object or name for the first of the two nodes.
        node_y: ccbase.nodes.Node or String
            The node object or name for the second of the two nodes.

        Returns
        --------
        list of lists of ccbase.nodes.Node or Strings
            A list of lists of node objects (or node names) that each represent
            an undirected path from node_x to node_y.
    """
    raise NotImplementedError("TODO Exercise 2.1")


def is_collider(dg, node, path):
    """
        Checks whether or not the given node is a collider with respect to the given
        path.

        Parameters
        ----------
        dg: ccbase.graph.Graph
            The graph that contains at least all the nodes of the given path 
            and their connections.
        node: ccbase.nodes.Node or String
            The node object (or its name) of a node that should be present in the 
            given path, which is to be checked.
        path: list of ccbase.nodes.Node or Strings
            A list of node objects (or node names) that represents
            an undirected path that contains the given node.

        Returns
        ----------
        bool
            True if the given node is a collider with respect to the given path
            within the graph, False otherwise.
    """
    raise NotImplementedError("TODO Exercise 2.2")


def is_path_open(dg, path, nodes_z):
    """ 
        Checks whether or not the given path is open conditioned on the given nodes.

        Parameters
        ---------
        dg: ccbase.graph.Graph
            The graph that should contain all the nodes and their connections.
        path: list of ccbase.nodes.Node or Strings
            A list of node objects (or node names) that represents
            an undirected path between the first and last node of the path within 
            the graph.
        nodes_z: iterable of ccbase.nodes.Node or Strings
            The set of conditioned nodes (or their names), that might influence the 
            paths between node_x and node_y
        
        Returns
        --------
        bool
            False if the path is blocked given given the nodes_z, True otherwise.
        
    """
    raise NotImplementedError("TODO Exercise 2.3")


def unblocked_path_exists(dg, node_x, node_y, nodes_z):
    """
        Computes if there is at least one unblocked undirected path
        between node_x and node_y when considering the nodes in nodes_z.
        
        Parameters
        ---------
        dg: ccbase.graph.Graph
            The graph that should contain all the nodes.
        nodes_x: ccbase.nodes.Node or String
            The first of the two nodes whose paths are to be checked.
        nodes_y: ccbase.nodes.Node or String
            The second of the two nodes whose paths are to be checked.
        nodes_z: iterable of ccbase.nodes.Node or Strings
            The set of conditioned nodes, that might influence the paths 
            between node_x and node_y
            
        Returns
        --------
        bool
            False if all undirected paths between node_x and node_y are blocked 
            given the nodes_z, True otherwise.
    """
    raise NotImplementedError("TODO Exercise 2.4")

def check_independence(dg, nodes_x, nodes_y, nodes_z):
    """
        Computes whether or not nodes in nodes_x are conditionally 
        independend of nodes in nodes_y given nodes in nodes_z.
        
        Parameters
        ---------
        dg: ccbase.graph.Graph
            The graph that should contain all the nodes.
        nodes_x: iterable of ccbase.nodes.Node or String
            The nodes that should be conditionally independent of the nodes
            in nodes_y
        nodes_y: iterable of ccbase.nodes.Node or String
            The nodes that should be conditionally independent of the nodes
            in nodes_x                
        nodes_z: iterable of ccbase.nodes.Node or String
            The set of nodes that should make nodes_x and nodes_y conditionally
            independent.
            
        Returns
        ----------
        bool
            True if all nodes in nodes_x are conditionally independent of all
            nodes in nodes_y given the nodes in nodes_z, False otherwise.
    """
    raise NotImplementedError("TODO Exercise 2.5")

def create_example_graph():
    """
        A method to create a trivial example graph from the 
        lecture. Feel free to create your own methods that generate
        graphs on which you want to test your implementations!

        Returns
        --------
        ccbase.graph.Graph
            A directed graph containing the four nodes A,B,E and R.
    """
    dg = Graph()
    dg.add_node("A")
    dg.add_node("B")
    dg.add_node("E")
    dg.add_node("R")
    dg.add_edge("B","A")
    dg.add_edge("E","A")
    dg.add_edge("E","R")
    return dg

if __name__ == "__main__":
    # Example calls
    g = create_example_graph()
    forks = find_forks(g)
    print("The graph contains the following forks: {}".format(forks))
    assert set(forks) == set(["E"])
    colliders = find_colliders(g)
    print("The graph contains the following colliders: {}".format(colliders))
    assert set(colliders) == set(["A"])

    # Hint: You may want to test these methods with a more complex graph!
    paths = get_paths(g, "B", "R")
    print("Undirected paths from B to R in the graph: {}".format(paths))
    path = ["B","A","E"]
    print("Is A a collider for the path {}? {}".format(is_collider(g, "A", path)))
    print("Is path {} open? {}".format(path, is_path_open(g, path, [])))
    nodes_z = ("A","E")
    print("Is there a path from B to R not blocked by {}? {}".format(nodes_z, unblocked_path_exists(g, "B","R", nodes_z)))
    print("Are Nodes B and R independent given nodes {}?: {}".format(nodes_z, check_independence(g, ("B"), ("R"), nodes_z)))
