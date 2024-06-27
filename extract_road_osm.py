import osmnx as ox
import pandas as pd
from geopy.distance import geodesic
import constant as c

def extract_nodes_edges():
    """ osm から 2 つの地点 u, v の中心点を中心とする半径を持つ円内の道路ネットワークを取得し csv 形式で出力  \n
    Attributes:
        u (tuple): ある地点の緯度経度
        v (tuple): ある地点の緯度経度
        edges (pd.DataFrame): 
            u:            エッジの始点となる Node ID  #! 使用する
            v:            エッジの終点となる Node ID  #! 使用する
            key:          複数のエッジが同じノードペアを結ぶ場合に、それらを区別するためのキー
            osmid:        OpenStreetMap の Edge ID  #! 使用する
            highway:      道路タイプ
            oneway:       一方通行かどうかを示す真偽値  #! 使用する
            reversed:     終点から始点への一方通行の場合、真をとる。  #! 使用する
            length:       エッジの長さ (メートル単位)  #! 使用する
            geometry:     エッジの接続形状を示すオブジェクト
            ref:          公式に設定されている道路の参照番号
            name:         道路の名前
            maxspeed:     最高速度  #! 使用する
            bridge:       エッジが橋であるかどうかを示すブール値
            lanes:        車線の数
        nodes (pd.DataFrame): 
            osmid:        OpenStreetMap の Node ID  #! 使用する
            y:            Node の緯度  #! 使用する
            x:            Node の経度  #! 使用する
            street_count: Node に接続されている道路の数
            highway:      Node に接続されている道路のタイプ  #! 使用する
            geometry:     Node の位置を示すオブジェクト 
    """

    # (u, v) を指定
    u = c.Spot.Coordinate.kgu
    v = c.Spot.Coordinate.uddhichuo

    # 始点や終点の座標に最も近い頂点を取得した道路ネットワークに含まれるようにするための余分な距離
    margin_dist = c.MarginDist.get_road_network_radius

    # 道路ネットワークデータを取得
    center_point = ((u[0] + v[0]) / 2, (u[1] + v[1]) / 2)
    radius = (geodesic(u, v).meters + margin_dist) / 2
    G = ox.graph_from_point(center_point, dist=radius, network_type='drive')

    # グラフデータから DataFrame 形式に変更
    nodes, edges = ox.graph_to_gdfs(G, nodes=True, edges=True)
    nodes = pd.DataFrame(nodes)
    edges = pd.DataFrame(edges)

    # csv形式で出力
    nodes.to_csv(f'{c.Path.node_csv}')
    edges.to_csv(f'{c.Path.edge_csv}')

    # 道路ネットワークを可視化
    ox.plot_graph(G)

if __name__ == "__main__":
    extract_nodes_edges()
    print(c.FontColor.YELLOW + 'Program ran successfully' + c.FontColor.END)
