from node import Node
'''Graph class for general purpouses
David Picornell <dapicar(at)inf(dot)upv(dot)es>
Vicent Blanes <viblasel(at)inf(dot)upv(dot)es>
'''
class Graph:

    def __init__(self):
        '''
        Standar constructor, make a void graph
        '''
        self.nodes = list()

    def __str__(self):
        s = ''
        for i in self.nodes:
            s+= str(i)+'\n'
        return s

    def add_node(self, node):
        self.nodes.append(Node(node))

    def delete_node(self, node):
        self.nodes.remove(node)
        for v in self.nodes:
            v.delete_edge(node)

    def get_node(self, name):
        node = None
        for i in self.nodes:
            if i.name == name:
                node = i
                break
        return node

def test():
    nodes = []
    g = Graph()
    for i in range (5):
        nodes.append(Node(str(i)))
    for n in nodes:
        if n.name == '3':
            g.add_node(n)
            continue
        n.add_multiple_edges(nodes, [10*i for i in range(len(nodes))])
        g.add_node(n)
    print(g)


if __name__ == '__main__':
    test()
