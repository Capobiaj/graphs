# Course: CS261 - Data Structures
# Author: Joseph Capobianco
# Assignment: 6
# Description: Program will implement an undirected, unweighted, no duplicate
# edges, and no loops graph.


class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------------------------------------------ #

    def add_vertex(self, v: str) -> None:
        """
        Method adds a new vertex to the graph. Vertex names can be any
        string. If a vertex with the same name is already present in the
        graph, the method will do nothing.
        """

        if v in self.adj_list.keys():
            return None
        else:
            self.adj_list[v] = []

    def add_edge(self, u: str, v: str) -> None:
        """
        Method adds a new edge to the graph, connecting two vertices with
        the provided names. If either or both vertex names do not exist in
        the graph, the method will first create them and then create an
        edge between them. If an edge already exists in the graph, or if
        u and v refer to the same vertex, the method will do nothing.
        """

        if u != v:
            if u not in self.adj_list.keys() and v not in self.adj_list.keys():
                self.add_vertex(u)
                self.add_vertex(v)
                u_list = self.adj_list.get(u)
                u_list.append(v)
                v_list = self.adj_list.get(v)
                v_list.append(u)
                return None
            elif u in self.adj_list.keys() and v not in self.adj_list.keys():
                self.add_vertex(v)
                u_list = self.adj_list.get(u)
                u_list.append(v)
                v_list = self.adj_list.get(v)
                v_list.append(u)
                return None
            elif u not in self.adj_list.keys() and v in self.adj_list.keys():
                self.add_vertex(u)
                u_list = self.adj_list.get(u)
                u_list.append(v)
                v_list = self.adj_list.get(v)
                v_list.append(u)
                return None
            else:
                # for loops check to see if edge already exists
                for values in self.adj_list.get(u):
                    if values == v:
                        return None
                for values in self.adj_list.get(v):
                    if values == u:
                        return None
                # otherwise adds edge
                u_list = self.adj_list.get(u)
                u_list.append(v)
                v_list = self.adj_list.get(v)
                v_list.append(u)
                return None
        else:
            return None

    def remove_edge(self, v: str, u: str) -> None:
        """
        Method removes an edge between two vertices with the provided
        names. If either or both vertex names do not exist in the
        graph, or if there is no edge between them, the method
        will do nothing.
        """

        u_list = self.adj_list.get(u)
        v_list = self.adj_list.get(v)
        if v not in self.adj_list.keys() or u not in self.adj_list.keys():
            return None
        elif v not in u_list and u not in v_list:
            return None
        else:
            u_list.remove(v)
            v_list.remove(u)
            return None

    def remove_vertex(self, v: str) -> None:
        """
        Method removes a vertex with a given name and all edges that
        are incident to it from the graph. If the given vertex does
        not exist, the method will do nothing.
        """
        if v in self.adj_list.keys():
            del self.adj_list[v]
            for values in self.adj_list:
                value_list = self.adj_list.get(values)
                for things in value_list:
                    if things == v:
                        value_list.remove(v)
            return None
        else:
            return None

    def get_vertices(self) -> []:
        """
        Method returns a list of vertices of the graph. The order of the
        vertices in the list does not matter.
        """

        vertice_list = []
        for values in self.adj_list.keys():
            vertice_list.append(values)
        return vertice_list

    def get_edges(self) -> []:
        """
        Method returns a list of edges in the graph. Each edge
        is returned as a tuple of two incident vertex names. The
        order of the edges in the list or the order of the vertices
        incident to each edge does not matter.
        """

        edges_list = []
        for values in self.adj_list.keys():
            value_list = self.adj_list.get(values)
            for things in value_list:
                if (things, values) not in edges_list:
                    edges_list.append((values, things))
        return edges_list

    def is_valid_path(self, path: []) -> bool:
        """
        Method takes a list of vertex names and returns True if the
        sequence of vertices represents a valid path in the graph
        so that one can travel from the first vertex in the list to
        the last vertex in the list by traversing over an edge in
        the graph for each step. An empty path will be considered valid.
        """

        if len(path) == 0:
            return True
        elif len(path) == 1:
            if path[0] in self.adj_list.keys():
                return True
            else:
                return False
        else:
            match = 0
            completed = len(path) - 1
            index = 0
            while index < completed:
                if path[index] in self.adj_list.keys():
                    value_list = self.adj_list.get(path[index])
                    if path[index+1] in value_list:
                        match += 1
                        index += 1
                    else:
                        index += 1
            if match == completed:
                return True
            else:
                return False

    def dfs(self, v_start, v_end=None) -> []:
        """
        Method performs a depth first search in the graph and returns
        a list of vertices visited during the search in the order that
        they were visited. The method takes one required parameter,
        name of the vertex from which the search will start, and one
        optional parameter - the name of the 'end' vertex that will
        stop the search when reached.
        If the starting vertex is not in the graph, the method will
        return an empty list. If the name of the 'end' vertex is provided
        but is not in the graph, the search should be done as if there
        was no end vertex.
        When there are several options available for picking the next
        vertex to continue the search, the method will pick the vertices
        in ascending lexicographical order.
        """

        reachable_list = []
        stack_list = []
        if v_start not in self.adj_list.keys():
            return reachable_list
        else:
            if v_end != None and v_end not in self.adj_list.keys() or v_end == None:
                stack_list += v_start
                while len(stack_list) > 0:
                    value = stack_list[-1]
                    stack_list.remove(value)
                    if value not in reachable_list:
                        reachable_list += value
                        value_list = self.adj_list.get(value)
                        value_list.sort(reverse=True)
                        for things in value_list:
                            stack_list.append(things)
                return reachable_list
            else:
                stack_list += v_start
                while len(stack_list) > 0 and v_end not in reachable_list:
                    value = stack_list[-1]
                    stack_list.remove(value)
                    if value not in reachable_list:
                        reachable_list += value
                        value_list = self.adj_list.get(value)
                        value_list.sort(reverse=True)
                        for things in value_list:
                            stack_list.append(things)
                return reachable_list

    def bfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during BFS search
        Vertices are picked in alphabetical order
        """

        reachable_list = []
        queue_list = []
        if v_start not in self.adj_list.keys():
            return reachable_list
        else:
            if v_end != None and v_end not in self.adj_list.keys() or v_end == None:
                queue_list += v_start
                # queue is inserted from back and deleted from front
                while len(queue_list) > 0:
                    value = queue_list[0]
                    queue_list.remove(value)
                    if value not in reachable_list:
                        reachable_list += value
                        value_list = self.adj_list.get(value)
                        value_list.sort()
                        for things in value_list:
                            queue_list.append(things)
                return reachable_list
            else:
                queue_list += v_start
                # queue is inserted from back and deleted from front
                while len(queue_list) > 0 and v_end not in reachable_list:
                    value = queue_list[0]
                    queue_list.remove(value)
                    if value not in reachable_list:
                        reachable_list += value
                        value_list = self.adj_list.get(value)
                        value_list.sort()
                        for things in value_list:
                            queue_list.append(things)
                return reachable_list

    def count_connected_components(self) -> int:
        """
        Method returns the number of connected components in the
        graph.
        """

        connected_components = 0
        value_list = {}
        queue_list = []
        index = 0
        key_list = self.get_vertices()
        while index < len(self.get_vertices()):
            if key_list[index] not in value_list.keys():
                queue_list.append(key_list[index])
                while len(queue_list) is not 0:
                    value = queue_list[0]
                    queue_list.remove(value)
                    if value not in value_list.keys():
                        if len(self.adj_list.get(value)) is 0:
                            value_list[value] = 1
                        else:
                            value_list[value] = 1
                            for connections in self.adj_list.get(value):
                                if connections not in value_list:
                                    queue_list.append(connections)
                connected_components += 1
            else:
                index += 1
        return connected_components

    def has_cycle(self) -> bool:
        """
        Method returns True if there is at least one cycle in
        the graph. If the graph is acyclic, the method will
        return False.
        """

        value_list = {}
        queue_list = []
        index = 0
        last_node = 0
        key_list = self.get_vertices()
        while index < len(self.get_vertices()):
            if len(self.adj_list.get(key_list[index])) > 0:
                if key_list[index] not in value_list.keys():
                    queue_list.append(key_list[index])
                    while len(queue_list) is not 0:
                        value = queue_list[0]
                        queue_list.remove(value)
                        if value not in value_list.keys():
                            value_list[value] = [1, last_node]
                            last_node = value
                            connection_counter = 0
                            for connections in self.adj_list.get(value):
                                if connections not in value_list:
                                    queue_list.append(connections)
                                else:
                                    if value_list.get(connections)[1] != last_node:
                                        connection_counter += 1
                                        if connection_counter > 1:
                                            return True
                else:
                    index += 1
            else:
                index += 1
        return False


   


if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = UndirectedGraph()
    print(g)

    for v in 'ABCDE':
        g.add_vertex(v)
    print(g)

    g.add_vertex('A')
    print(g)

    for u, v in ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', ('B', 'C')]:
        g.add_edge(u, v)
    print(g)


    print("\nPDF - method remove_edge() / remove_vertex example 1")
    print("----------------------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    g.remove_vertex('DOES NOT EXIST')
    g.remove_edge('A', 'B')
    g.remove_edge('X', 'B')
    print(g)
    g.remove_vertex('D')
    print(g)


    print("\nPDF - method get_vertices() / get_edges() example 1")
    print("---------------------------------------------------")
    g = UndirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE'])
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '', 'D', 'Z']
    for path in test_cases:
        print(list(path), g.is_valid_path(list(path)))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = 'ABCDEGH'
    for case in test_cases:
        print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')
    print('-----')
    for i in range(1, len(test_cases)):
        v1, v2 = test_cases[i], test_cases[-1 - i]
        print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')


    print("\nPDF - method count_connected_components() example 1")
    print("---------------------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print(g.count_connected_components(), end=' ')
    print()


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG',
        'add FG', 'remove GE')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print('{:<10}'.format(case), g.has_cycle())
