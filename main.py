import igraph as ig
from igraph import summary, Graph


def get_length_and_material_info(graph_data: Graph, from_point, to_point):
    vertex_a_index, vertex_c_index = graph_data.vs.find(id=from_point).index, graph_data.vs.find(id=to_point).index
    shortest_path_indices = \
        graph_data.get_shortest_paths(v=vertex_a_index, to=vertex_c_index, weights="length", mode="OUT",
                                      output="vpath")[0]
    total_length = 0
    for i in range(0, len(shortest_path_indices) - 1):
        edge_index = graph_data.get_eid(shortest_path_indices[i], shortest_path_indices[i + 1])
        total_length += graph_data.es[edge_index]["length"]
    return total_length


rate_cards = {
    "Rate Card A": {"Cabinet": 1000,
                    "Trench/m (verge)": 50,
                    "Trench/m (road)": 100,
                    "Chamber": 200,
                    "Pot": 100},
    "Rate Card B": {"Cabinet": 1200,
                    "Trench/m (verge)": 40,
                    "Trench/m (road)": 80,
                    "Chamber": 200,
                    "Pot": lambda trench_length: 20 * trench_length}}


def get_rate_cards_price_info(graph_data: Graph):
    price_data = dict()
    for vertex_object in graph_data.vs:
        vertex_type = vertex_object['type']

        for rate_card_title, rate_card_data in rate_cards.items():
            if callable(rate_card_data[vertex_type]):
                trench_length = get_length_and_material_info(graph_data, graph_data.vs.find(type='Cabinet')['id'],
                                                             vertex_object['id'])
                amount_to_add = rate_card_data[vertex_type](trench_length)
            else:
                amount_to_add = rate_card_data[vertex_type]
            price_data[rate_card_title] = price_data.get(rate_card_title, 0) + amount_to_add

    for wire_connection in graph_data.es:
        for rate_card_title, rate_card_data in rate_cards.items():
            rate_card_price_key = f"Trench/m ({wire_connection['material']})"
            amount_to_add = rate_card_data[rate_card_price_key] * wire_connection['length']
            price_data[rate_card_title] = price_data.get(rate_card_title, 0) + amount_to_add

    return price_data


graph_file: Graph = ig.Graph.Read_GraphML(
    '/home/oleksandr/PycharmProjects/gigaclear_laying_cost_calculation/task_files/problem.graphml')

print(get_rate_cards_price_info(graph_file))
