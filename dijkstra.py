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
#! [参考]:
#!  アントルーティング(ACO): 蟻を用いた最短経路の探索方法 (蟻の行動はいずれ最短経路に収束する)
#!  ベルマンフォード法: 負のコストを持つ辺が存在する場合にも適用可能
#!  ワーシャルフロイド法: すべての頂点間の最短経路を求める

import osmnx as ox
import my_network as nt
import constant as c

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
    MakeNetwork = nt.MakeNetwork(Network, c.Path.node_csv, c.Path.edge_csv)
    MakeNetwork.add_node()
    MakeNetwork.add_edge()
    start_osmid = get_node_osmids(c.Spot.kgu)
    goal_osmid = get_node_osmids(c.Spot.uddhichuo) 
    min_costs = Network.dijkstra(start_osmid)
    print(f'({c.Transportation.car}) {c.Spot.kgu_name} -> {c.Spot.uddhichuo_name}: {round(min_costs[goal_osmid], 3)} min')
    shortest_path = Network.get_shortest_path(start_osmid, goal_osmid)
    Network.draw(is_directed=True, path=shortest_path)

if __name__ == "__main__":
    main()
    print(c.FontColor.YELLOW + 'Program ran successfully' + c.FontColor.END)
