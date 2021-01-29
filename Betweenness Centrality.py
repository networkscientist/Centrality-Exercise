# This script calculates the betweenness centrality for the road network in the canton Zurich between all the
# non-flooded edges and nodes
import geopandas as gpd
import networkx as nx

# General workspace settings
MY_WORKSPACE: str = "/home/sirian/Applications/Scripts/python/networkExercise/exercise"

# Input data: Take the shp files of the flooded and non-flooded edges & nodes.
NODES_FILE_TOTAL: str = MY_WORKSPACE + "/zh_nodes.shp"
EDGES_FILE_TOTAL: str = MY_WORKSPACE + "/zh_roads.shp"
NODES_FILE_FLOODED: str = MY_WORKSPACE + "/zh_nodes_flooded.shp"
EDGES_FILE_FLOODED: str = MY_WORKSPACE + "/zh_roads_flooded.shp"

# GeoDataFrame: Read the shp files into GeoDataFrames
nodes_gdf_total = gpd.read_file(NODES_FILE_TOTAL)
edges_gdf_total = gpd.read_file(EDGES_FILE_TOTAL)
nodes_gdf_flooded = gpd.read_file(NODES_FILE_FLOODED)
edges_gdf_flooded = gpd.read_file(EDGES_FILE_FLOODED)

# TextIO: Create nodes distances file for output data and open in write mode
node_betweenness_centrality_file = open(MY_WORKSPACE + "/betweenness_centrality.csv", "w")
node_betweenness_centrality_file.write("nodeid" + ";" + "betweenness_centrality" + "\n")

# List[Any]: Get all node & edges ids from the flooded situation
nodes_id_list_flooded = []
edges_id_list_flooded = []
for index, row in nodes_gdf_flooded.iterrows():
    nodes_id_list_flooded.append(row.nodeid)
for index, row in edges_gdf_flooded.iterrows():
    edges_id_list_flooded.append(row.ID_Road)

# Graph G: Create with Graph() function from the networkx~nx library
G = nx.Graph()
# loop through the road shapefile
counter_flooded: int = 0
counter_safe: int = 0
for index, row in edges_gdf_total.iterrows():
    # Check if the node is flooded
    # The if statement is TRUE, if the edge IS NOT flooded
    if (row.ID_Road not in edges_id_list_flooded) and (row.nodeid1 not in nodes_id_list_flooded) and (
            row.nodeid2 not in nodes_id_list_flooded):
        # print("Not flooded: " + str(row.ID_Road))
        # counter_safe += 1
        length: object = row.SHAPE_Leng
        # node_id_1: object = row.nodeid1
        # nodeid2: object = row.nodeid2

        # Get the starting node's coordinates and add it to the graph
        x_coord_1 = nodes_gdf_total[nodes_gdf_total["nodeid"] == row.nodeid1].x
        y_coord_1 = nodes_gdf_total[nodes_gdf_total["nodeid"] == row.nodeid1].y
        G.add_node(row.nodeid1, pos=(x_coord_1, y_coord_1))

        # Get the end node's coordinates and add it to the graph.
        x_coord_2 = nodes_gdf_total[nodes_gdf_total["nodeid"] == row.nodeid2].x
        y_coord_2 = nodes_gdf_total[nodes_gdf_total["nodeid"] == row.nodeid2].y
        G.add_node(row.nodeid2, pos=(x_coord_2, y_coord_2))

        # Get the edge's start/end nodes' ids and add it to the graph
        G.add_edge(row.nodeid1, row.nodeid2, weight=length)
        # print("Edge " + str(row.ID_Road) + " added!")
    # If the edge is flooded, do not input it into the graph
    # else:
    # print("Flooded: " + str(row.ID_Road))
    # counter_flooded += 1

# print("Safe edges: " + str(counter_safe))
# print("Flooded edges: " + str(counter_flooded))
print("network graph created ...")

# calculate betweenness centrality for all nodes and write it to the output file
# Betweenness centrality of a node v is the sum of the fraction of all-pairs shortest paths that pass through v.
# parameter k is the number of the sample to safe time, k=1000 --> ca. 1% of the total network is taken as a sample
# if k=None, the full network will be considered. This needs some hours of computation
betweenness_centrality: dict = nx.betweenness_centrality(G, k=1000, normalized=True, endpoints=True)
# betweennesscentrality=nx.betweenness_centrality(G, k=None, normalized=True, endpoints=True)
for n in betweenness_centrality:
    node_betweenness_centrality_file.write(str(n) + ";" + str(betweenness_centrality[n]) + "\n")
node_betweenness_centrality_file.close()
print("betweenness centrality for nodes in ZH traffic network computed and exported to file ...")
