import networkx as nx
import xml.etree.ElementTree as ET

def load_networkx_graph_from_xml(xml_filepath):
    """
    Liest einen Graphen aus einer XML-Datei und gibt ihn als NetworkX-Graph zurück.

    :param xml_filepath: Pfad zur XML-Datei.
    :return: NetworkX-Graph mit erweiterten Attributen.
    """
    tree = ET.parse(xml_filepath)
    root = tree.getroot()
    namespace = {"ns": "http://sndlib.zib.de/network"}

    G = nx.Graph()

    # Knoten hinzufügen
    for node in root.findall(".//ns:node", namespace):
        node_id = node.get("id")
        x = float(node.find("ns:coordinates/ns:x", namespace).text)
        y = float(node.find("ns:coordinates/ns:y", namespace).text)
        G.add_node(node_id, pos=(x, y))

    # Kanten hinzufügen
    for link in root.findall(".//ns:link", namespace):
        source = link.find("ns:source", namespace).text
        target = link.find("ns:target", namespace).text

        # Zusätzliche Module und Kapazitätskosten analysieren
        modules = []
        for module in link.findall("ns:additionalModules/ns:addModule", namespace):
            capacity = float(module.find("ns:capacity", namespace).text)
            cost = float(module.find("ns:cost", namespace).text)
            modules.append({"capacity": capacity, "cost": cost})

        # Mindestkapazität und minimaler Kostenwert
        if modules:
            min_capacity = min(module["capacity"] for module in modules)
            min_cost = min(module["cost"] for module in modules)
        else:
            min_capacity = 0
            min_cost = 0

        G.add_edge(source, target, distance=min_cost, capacity=min_capacity, modules=modules)

    return G



