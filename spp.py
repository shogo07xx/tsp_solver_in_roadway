import heapq
from my_network import Network 
from typing import Dict

class Dijkstra(Network):
    """ 継承元が Network クラスである最短経路問題をダイクストラ法で解くクラス """
    def __init__(self, node_csv_file: str, edge_csv_file: str) -> None:
        """ ネットワーク及び最短経路を求めるために必要な変数を初期化 \n
        Args:
            node_csv_file (str): 頂点に関する情報を格納した csv ファイルの path
            edge_csv_file (str): 辺に関する情報を格納した csv ファイルの path
        Attributes:
            cost (Dict[int, Dict[int, float]]): 各頂点から各頂点までのコストを格納
                key (int): 始点の osmid
                value (dict): 始点からのコストを格納する辞書
                    key (int): 終点の osmid
                    value (float): 始点から終点までのコスト
            prev (Dict[int, Dict[int, int]]): 最短経路において、各頂点の直前の頂点を格納
                key (int): 始点の osmid
                value (dict): 最短経路の直前の頂点を格納する辞書
                    key (int): 終点の osmid
                    value (int): 最短経路において、終点の前の頂点の osmid
        """
        super().__init__(node_csv_file, edge_csv_file)
        self.cost: Dict[int, Dict[int, float]] = {}
        self.prev: Dict[int, Dict[int, float]] = {}

    def solve(self, start: int) -> list[float]:
        """ ダイクストラ法を用いて最短経路とその時のコストを求める \n
        Args:
            start (int): 最短経路問題における始点の osmid
        Return:
            cost (Dict[int, float]):
                key: 終点の osmid
                value: 始点から全ての頂点までの最短経路のコスト
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
        """ 最短経路を求める  \n
        Args:
            start (int): 最短経路問題における始点の osmid
            goal (int): 最短経路問題における終点の osmid
        Returns:
            path (list[int]): 要素は各頂点の osmid で、始点から終点までの最短経路を表すリストを返す
        """
        path = []
        u = goal
        while u != -1:
            path.append(u)
            u = self.prev[start][u]
        path.reverse()
        return path
