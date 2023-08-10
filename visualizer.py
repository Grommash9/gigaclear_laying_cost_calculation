from igraph import Graph
import igraph.drawing as igdraw
import sys

if __name__ == '__main__':
    try:
        file_path = sys.argv[1]
    except IndexError:
        print('Please specify file to with you want to process. Example: python main.py ./task_files/problem.graphml')
        sys.exit(-1)

    if not file_path.endswith('.graphml'):
        raise ValueError('Please use graphml file!')

    graph_data = Graph.Read_GraphML(file_path)

    visual_style = {}
    visual_style["layout"] = graph_data.layout("kk")
    visual_style["vertex_size"] = 30
    visual_style["vertex_color"] = "lightblue"
    visual_style["vertex_label"] = graph_data.vs["id"]
    visual_style["edge_color"] = "gray"
    visual_style["edge_width"] = 2

    old_file_name = file_path.split("/")[-1].split('.')[0]
    igdraw.plot(graph_data, **visual_style).save(f'{old_file_name}_visual.png')
