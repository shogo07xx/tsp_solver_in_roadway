import osmnx as ox
import constant as c
from spp import Dijkstra

def get_node_osmid(u: tuple) -> int:
    """ 座標 u = (x, y) に最も近い Node の osmid を返す  \n
    Args:
        u (tuple): 座標 u の経度と緯度を格納したタプル
    Returns:
        nearest_node (int): 座標 u に最も近い頂点の osmid を返す
    """
    G = ox.graph_from_point(u, dist=200, network_type='drive')
    nearest_node = ox.nearest_nodes(G, u[0], u[1])
    return nearest_node

def main_spp():
    solve_for_network = Dijkstra(c.Path.node_csv, c.Path.edge_csv)
    start_osmid = get_node_osmid(c.Spot.kgu)
    goal_osmid = get_node_osmid(c.Spot.uddhichuo) 
    min_costs = solve_for_network.solve_spp(start_osmid)
    print(f'({c.Transportation.car}) {c.Spot.kgu_name} -> {c.Spot.uddhichuo_name}: {round(min_costs[goal_osmid], 3)} min')
    shortest_path = solve_for_network.get_shortest_path(start_osmid, goal_osmid)
    solve_for_network.draw(is_directed=True, path=shortest_path)

if __name__ == '__main__':
    main_spp()
    print(c.FontColor.YELLOW + 'Program ran successfully' + c.FontColor.END)
