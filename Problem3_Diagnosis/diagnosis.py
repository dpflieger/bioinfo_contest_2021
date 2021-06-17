import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import write_dot

input = "D:/GitHub/bioinfo_contest_2021/Problem3_Diagnosis/test1"


def hierarchy_pos(G, root=None, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5):
    '''
    From Joel's answer at https://stackoverflow.com/a/29597209/2966723.  
    Licensed under Creative Commons Attribution-Share Alike 
    
    If the graph is a tree this will return the positions to plot this in a 
    hierarchical layout.
    
    G: the graph (must be a tree)
    
    root: the root node of current branch 
    - if the tree is directed and this is not given, 
      the root will be found and used
    - if the tree is directed and this is given, then 
      the positions will be just for the descendants of this node.
    - if the tree is undirected and not given, 
      then a random choice will be used.
    
    width: horizontal space allocated for this branch - avoids overlap with other branches
    
    vert_gap: gap between levels of hierarchy
    
    vert_loc: vertical location of root
    
    xcenter: horizontal location of root
    '''
    if not nx.is_tree(G):
        raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')

    if root is None:
        if isinstance(G, nx.DiGraph):
            root = next(iter(nx.topological_sort(G)))  #allows back compatibility with nx version 1.11
        else:
            root = random.choice(list(G.nodes))

    def _hierarchy_pos(G, root, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5, pos = None, parent = None):
        '''
        see hierarchy_pos docstring for most arguments

        pos: a dict saying where all nodes go if they have been assigned
        parent: parent of this branch. - only affects it if non-directed

        '''
    
        if pos is None:
            pos = {root:(xcenter,vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        children = list(G.neighbors(root))
        if not isinstance(G, nx.DiGraph) and parent is not None:
            children.remove(parent)  
        if len(children)!=0:
            dx = width/len(children) 
            nextx = xcenter - width/2 - dx/2
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(G,child, width = dx, vert_gap = vert_gap, 
                                    vert_loc = vert_loc-vert_gap, xcenter=nextx,
                                    pos=pos, parent = root)
        return pos

            
    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)

with open(input) as infile:

    # n = number of nodes
    number_of_nodes = int(infile.readline().strip())
    parents_identifiers = [int(s) for s in infile.readline().strip().split()]
    icv = [int(s) for s in infile.readline().strip().split()]
    # m = number of diseases
    number_of_diseases = int(infile.readline().strip())
    diseases_description = [infile.readline().strip().split() for _ in range(number_of_diseases)]
    # key = disease number, value = nodes with the disease
    diseases_nodes = {i[0]: i[1:] for i in diseases_description}
    
    # nq = number of patients
    number_of_patients = int(infile.readline().strip())
    patients_description = [infile.readline().strip().split() for _ in range(number_of_patients)]
     # key = patient number, value = nodes with the disease
    patients_nodes = {i: patients[1:] for i, patients in enumerate(patients_description, start = 1)}

    print(f"number_of_nodes: {number_of_nodes}")
    print(f"parents_identifiers: {parents_identifiers}")
    print(f"icv: {icv}")
    print(f"number_of_diseases: {number_of_diseases}")
    #print(f"diseases_description: {diseases_description}")
    print(f"diseases_nodes: {diseases_nodes}")
    #print(f"patients_description: {patients_description}")
    #print(f"patients_nodes: {patients_nodes}")

    # LCA(q,d) is the lowest common ancestor of phenotype vertex q and phenotype vertex d and
    # IC(v) is the information content of vertex v. If there are several diseases with the same maximal value, then any of them can be returned.

    #G = nx.parse_edgelist(, nodetype = int, data=False, delimiter=" ")
    G = nx.Graph()

    G.add_nodes_from(range(1, number_of_nodes + 1))
    G.add_edges_from(list(zip(parents_identifiers, range(2, number_of_nodes + 1))))

    # Set icv
    nx.set_node_attributes(G, values = dict(zip(range(1, number_of_nodes + 1), icv)), name='icv')
    # Print icv
    #print(nx.get_node_attributes(G, 'icv'))

    #print(G.nodes[1]["icv"])

    #for node in range(1, number_of_nodes + 1):
    #    if node in diseases_nodes.values
    #    G.nodes[node]["disease"] = 

    for disease, nodes in diseases_nodes.items():
        for node in nodes:
            #print(disease, node)
            G.nodes[int(node)]["disease_type"] = int(disease)
    
    #print(nx.get_node_attributes(G, 'disease_type'))
    #print(list(G.nodes(data=True)))
    
    colorlist = []

    for node in range(1, number_of_nodes + 1):
        try: 
            G.nodes[int(node)]["disease_type"]
            colorlist.append("red")
        except KeyError:
            colorlist.append("blue")


    ## See the actual tree
    #pos = hierarchy_pos(G,1)   
    #nx.draw(G, pos= pos, with_labels=True, node_color = colorlist, node_size=10)
    #nx.draw(G.subgraph(["1", "2"]), node_color='red', font_color='green')
    #plt.show()