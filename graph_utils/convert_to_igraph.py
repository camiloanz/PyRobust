from igraph import Graph

def convert_to_igraph(graph):
    """Convert graph to an igraph graph with setting the 'name' tags to proper idx."""
    g = Graph()
    g.add_vertices(list(graph.nodes))
    g.add_edges(list(graph.edges))
    
    for idx in range(g.vcount()):
        g.vs[idx]["name"] = idx  

    for idx in range(g.ecount()):
        g.es[idx]["name"] = idx 

    for idx, (node, data) in enumerate(graph.nodes(data=True)):
        for key, value in data.items():
            g.vs[idx][key] = value

    for edge_idx, (source, target, data) in enumerate(graph.edges(data=True)):
        for key, value in data.items():
            g.es[edge_idx][key] = value 

    return g