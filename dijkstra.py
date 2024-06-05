# 最短距離問題 (ダイクストラ法)
#
# [定式化]
#   s ∈ V       ... 始点
#   f(u, k)      ... k 回以内で移動する場合の始点から頂点 u までの距離の最小値
#   adjacent(u)  ... 頂点 u に隣接する頂点の集合
#   c(u, v)      ... 頂点 u から頂点 v への辺のコスト
#   漸化式:
#     f(u, k) = min[v ∈ adjacent(u)]{ f(v, k-1) + c(u, v) }  (if k > 0)
#     f(u, k) = ∞  (if k < 0)
#   初期条件:
#     f(s, 0) = 0
#     f(u, 0) = ∞  (u ≠ s)

#! 参考:
#!  アントルーティング: 蟻を用いた最短経路の探索方法 (蟻の行動はいずれ最短経路に収束する)


import osmnx as ox
import extract_driveway_csv as edc
import my_network as nt
import extract_driveway_osm as edo

def get_node_osmids(u: tuple) -> int:
    """ u の座標に最も近い Node の osmid を返す
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
    MakeNetwork = nt.MakeNetwork(Network, edc.FilePath.node, edc.FilePath.edge)
    MakeNetwork.add_node()
    MakeNetwork.add_edge()
    start_osmid = get_node_osmids(edo.Spot.kgu)
    goal_osmid = get_node_osmids(edo.Spot.uddhichuo) 
    min_costs = Network.dijkstra(start_osmid)
    print(f'{round(min_costs[goal_osmid], 3)} min')
    shortest_path = Network.get_shortest_path(start_osmid, goal_osmid)
    Network.draw(is_directed=True, path=shortest_path)

if __name__ == "__main__":
    main()
