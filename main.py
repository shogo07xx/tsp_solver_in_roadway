import osmnx as ox
import constant as c
from spp import Dijkstra
from tsp import TwoOpt
from my_network import Network

def get_node_osmid(u: tuple) -> int:
    """ 座標 u = (x, y) に最も近い Node の osmid を返す  \n
    Args:
        u (list[tuple] | tuple): 座標 u の経度と緯度を格納したタプル
    Returns:
        nearest_node (int): 座標 u に最も近い頂点の osmid の値
    """
    G = ox.graph_from_point(u, dist=200, network_type='drive')
    nearest_node = ox.nearest_nodes(G, u[0], u[1])
    return nearest_node

def main_get_node_osmid():
    print(get_node_osmid(c.Spot.Coordinate.kgu))
    print(get_node_osmid(c.Spot.Coordinate.uddhichuo))

def main_draw_network():
    N = Network(c.Path.node_csv, c.Path.edge_csv)
    N.draw(is_directed=True)

def main_spp():
    spp = Dijkstra(c.Path.node_csv, c.Path.edge_csv)
    start_osmid = get_node_osmid(c.Spot.Coordinate.kgu)
    goal_osmid = get_node_osmid(c.Spot.Coordinate.uddhichuo) 
    min_costs = spp.solve(start_osmid)
    print(f'({c.Transportation.car}) {c.Spot.Name.kgu} -> {c.Spot.Name.uddhichuo}: {round(min_costs[goal_osmid], 3)} min')
    shortest_path = spp.get_shortest_path(start_osmid, goal_osmid)
    spp.draw(is_directed=True, path=shortest_path)

def main_tsp():
    V = [
        2028119845,
        2699081269,
        3804698739,
        675652775,
        6065363505,
        5584275744,
        5472922597,
        1483026505,
        1483561439,
        4858788235
    ]
    tsp = TwoOpt(c.Path.node_csv, c.Path.edge_csv, V)
    for l in tsp.tour_osmid:
        print(l)
        tsp.draw(is_directed=True, multiple_path=tsp.tour_osmid)
    tsp.solve()
    for l in tsp.tour_osmid:
        print(l)


if __name__ == '__main__':
    # main_get_node_osmid()
    # main_draw_network()
    # main_spp()
    main_tsp()
    print(c.FontColor.YELLOW + 'Program ran successfully' + c.FontColor.END)
