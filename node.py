'''
Node for Graph class
David Picornell <dapicar(at)inf(dot)upv(dot)es>
Vicent Blanes <viblasel(at)inf(dot)upv(dot)es>
'''
class Node:

      def __init__(self, name, edges = None):
          self.name = name
          self.edges = [] if edges is None else edges


      def __str__(self):
          s = str(self.name) +' -> '
          for e in self.edges:
              s+='('+str(e[0].name)+", "+str(e[1])+')\n\t'
          return s

      def add_edge(self, vertex, weight=0):
          '''
          vertex: an other node object
          weight: weight of the arc self -> otherVertex
          '''
          self.edges.append((vertex, weight))


      def add_multiple_edges(self, vertices, weights = None):
          '''
          vertices: list of node objects
          weights (optional): list of numbers
          '''
          if weights is None:
              weights = [0 for v in vertices]
          for i in range(len(vertices)):
              self.edges.append(tuple((vertices[i], weights[i])))

      def edge_list(self):
          return self.edges

      def delete_edge(self, node):
          for n in self.edges:
              if n == self:
                  self.edges.remove(node)
                  break
