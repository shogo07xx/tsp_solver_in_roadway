import osmnx as ox
import my_network as nt
import constant as c

def get_node_osmids(u: tuple) -> int:
    """ u の座標に最も近い Node の osmid を返す  \n
    Args:
        u (tuple): 頂点 u の経度と緯度を格納したタプル
    Returns:
        nearest_node (int): u に最も近い頂点の osmid を表す
    """
    G = ox.graph_from_point(u, dist=200, network_type='drive')
    nearest_node = ox.nearest_nodes(G, u[0], u[1])
    return nearest_node

def main():
    Network = nt.Dijkstra()
    MakeNetwork = nt.MakeNetwork(Network, c.Path.node_csv, c.Path.edge_csv)
    MakeNetwork.add_node()
    MakeNetwork.add_edge()
    start_osmid = get_node_osmids(c.Spot.kgu)
    goal_osmid = get_node_osmids(c.Spot.uddhichuo) 
    min_costs = Network.dijkstra(start_osmid)
    print(f'({c.Transportation.car}) {c.Spot.kgu_name} -> {c.Spot.uddhichuo_name}: {round(min_costs[goal_osmid], 3)} min')
    shortest_path = Network.get_shortest_path(start_osmid, goal_osmid)
    Network.draw(is_directed=True, path=shortest_path)

if __name__ == '__main__':
    main()
    print(c.FontColor.YELLOW + 'Program ran successfully' + c.FontColor.END)
