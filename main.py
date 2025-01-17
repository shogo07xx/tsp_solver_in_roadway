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
    """ 複数の座標に対して osmid を取得するメイン関数 """
    print(get_node_osmid(c.Spot.Coordinate.kgu))
    print(get_node_osmid(c.Spot.Coordinate.uddhichuo))

def main_draw_network():
    """ 道路ネットワークを描画するメイン関数 """
    N = Network(c.Path.node_csv, c.Path.edge_csv)
    N.draw(is_directed=True)

def main_spp():
    """ 最短経路問題を解くメイン関数 """
    spp_solver = Dijkstra(c.Path.node_csv, c.Path.edge_csv)
    start_osmid = get_node_osmid(c.Spot.Coordinate.kgu)
    goal_osmid = get_node_osmid(c.Spot.Coordinate.uddhichuo) 
    min_costs = spp_solver.solve(start_osmid)
    shortest_path = spp_solver.get_shortest_path(start_osmid, goal_osmid)
    delay_time = len(shortest_path) * c.DelayCoefficient.node + spp_solver.ct_traffic_signals(shortest_path) * c.DelayCoefficient.traffic_light + 2 * c.DelayCoefficient.departure_and_stop
    print(f'({c.Transportation.car}) {c.Spot.Name.kgu} -> {c.Spot.Name.uddhichuo}: {round(min_costs[goal_osmid] + delay_time, 2)} min')
    spp_solver.draw(is_directed=True, paths=shortest_path)

def main_tsp():
    """ 巡回セールスマン問題を解くメイン関数 """
    V = [
        1483026599,
        1483026595,
        1483026576,
        1483026548,
        1483026532,
        1483026505,
        1483026484
    ]
    tsp_solver = TwoOpt(c.Path.node_csv, c.Path.edge_csv, V)
    print(f'({c.Transportation.car}) 最近挿入法による推定巡回路移動時間: {round(tsp_solver.min_cost, 2)} min')
    tsp_solver.draw(is_directed=True, paths=tsp_solver.tour_paths)
    tsp_solver.solve()
    print(f'({c.Transportation.car}) 2-opt 法による推定巡回路移動時間: {round(tsp_solver.min_cost, 2)} min')  
    tsp_solver.draw(is_directed=True, paths=tsp_solver.tour_paths)

if __name__ == '__main__':
    # main_get_node_osmid()
    # main_draw_network()
    # main_spp()
    main_tsp()
    print(c.FontColor.YELLOW + 'Program ran successfully' + c.FontColor.END)
