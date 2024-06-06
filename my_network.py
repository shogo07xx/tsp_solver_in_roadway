import networkx as nx
import matplotlib.pyplot as plt
import heapq
import extract_road_csv as edc
from typing import Dict

class Network:
    def __init__(self) -> None:
        """ ネットワークの初期化を行うコンストラクタ
        Args:
            # n (int): 頂点数
            nodes (Dict[int, Dict[str, int]]): 各頂点の情報を格納
                osmid (dict): 頂点の osmid の値に基づく情報を格納
                    'x': 頂点の x 座標
                    'y': 頂点の y 座標
            edges (Dict[int, Dict[int, Dict[str, float]]]): edges[u][v] には、辺 (u, v) の情報を格納 
                osmid (dict): 頂点 u の隣接ノードを格納
                  osmid (dict): 辺 (u, v) の情報を格納
                    'osmid': 辺の OSMID
                    'cost': 辺のコスト
        """
        self.nodes: Dict[int, Dict[str, int]] = {}   
        self.edges: Dict[int, Dict[int, Dict[str, float]]] = {}

    def add_node(self, osmid: int, x: float, y: float):
        """ 頂点を追加
        Args:
            osmid (int): 頂点の osmid
            x (float): 頂点の x 座標
            y (float): 頂点の y 座標
        """
        self.nodes[osmid] = {'x': x, 'y': y}

    def add_edge(self, u_osmid: int, v_osmid: int, e_osmid: int, cost: float, oneway=False, reverse=False) -> None:
        """ 辺を追加
        Args:
            u_osmid (int): 頂点 u の osmid
            v_osmid (int): 頂点 v の osmid
            e_osmid (int): 辺 (u, v) の osmid
            cost (float): 辺 (u, v) のコスト
            oneway (bool, optional): 一方通行ならば真
            reverse (bool, optional): 逆方向に一方通行ならば真
        """
        self.edges.setdefault(u_osmid, {}).setdefault(v_osmid, {})['osmid'] = e_osmid
        self.edges.setdefault(v_osmid, {}).setdefault(u_osmid, {})['osmid'] = e_osmid
        if(oneway and not reverse):
            self.edges[u_osmid][v_osmid]['cost'] = cost
            self.edges[v_osmid][u_osmid]['cost'] = float("inf")
        elif(oneway and reverse):
            self.edges[u_osmid][v_osmid]['cost'] = float("inf")
            self.edges[v_osmid][u_osmid]['cost'] = cost
        else:
            self.edges[u_osmid][v_osmid]['cost'] = cost
            self.edges[v_osmid][u_osmid]['cost'] = cost
        
    def draw(self, is_directed = False, path = None) -> None:
        """ ネットワークを描画
        Args:
            is_directed (bool, optional): 有向グラフならば真
            path (_type_, optional): 頂点番号のリストで表現した強調したい経路
        """
        node_size = 10
        if is_directed:
            G = nx.DiGraph()
        else:
            G = nx.Graph()
        # edge_labels = {}
        for u_osmid, edge in self.edges.items():
            for v_osmid, edge_info in edge.items():
                if edge_info['cost'] == float("inf"):
                    continue
                G.add_edge(u_osmid, v_osmid, weight=edge_info['cost'])
                # edge_labels[(u_osmid, v_osmid)] = round(edge_info['cost'],1)
        pos = {node: (data['x'], data['y']) for node, data in self.nodes.items()}  # 座標の辞書を作成
        nx.draw(G, pos, with_labels=False, node_size=node_size, node_color='skyblue', font_size=10, font_color='black')
        # nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        if path is not None:
            start_node = path[0]
            end_node = path[-1]
            nx.draw_networkx_nodes(G, pos, nodelist=[start_node, end_node], node_size=8*node_size, node_color='#ff7100')
            edges_in_path = [(path[i], path[i+1]) for i in range(len(path)-1)]
            nx.draw_networkx_edges(G, pos, edgelist=edges_in_path, edge_color='red', width=2)
        plt.show()

class MakeNetwork:
    def __init__(self, network: Network, node_csv_file: str, edge_csv_file: str) -> None:
        """ ネットワークを作成するためのコンストラクタ
        Args:
            edge_csv_file (str): 辺に関する情報を持つ csv ファイルの path
            node_csv_file (str): 頂点に関する情報を持つ csv ファイルの path
        """
        self.network: Network = network
        self.nodes: list[dict] = edc.extract_node_datas(node_csv_file)
        self.edges: list[dict] = edc.extract_edge_datas(edge_csv_file)
    def add_node(self):
        """ csv ファイルの情報に基づいて頂点を追加 """
        for node in self.nodes:
            self.network.add_node(node['osmid'], node['x'], node['y'])
    def add_edge(self):
        """ csv ファイルの情報に基づいて辺を追加 """
        for edge in self.edges:
            cost = (edge['length']/1000)/(edge['maxspeed']/60)  # 辺 (u, v) を移動するためにかかる時間 [min]
            self.network.add_edge(edge['u'], edge['v'], edge['osmid'], cost, edge['oneway'], edge['reversed'])

class Dijkstra(Network):
    def __init__(self) -> None:
        """ ダイクストラ法を実行するためのコンストラクタ """
        super().__init__()
        self.cost = {}
        self.prev = {}

    def dijkstra(self, start: int) -> list[float]:
        """ ダイクストラ法を用いて最短経路とその時のコストを求める
        Args:
            start (int): 最短経路の開始点の頂点番号
        Return:
            cost (list[float]): 開始点から各頂点までの最短経路のコストを格納したリスト
        """
        self.cost[start] = {start: 0}
        self.prev[start] = {start: -1}
        q = []
        heapq.heappush(q, (0, start))
        while q != []:
            d, u = heapq.heappop(q)
            if(self.cost[start][u] < d):
                continue
            for v in self.edges[u]:
                if (v not in self.cost[start]) or (self.cost[start][v] > self.cost[start][u] + self.edges[u][v]['cost']):
                    self.cost[start][v] = self.cost[start][u] + self.edges[u][v]['cost']
                    self.prev[start][v] = u
                    heapq.heappush(q, (self.cost[start][v], v))
        return self.cost[start]

    def get_shortest_path(self, start: int, goal: int) -> list[int]:
        """ 最短経路を求める
        Args:
            start (int): 最短経路の開始点の頂点番号
            goal (int): 最短経路の終点の頂点番号
        Returns:
            list (int): 開始点から終点までの最短経路を頂点番号のリストとして返す
        """
        path = []
        u = goal
        while u != -1:
            path.append(u)
            u = self.prev[start][u]
        path.reverse()
        return path
