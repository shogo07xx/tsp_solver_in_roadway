import heapq
from typing import Dict
from my_network import Network 

class Dijkstra(Network):
    def __init__(self) -> None:
        """ ダイクストラ法を実行するためのコンストラクタ """
        super().__init__()
        self.cost = {}
        self.prev = {}

    def dijkstra(self, start: int) -> list[float]:
        """ ダイクストラ法を用いて最短経路とその時のコストを求める \n
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
        """ 最短経路を求める  \n
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
