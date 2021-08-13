# Course: CS261 - Data Structures
# Author: Joseph Capobianco
# Assignment: 6
# Description: Program will implement a directed, weighted graph
#  with no duplicate edges or loops.

class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #

    def add_vertex(self) -> int:
        """
        Method will add a new vertex to the graph. A vertex name does not
        need to be provided; instead the vertex will be assigned a reference
        index (integer). The first vertex created in the graph will be
        assigned index 0, subsequent vertices will have indexes 1, 2, 3 etc.
        This method will return a single integer - the number of vertices in
        the graph after the addition.
        """

        self.v_count += 1
        self.adj_matrix = [[0 for vertex in range(self.v_count)] for vertexes in range(self.v_count)]
        return self.v_count

    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """
        Method adds a new edge to the graph, connecting the two vertices with
        the provided indices. If either (or both) vertex indices do not exist
        in the graph, or if the weight is not a positive integer, or if src
        and dst refer to the same vertex, the method will do nothing. If an
        edge already exists in the graph, the method will update its weight.
        """

        if weight < 0:
            return None
        elif src > self.v_count - 1 or dst > self.v_count - 1:
            return None
        elif src < 0 or dst < 0:
            return None
        elif src == dst:
            return None
        else:
            self.adj_matrix[src][dst] = weight

    def remove_edge(self, src: int, dst: int) -> None:
        """
        Method removes an edge between the two vertices with the
        provided indices. If either or both vertex indices do not
        exist in the graph, or if there is no edge between them,
        the method will do nothing
        """

        if src > self.v_count - 1 or dst > self.v_count - 1:
            return None
        elif src < 0 or dst < 0:
            return None
        elif self.adj_matrix[src][dst] == 0:
            return None
        else:
            self.adj_matrix[src][dst] = 0

    def get_vertices(self) -> []:
        """
        The method returns a list of the vertices of the graph.
        The order of the vertices in the list does not matter.
        """

        vertices_list = []
        for vertexes in range(self.v_count):
            vertices_list.append(vertexes)
        return vertices_list

    def get_edges(self) -> []:
        """
        Method returns a list of edges in the graph. Each edge
        will be returned as a tuple of two incident vertex indices
        and weight. The first element in the tuple will refer to the
        source vertex, while the second element in the tuple will
        refer to the destination vertex. The third tuple in the element
        will be the weight of the edge. The order of the edges in the
        list does not matter.
        """
        if len(self.adj_matrix) == 0:
            return []
        else:
            edges_list = []
            index_vertex = 0
            for vertexes in range(self.v_count):
                for edges in range(self.v_count):
                    if self.adj_matrix[vertexes][edges] != 0:
                        the_tuple = (vertexes, edges, self.adj_matrix[vertexes][edges])
                        edges_list.append(the_tuple)
            return edges_list

    def is_valid_path(self, path: []) -> bool:
        """
        Method takes a list of vertex indices and returns True if
        the sequence of vertices represents a valid path in the graph.
        Valid paths allow travel from one vertex in the list to the
        last vertex in the list, at each step traversing over an edge
        in the graph. An empty path is considered valid.
        """

        if len(path) == 0 or len(path) == 1:
            return True
        else:
            valid_jumps = 0
            index = 0
            while index < len(path) - 1:
                if self.adj_matrix[path[index]][path[index+1]] != 0:
                    valid_jumps += 1
                    index += 1
                else:
                    return False

            return True

    def dfs(self, v_start, v_end=None) -> []:
        """
        Method performs a depth first search in the graph and
        returns a list of vertices visited during the search,
        in the order they were visited. It takes one required
        parameter, the index of the vertex from which the search
        will start, and one optional parameter - the index of the
        'end' vertex that will stop the search once that vertex
        is reached.

        If the starting vertex is not in the graph, the method will
        return an empty list. If the 'end' vertex is provided but
        is not in the graph, the search should be done as if there
        was no end vertex.

        If several options are available for the next vertex to
        continue the search, the method will pick the vertices by
        vertex index in ascending order.
        """

        vertices_list = []
        vertices_list_stack = []
        if v_start > self.v_count:
            return vertices_list
        elif v_end is None or v_end is not None and v_end > self.v_count:
            vertices_list_stack.append(v_start)
            while len(vertices_list_stack) > 0:
                value = vertices_list_stack[-1]
                vertices_list_stack.remove(value)
                if value not in vertices_list:
                    vertices_list.append(value)
                    for edges in reversed(range(self.v_count)):
                        if self.adj_matrix[value][edges] != 0:
                            vertices_list_stack.append(edges)
            return vertices_list
        else:
            vertices_list_stack.append(v_start)
            while len(vertices_list_stack) > 0 and v_end not in vertices_list:
                value = vertices_list_stack[-1]
                vertices_list_stack.remove(value)
                if value not in vertices_list:
                    vertices_list.append(value)
                    for edges in reversed(range(self.v_count)):
                        if self.adj_matrix[value][edges] != 0:
                            vertices_list_stack.append(edges)
            return vertices_list

    def bfs(self, v_start, v_end=None) -> []:
        """
        This method will work the same as the dfs method but will
        implement a breadth-first search.
        """
        vertices_list = []
        vertices_list_queue = []
        if v_start > self.v_count:
            return vertices_list
        elif v_end is None or v_end is not None and v_end > self.v_count:
            vertices_list_queue.append(v_start)
            while len(vertices_list_queue) > 0:
                value = vertices_list_queue[0]
                vertices_list_queue.remove(value)
                if value not in vertices_list:
                    vertices_list.append(value)
                    for edges in range(self.v_count):
                        if self.adj_matrix[value][edges] != 0:
                            vertices_list_queue.append(edges)
            return vertices_list
        else:
            vertices_list_queue.append(v_start)
            while len(vertices_list_queue) > 0 and v_end not in vertices_list:
                value = vertices_list_queue[0]
                vertices_list_queue.remove(value)
                if value not in vertices_list:
                    vertices_list.append(value)
                    for edges in range(self.v_count):
                        if self.adj_matrix[value][edges] != 0:
                            vertices_list_queue.append(edges)
            return vertices_list

    def has_cycle(self):
        """
        Method will return True if there is at least one cycle in
        the graph. If the graph is acyclic, the method will return
        False.
        """

        index = 0
        while index < self.v_count:
            for edges in range(self.v_count):
                if self.adj_matrix[index][edges] != 0:
                    for connections in range(self.v_count):
                        if self.adj_matrix[edges][connections] != 0:
                            if self.adj_matrix[connections][index] != 0:
                                return True
                            else:
                                for arrows in range(self.v_count):
                                    if self.adj_matrix[connections][arrows] != 0:
                                        if self.adj_matrix[arrows][index] != 0:
                                            return True
            index += 1
        return False

    def dijkstra(self, src: int) -> []:
        """
        Method implements the Dijkstra algorithm to compute the length
        of the shortest path from a given vertex to all other vertices
        in the graph. It returns a list with one value per each vertex
        in the graph, where the value at index 0 is the length of the
        shortest path from vertex SRC to vertex 1 etc. If a certain
        vertex is not reachable from SRC, the returned value should
        be INFINITY (float('inf)). The SRC will be a valid vertex.
        """

        distance_list = []
        dfs_list = self.dfs(src)
        dfs_dict = {}
        index = 0
        while index < self.v_count:
            if index not in dfs_list:
                dfs_dict[index] = float('inf')
                index += 1
            elif dfs_list[index] == src:
                dfs_dict[dfs_list[index]] = 0
                index += 1
            else:
                if self.adj_matrix[dfs_list[index-1]][dfs_list[index]] != 0:
                    new_distance = self.adj_matrix[dfs_list[index-1]][dfs_list[index]]
                    distance = dfs_dict[dfs_list[index-1]] + new_distance
                    dfs_dict[dfs_list[index]] = distance
                    index += 1
                else:
                    test_index = index
                    while self.adj_matrix[dfs_list[test_index-1]][dfs_list[index]] == 0:
                        test_index -= 1
                    value = dfs_dict.get(dfs_list[test_index-1]) + self.adj_matrix[dfs_list[test_index - 1]][dfs_list[index]]
                    dfs_dict[dfs_list[index]] = value
                    index += 1


        number = 0
        while number < self.v_count:
            distance_list.append(dfs_dict.get(number))
            number += 1
        return distance_list









if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = DirectedGraph()
    print(g)
    for _ in range(5):
        g.add_vertex()
    print(g)

    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    for src, dst, weight in edges:
        g.add_edge(src, dst, weight)
    print(g)


    print("\nPDF - method get_edges() example 1")
    print("----------------------------------")
    g = DirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    for path in test_cases:
        print(path, g.is_valid_path(path))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for start in range(5):
        print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)

    edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    for src, dst in edges_to_remove:
        g.remove_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')

    edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0)]
    for src, dst in edges_to_add:
        g.add_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')
    print('\n', g)


    print("\nPDF - dijkstra() example 1")
    print("--------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    g.remove_edge(4, 3)
    print('\n', g)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
