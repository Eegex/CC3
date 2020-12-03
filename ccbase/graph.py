#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Last modified on Wed Nov 25 12:20:30 2020
Refactored module for holding graphical networks.
@author: jpoeppel
"""

import copy
# A relative import of another module from the same package:
from .nodes import Node

class Graph(object):
    """
        Attributes
        ----------
        nodes: dict
            A dictionary containing node-name:`ccbase.nodes.Node` pairs for all nodes in the graph.
        is_directed: bool, defaults to True
            A boolean indicating if the graph is a directed graph.

    """
    
    def __init__(self):
        self.nodes = {}
        self.is_directed = True
        
    def add_node(self, node):
        """
            Adds a node to the graph. Will first create a new node object
            with the given name.
            
            Parameters
            ----------
            node: String or `ccbase.nodes.Node`
                The name of the new node or the new node directly. In case
                a string is passed, a new node will be created before adding it.
        """
        if node in self.nodes:
            raise ValueError("The graph already contains a node named {}".format(node))
        
        try:
            self.nodes[node.name] = node
        except AttributeError: #We check for an attribute, rather than a type.
            self.nodes[node] = Node(node)
        
    def remove_node(self, node):
        """
            Removes the node with the given name from the graph.
            
            Parameters
            ----------
            node: String
                The name of the new node.

            Raises
            ----------
            ValueError
                If the specified node is not in the graph.
        """
        if not node in self.nodes:
            raise ValueError("The graph does not contain a node named {}".format(node))
        
        self.nodes[node].destroy()
        del self.nodes[node]
        
    def add_edge(self, node_a, node_b):
        """
            Adds a directed edge from node_a to node_b. In this implementation, edges
            are only implictly represented, via parent and child relations in the
            nodes. One could alternatively explicitly represent edge objects that
            connect nodes.
            
            Parameters
            ----------
            node_a: String
                The name of the first node.
            node_b: String
                The name of the second node.

            Raises
            ----------
            ValueError
                If any of the specified nodes are not in the graph.
        """
        try:
            self.nodes[node_a].add_child(self.nodes[node_b])
            self.nodes[node_b].add_parent(self.nodes[node_a])
        except KeyError:
            raise ValueError("At least one of your specified nodes ({},{}) " \
                             "is not contained in the graph".format(node_a, node_b))
            
            
    def remove_edge(self, node_a, node_b):
        """
            Removes an edge from node_a to node_b, if it exists. 
            Non-existing edges are ignored. However, specifying nodes not 
            contained in the graph will raise a ValueError.
            
            Parameters
            ----------
            node_a: String
                The name of the first node.
            node_b: String
                The name of the second node.
        """
        try:
            self.nodes[node_a].remove_child(self.nodes[node_b])
            self.nodes[node_b].remove_parent(self.nodes[node_a])
        except KeyError:
            raise ValueError("At least one of your specified nodes ({},{}) " \
                             "is not contained in the graph".format(node_a, node_b))
            
            
    def get_number_of_nodes(self):
        """
            Returns
            -------
            int
                The total number of nodes in the graph.
        """
        return len(self.nodes)

    # Comment: Properties are the preferred way of not using explicit
    # get_x / set_x methods from other languages. We can discuss how exactly
    # they work in the tutorials, or you can read up on the reasoning behind them
    # at https://www.python-course.eu/python3_properties.php
    @property
    def num_nodes(self):
        """
            Performs the same as "get_number_of_nodes" but as a property.

            Returns
            -------
            int
                The total number of nodes in the graph.
        """
        return len(self.nodes)
    
    def get_parents(self, node, return_names=True):
        """
            Collects and returns all parents of the given node. Should raise an
            exception when the node is not in the graph.

            Parameters
            ----------
            node: String
                The name of the node whose parents are queried.
            return_names: Bool, optional (Default:True)
                Will only return the names of the parents if given, otherwise
                the actual parent node objects will be returned.
                
            Returns
            -------
            list
                A list containing all parent nodes (or their names) of the specified node.
        """
        try:
            if return_names:
                return [n.name for n in self.nodes[node].parents.values()]
            else:
                return list(self.nodes[node].parents.values())
        except KeyError:
            raise ValueError("The graph does not contain a node called {}".format(node))
            
            
    def get_children(self, node, return_names=True):
        """
            Collects and returns all children of the given node. Should raise
            an exception when the node is not in the graph.

            Parameters
            ----------
            node: String
                The name of the node whose children are queried.
            return_names: Bool, optional (Default:True)
                Will only return the names of the children if given, otherwise
                the actual children node objects will be returned.
                
            Returns
            -------
            list
                A list containing all children nodes (or their names) of the specified node.
        """
        try:
            if return_names:
                return [n.name for n in self.nodes[node].children.values()]
            else:
                return list(self.nodes[node].children.values())
        except KeyError:
            raise ValueError("The graph does not contain a node called {}".format(node)) 
            
    def get_ancestors(self, node):
        """
            Parameters
            ----------
            node: String or `ccbase.nodes.Node`
                The name of the node whose ancestors are queried.
                
            Returns
            -------
            list
                A list containing all ancestor nodes of the specified node.
        """
        def _add_parents(tmp_node):
            for p in tmp_node.parents.values():
                if p in res:
                    continue
                res.add(p)
                _add_parents(p)
        res = set()
        _add_parents(self.nodes[node])
        return res

    def is_ancestor(self, node_a, node_b):
        """
            Checks if node_a is an ancestor of node_b. 
            Should also work in cyclic graphs!

            Parameters
            ----------
            node_a: String
                The name of the potential ancestor node.
            node_b: String
                The name of the potential descendant node.

            Returns
            -------
            bool
                True if node_a is an ancestor of node_b, False otherwise.
        """
        # The "in" check works despite node_a being a string an get_ancestors returning
        # a list of node objects, since our node class overwrites the __eq__ method used
        # by the "in" check.
        return node_a in self.get_ancestors(node_b)

    def get_descendants(self, node):
        """
            Parameters
            ----------
            node: String or `ccbase.nodes.Node`
                The name of the node whose descendants are queried.
                
            Returns
            -------
            list
                A list containing all descendant nodes of the specified node.
        """
        def _add_children(tmp_node):
            for p in tmp_node.children.values():
                if p in res:
                    continue
                res.add(p)
                _add_children(p)
        res = set()
        _add_children(self.nodes[node])
        return res

    def is_descendant(self, node_a, node_b):
        """
            Checks if node_a is a descendant of node_b. 
            Should also work in cyclic graphs!

            Parameters
            ----------
            node_a: String
                The name of the potential descendant node.
            node_b: String
                The name of the potential ancestor node.

            Returns
            -------
            bool
                True if node_a is a descendant of node_b, False otherwise.
        """
        return node_b in self.get_ancestors(node_a)
            
    def copy(self, deep=True):
        """
            Copies the current graph.
            
            Parameters
            ----------
            deep: Bool, optional (Default:True)
                If true, a deep copy will be performed, i.e. all nodes are also
                copied. In a shallow copy, both graph instances will contain the
                same node references.
            
            Returns
            -------
            Graph
                Creates a (deep) copy of this graph.
        """
       
        if deep:
            return copy.deepcopy(self)
        else:
             return copy.copy(self)
            
    def to_undirected(self):
        """
            Returns an undirected copy this graph. Sine this implementation
            does not really specify edge directions, we consider a bidrectional
            graph as undirected!
            
            Returns
            -------
            Graph
                An undirected copy of this graph.
        """
        res = self.copy()
        if res.is_directed:
            for n in res.nodes.values():
                for p in n.parents.values():
                    n.add_child(p)
                    p.add_parent(n)
                for c in n.children.values():
                    c.add_child(n)
                    n.add_parent(c)
            res.is_directed = False  
        return res
        