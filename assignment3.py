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
	# gehe alle knoten durch
	# wenn von dem Knoten mehr als zwei Kanten ausgehen ist es ein Fork?
	forks = []
	for node in dg.nodes:
		if len(dg.get_parents(node)) < 2 and len(dg.get_children(node)) > 1:
			forks.append(node)
	return forks

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
	forks = []
	for node in dg.nodes:
		if len(dg.get_parents(node)) > 1 and len(dg.get_children(node)) < 2:
			forks.append(node)
	return forks

def get_paths(dg, node_x, node_y):
	"""
		Computes all undirected paths between node_x and node_y within
		the graph.

		Parameters A->B B->A B->C und C->B
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

	undirected = dg.to_undirected()
	list = []
	path = []
	paths = []
	search(undirected, node_x, node_y, list, path, paths)
	return paths

def search(graph, node_x, node_y, list, path, paths): 
	list.append(node_x)
	path.append(node_x) 
	if node_x == node_y: 
		paths.append(path.copy())
	else: 
		for child in graph.get_children(node_x): 
			if not child in list: 
				search(graph, child, node_y, list, path, paths) 
	path.pop() 
	list.pop()

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
	parents = 0
	for n in path:
		if n is not node and n in dg.get_parents(node):
			parents += 1
	return parents > 1

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
	open = True
	for index in range(1,len(path) - 1):
		if path[index-1] in dg.get_parents(path[index]) and path[index+1] in dg.get_parents(path[index]):
			open = path[index] in nodes_z
			for child in dg.get_children(path[index]):
				open = open and child in nodes_z
		elif path[index-1] in dg.get_children(path[index]) and path[index+1] in dg.get_children(path[index]):
			open = path[index] not in nodes_z
		else:
			open = path[index] not in nodes_z
		if not open:
			break
	return open

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
	for path in get_paths(dg,node_x,node_y): 
		if is_path_open(dg, path, nodes_z):
				return True
	return False

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
	for node_x in nodes_x:
		for node_y in nodes_y:
			if unblocked_path_exists(dg,node_x,node_y,nodes_z):
				return False
	return True

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
	dg.add_edge("B", "A")
	dg.add_edge("E", "A")
	dg.add_edge("E", "R")
	#dg.add_edge("A", "R") #neu
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
	path = ["B", "A", "E"]
	print("Is A a collider for the path {}? {}".format(path, is_collider(g, "A", path)))
	print("Is path {} open? {}".format(path, is_path_open(g, path, [])))
	nodes_z = ("A", "E")
	print("Is there a path from B to R not blocked by {}? {}".format(
		nodes_z, unblocked_path_exists(g, "B", "R", nodes_z)))
	print("Are Nodes B and R independent given nodes {}?: {}".format(
		nodes_z, check_independence(g, ("B"), ("R"), nodes_z)))
