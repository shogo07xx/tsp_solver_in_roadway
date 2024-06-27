from spp import Dijkstra

class CHI:
    def __init__(self, dist_matrix):
        self.n: int = len(dist_matrix)
        self.dist_matrix: list[list[float]] = dist_matrix
        self.tour: list[int] = self.__find_initial_tour()

    # 初期の巡回路を最も遠い都市ペアを用いて選択
    def __find_initial_tour(self) -> list[int]:
        max_dist = -1
        initial_pair = (0, 0)
        for i in range(self.n):
            for j in range(i+1, self.n):
                tour_cost = self.dist_matrix[i][j] + self.dist_matrix[j][i]
                if tour_cost > max_dist:
                    max_dist = tour_cost
                    initial_pair = (i, j)
        # 初期巡回路に最も遠い都市ペアを追加
        initial_tour = [initial_pair[0], initial_pair[1], initial_pair[0]]
        return initial_tour

    def calc_cost(self) -> float:
        cost = 0
        for i in range(len(self.tour) - 1):
            cost += self.dist_matrix[self.tour[i]][self.tour[i + 1]]
        return cost

    def __find_best_insertion(self) -> tuple[int, int]:
        best_ratio = float('inf')
        best_city = None
        best_i = None

        for k in range(self.n):
            if k in self.tour:
                continue
            for i in range(len(self.tour) - 1):
                j = i + 1
                cik = self.dist_matrix[self.tour[i]][k]
                ckj = self.dist_matrix[k][self.tour[j]]
                cij = self.dist_matrix[self.tour[i]][self.tour[j]]
                if cij == 0:
                    ratio = float('inf')
                else:
                    ratio = (cik + ckj) / cij
                if ratio < best_ratio:
                    best_ratio = ratio
                    best_city = k
                    best_i = i
        return best_city, best_i

    def solve(self):
        while len(self.tour) < self.n + 1:
            best_city, best_i = self.__find_best_insertion()
            self.tour.insert(best_i + 1, best_city)
        return self.tour
    

class TwoOpt(Dijkstra):
    """ 継承元が最短経路を解くクラスである TSP を 2-opt 法で解くためのクラス """
    def __init__(self, node_csv_file: str, edge_csv_file: str, V: list[int]) -> None:
        """ ネットワーク及び TSP を解くのに必要な変数を初期化 \n
        Args:
            V (list[int]): 巡回路に含む頂点の osmid を格納したリスト
        Attributes:
            n (int): 頂点の数
            V (list[int]): 巡回路の頂点の osmid を格納したリスト
            dist_matrix (list[list[float]]): 頂点間の距離行列
            min_cost (float): 巡回路の最小コスト
            tour (list[int]): 要素が頂点の index である最適な巡回路
            tour_osmid (list[int]): 要素が頂点の osmid である最適な巡回路
            sp_matrix (list[list[list[int]]]): 頂点間の最短経路リストを要素とする行列
            tour_multi_paths (list[list[int]]): 巡回路の各エッジにおける最短経路リスト
        """
        super().__init__(node_csv_file, edge_csv_file)
        self.n: int = len(V)
        self.V: list[int] = V
        self.dist_matrix: list[list[float]] = [[0] * self.n for _ in range(self.n)]
        self.min_cost: float = float('inf')
        self.sp_matrix: list[list[list[int]]] = [[[]] * self.n for _ in range(self.n)]
        self._make_dist_matrix()
        self.tour = (_ := CHI(self.dist_matrix)).solve()
        self.tour_osmid: list[int] = [self.V[i] for i in self.tour]
        self.tour_multi_paths = [self.sp_matrix[self.tour[i]][self.tour[i+1]] for i in range(self.n - 1)]

    def _make_dist_matrix(self) -> None:
        """ 頂点間の距離行列を計算する関数 """
        for v in self.V:
            min_cost = super().solve(v)
            for u in self.V:
                self.dist_matrix[self.V.index(v)][self.V.index(u)] = min_cost[u]
                self.sp_matrix[self.V.index(v)][self.V.index(u)] = self.get_shortest_path(v, u)

    def _two_opt_swap(self, tour: list[int], i: int, j: int) -> list[int]:
        """ 2-OPT のエッジ交換操作を行う関数 \n
        Args:
            tour (list[int]): 交換前の巡回路 (ハミルトン閉路)
            i (int): 交換するエッジのインデックス
            j (int): 交換するエッジのインデックス
        Returns:
            new_tour (list[int]): 交換後の巡回路
        """
        new_tour = tour[:i] + tour[i:j][::-1] + tour[j:]
        return new_tour
    
    def _calc_cost(self, tour) -> float:
        """ 巡回路の総コストを計算 \n
        Args:
            tour (list[int]): 巡回路（要素は頂点の添字）
        Returns:
            cost (float): 巡回路の総コスト
        """
        cost = 0
        for i in range(len(tour) - 1):
            cost += self.dist_matrix[tour[i]][tour[i+1]]
        return cost

    def solve(self) -> float:
        """ 2-opt 法を用いて最適な巡回路とその時のコストを求める \n
        Return:
            dict:
                key (str): 'tour_osmid'
                value (list[int], float, list[list[int]]): 巡回路の各頂点の osmid のリスト
                key (str): 'cost'
                value (float): 巡回路のコスト
                key (str): 'multi_paths'
                value (list[list[int]]): 巡回路の各エッジにおける最短経路リスト
        """
        best_tour = self.tour
        best_cost = self._calc_cost(best_tour)
        improved = True
        while improved:
            improved = False
            for i in range(1, self.n - 1):
                for j in range(i + 1, self.n):
                    new_tour = self._two_opt_swap(best_tour, i, j)
                    new_cost = self._calc_cost(new_tour)
                    if new_cost < best_cost:
                        best_tour = new_tour
                        best_cost = new_cost
                        improved = True
                        break  # 改善が見つかったので外ループへ
                if improved:
                    break  # 改善が見つかったので外ループへ
        self.min_cost = best_cost
        self.tour = best_tour
        self.tour_osmid = [self.V[i] for i in self.tour]
        self.tour_multi_paths = [self.sp_matrix[self.tour[i]][self.tour[i+1]] for i in range(self.n - 1)]
        return {'tour_osmid': self.tour_osmid, 'cost': self.min_cost, 'multi_paths': self.tour_multi_paths}
    