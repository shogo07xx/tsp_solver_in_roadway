from spp import Dijkstra

class TwoOpt(Dijkstra):
    """ 継承元が最短経路を解くクラスである巡回セールスマン問題を 2-opt 法で解くためのクラス """
    def __init__(self, V: list[int], node_csv_file: str, edge_csv_file: str) -> None:
        """ ネットワーク及び巡回セールス問題に必要な変数を初期化 \n
        Args:
            V (list[int]): 巡回路の頂点の osmid を格納したリスト
        Attributes:
            n (int): 頂点の数
            V (list[int]): 巡回路の頂点の osmid を格納したリスト
            dist_matrix (list[list[float]]): 頂点間の距離行列
            # sp_matrix (list[list[list[int]]]): 頂点間の最短経路リストを要素とする行列
        """
        super().__init__(node_csv_file, edge_csv_file)
        self.n: int = len(V)
        self.V: list[int] = V
        self.dist_matrix: list[list[float]] = [[0] * self.n for _ in range(self.n)]
        # self.sp_matrix: list[list[list[int]]] = [[[]] * self.n for _ in range(self.n)]
        self._distance_matrix()
    def _distance_matrix(self) -> None:
        """ 都市間の距離行列を計算する関数 """
        for v in self.V:
            min_cost = self.solve_spp(v)
            for u in self.V:
                self.dist_matrix[self.V.index(v)][self.V.index(u)] = min_cost[u]
                # self.sp_matrix[self.V.index(v)][self.V.index(u)] = self.get_shortest_path(v, u)

    def two_opt_swap(self, tour: list[int], i: int, j: int) -> list[int]:
        """ 2-OPT のエッジ交換操作を行う関数 \n
        Args:
            tour (list[int]): 交換前の巡回路 (ハミルトン閉路)
            i (int): 交換するエッジのインデックス
            j (int): 交換するエッジのインデックス
        Returns:
            new_tour (list[int]): 交換後の巡回路
        """
        new_tour = tour[:i] + tour[i:j+1][::-1] + tour[j+1:]
        return new_tour
    
    def calc_cost(self, tour: list[int]) -> float:
        """ 巡回路の総コストを計算 \n
        Args:
            tour (list[int]): 巡回路 (ハミルトン閉路)
        Returns:
            cost (float): 巡回路の総コスト
        """
        cost = 0
        for i in range(len(tour) - 1):
            cost += self.dist_matrix[tour[i]][tour[i+1]]
        cost += self.dist_matrix[tour[-1]][tour[0]]  # 戻るコスト
        return cost

    def solve(self, initial_tour: list[int]) -> list[int]:
        """ 最適な巡回路を決定 \n
        Args:
            initial_tour (list[int]): 初期巡回路
        Returns:
            best_tour (list[int]): 最適な巡回路
        """
        best_tour = initial_tour
        best_cost = self.calc_cost(best_tour)
        improved = True
        
        while improved:
            improved = False
            for i in range(1, self.n - 1):
                for j in range(i + 1, self.n):
                    new_tour = self.two_opt_swap(best_tour, i, j)
                    new_cost = self.calc_cost(new_tour)
                    if new_cost < best_cost:
                        best_tour = new_tour
                        best_cost = new_cost
                        improved = True
                        break  # 改善が見つかったので外ループへ
                if improved:
                    break  # 改善が見つかったので外ループへ
        return best_tour