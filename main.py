import igraph as ig
from igraph import Graph
import sys


def get_length_and_material_info(graph_data: Graph, from_point, to_point):
    path_indices = graph_data.get_shortest_paths(
        v=from_point, to=to_point, weights="length", mode="OUT", output="vpath")[0]
    if len(path_indices) == 0:
        raise ValueError(f"Item with index {to_point} seems to have no connection to {from_point} please double check your graphml file")
    return sum([graph_data.es[graph_data.get_eid(path_indices[i], path_indices[i + 1])]["length"]
                for i in range(0, len(path_indices) - 1)])


def calculate_vertex_price(graph_data: Graph, rate_card_data, vertex_object):
    vertex_type = vertex_object['type']
    if callable(rate_card_data[vertex_type]):
        trench_length = get_length_and_material_info(
            graph_data, graph_data.vs.find(type='Cabinet').index, vertex_object.index)
        return rate_card_data[vertex_type](trench_length)
    else:
        return rate_card_data[vertex_type]


def calculate_wire_price(rate_card_data, wire_connection):
    rate_card_price_key = f"Trench/m ({wire_connection['material']})"
    return rate_card_data[rate_card_price_key] * wire_connection['length']


def count_graph_realisation_price(graph_data: Graph):
    prices = dict()
    for vertex_object in graph_data.vs:
        for title, price_data in rate_cards.items():
            prices[title] = prices.get(title, 0) + calculate_vertex_price(graph_data, price_data, vertex_object)
    for wire_connection in graph_data.es:
        for title, price_data in rate_cards.items():
            prices[title] = prices.get(title, 0) + calculate_wire_price(price_data, wire_connection)
    return prices


rate_cards = {"Rate Card A": {"Cabinet": 1000, "Trench/m (verge)": 50,
                              "Trench/m (road)": 100, "Chamber": 200, "Pot": 100},
              "Rate Card B": {"Cabinet": 1200, "Trench/m (verge)": 40, "Trench/m (road)": 80,
                              "Chamber": 200, "Pot": lambda trench_length: 20 * trench_length}}


try:
    file_path = sys.argv[1]
except IndexError:
    print('Please specify file to with you want to process. Example: python main.py ./task_files/problem.graphml')
    sys.exit(-1)

if not file_path.endswith('.graphml'):
    raise ValueError('Please use graphml file!')

graph_file: Graph = ig.Graph.Read_GraphML(file_path)

print(count_graph_realisation_price(graph_file))
