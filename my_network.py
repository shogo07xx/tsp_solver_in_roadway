import networkx as nx
import matplotlib.pyplot as plt
import extract_road_csv as edc
from typing import Dict
import itertools

class Network:
    """ ネットワークに頂点や辺を追加する機能や自身を描画する機能を持つクラス """
    def __init__(self, node_csv_file: str, edge_csv_file: str) -> None:
        """ ネットワークを初期化 \n
        Args:
            node_csv_file (str): 頂点に関する情報を格納した csv ファイルの path
            edge_csv_file (str): 辺に関する情報を格納した csv ファイルの path
        Attributes:
            nodes (Dict[int, Dict[str, int]]): 各頂点の情報を格納
                osmid (dict): 頂点の osmid 値に基づく情報を格納
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
        self._add_nodes(node_csv_file)
        self._add_edges(edge_csv_file)

    def __add_node(self, osmid: int, x: float, y: float, highway: str = None) -> None:
        """ 頂点を追加  \n
        Args:
            osmid (int): 頂点の osmid
            x (float): 頂点の x 座標
            y (float): 頂点の y 座標
            highway (str, optional): 頂点の種類
        """
        self.nodes[osmid] = {'x': x, 'y': y, 'highway': highway}
    
    def _add_nodes(self, node_csv_file: str) -> None:
        """ csv ファイルの情報に基づいて頂点を追加 \n
        Args:
            node_csv_file (str): 頂点に関する情報を格納した csv ファイルの path
        """
        nodes: list[dict] = edc.extract_node_datas(node_csv_file)
        for node in nodes:
            self.__add_node(node['osmid'], node['x'], node['y'], node['highway'])
        
    def __add_edge(self, u_osmid: int, v_osmid: int, e_osmid: int, cost: float, oneway=False, reverse=False) -> None:
        """ 辺を追加  \n
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

    def _add_edges(self, edge_csv_file: str) -> None:
        """ csv ファイルの情報に基づいて辺を追加 \n
            edge_csv_file (str): 辺に関する情報を格納した csv ファイルの path
        """
        edges: list[dict] = edc.extract_edge_datas(edge_csv_file)
        for edge in edges:
            cost = (edge['length']/1000)/(edge['maxspeed']/60)  # 辺 (u, v) を移動するためにかかる時間 [min]
            self.__add_edge(edge['u'], edge['v'], edge['osmid'], cost, edge['oneway'], edge['reversed'])
        
    def ct_traffic_signals(self, nodes: list[int] | list[list[int]]) -> int:
        """ 交通信号機の数をカウント \n
        Args:
            nodes (list[int] | list[list[int]]): 頂点の osmid のリストもしくはそれを格納したリスト
        Returns:
            count (int): 交差点が交通信号機であるような頂点の個数
        """
        count = 0
        if isinstance(nodes[0], list):
            nodes = list(itertools.chain(*nodes))
        for node in nodes:
            if self.nodes[node]['highway'] == 'traffic_signals':
                count += 1
        return count
        
    def draw(self, is_directed = False, paths: list[int] | list[list[int]] = None) -> None:
        """ ネットワークを描画  \n
        Args:
            is_directed (bool, optional): 有向グラフならば真
            paths (list[int] | list[list[int]], optional): 頂点の osmid を要素としそれらを繋いだ強調したい経路もしくはそれを格納したリスト
        """
        normal_node_size = 10
        normal_node_color = 'skyblue'
        emphasize_node_size = 8 * normal_node_size
        emphasize_node_color = '#ff7100'
        emphasize_edge_color = 'red'
        if is_directed:
            G = nx.DiGraph()
        else:
            G = nx.Graph()
        # edge_labels = {}
        for u_osmid, edges in self.edges.items():
            for v_osmid, edge in edges.items():
                if edge['cost'] == float('inf'):
                    continue
                G.add_edge(u_osmid, v_osmid, weight=edge['cost'])
                # edge_labels[(u_osmid, v_osmid)] = round(edge_info['cost'],1)
        pos = {osmid: (node['x'], node['y']) for osmid, node in self.nodes.items()} 
        nx.draw(G, pos, with_labels=False, node_size=normal_node_size, node_color=normal_node_color)
        # nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        def _draw_path(_G, _pos, _path, _emphasize_node_size, _emphasize_node_color, _emphasize_edge_color):
            start_node = _path[0]
            end_node = _path[-1]
            nx.draw_networkx_nodes(_G, _pos, nodelist=[start_node, end_node], node_size=_emphasize_node_size, node_color=_emphasize_node_color)
            edges_in_path = [(_path[i], _path[i+1]) for i in range(len(_path)-1)]
            nx.draw_networkx_edges(_G, _pos, edgelist=edges_in_path, edge_color=_emphasize_edge_color, width=2)
        if paths is not None and isinstance(paths[0], int):
            _draw_path(G, pos, paths, emphasize_node_size, emphasize_node_color, emphasize_edge_color)
        if paths is not None and isinstance(paths[0], list):
            for p in paths:
                _draw_path(G, pos, p, emphasize_node_size, emphasize_node_color, emphasize_edge_color)
        plt.show()
