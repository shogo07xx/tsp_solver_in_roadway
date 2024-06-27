from spp import Dijkstra

class CHI:
    """ 最近挿入法で距離行列から最適な巡回路を求めるクラス """
    def __init__(self, dist_matrix):
        """ 最近挿入法を用いるために必要な変数の初期化 \n
        Args:
            dist_matrix (_type_): 頂点間の距離行列
        Attributes:
            n (int): 頂点数
            dist_matrix (list[list[float]]): 頂点間の距離行列
            tour (list[int]): 最適な巡回路を表すリスト
        """
        self.n: int = len(dist_matrix)
        self.dist_matrix: list[list[float]] = dist_matrix
        self.tour: list[int] = self.__find_initial_tour()

    def __find_initial_tour(self) -> list[int]:
        """ 最も遠い二点からなる部分巡回路を凸包と仮定して初期部分巡回路を求める \n
        Returns:
            initial_tour (list[int]): 初期部分巡回路
        """
        max_dist = -1
        initial_pair = (0, 0)
        for i in range(self.n):
            for j in range(i+1, self.n):
                tour_cost = self.dist_matrix[i][j] + self.dist_matrix[j][i]
                if tour_cost > max_dist:
                    max_dist = tour_cost
                    initial_pair = (i, j)
        initial_tour = [initial_pair[0], initial_pair[1], initial_pair[0]]
        return initial_tour

    def calc_cost(self) -> float:
        """ 巡回路の総コストを計算 """
        cost = 0
        for i in range(len(self.tour) - 1):
            cost += self.dist_matrix[self.tour[i]][self.tour[i + 1]]
        return cost

    def __find_best_insertion(self) -> tuple[int, int]:
        """ 追加コスト比を評価して部分巡回路に追加する頂点の最適な挿入位置を決定
        Returns:
            best_city (int): 最適な挿入位置に追加する頂点
            best_i (int): 最適な挿入位置のインデックス 
        """
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

    def solve(self) -> list[int]:
        """ 最近挿入法で最適な巡回路を求める \n
        Returns:
            tour (list[int]): 最適な巡回路を表すリスト
        """
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
            n (int): 頂点数
            V (list[int]): 巡回路の頂点の osmid を格納したリスト
            dist_matrix (list[list[float]]): 頂点間の距離行列
            sp_matrix (list[list[list[int]]]): 頂点間の最短経路リスト行列
            tour (list[int]): 要素が頂点の index である最適な巡回路、初期解は最近挿入法を用いる
            min_cost (float): 巡回路の最小コスト
            tour_osmid (list[int]): 要素が頂点の osmid である最適な巡回路
            tour_paths (list[list[int]]): 巡回路の各エッジにおける最短経路リストを格納したリスト
        """
        super().__init__(node_csv_file, edge_csv_file)
        self.n: int = len(V)
        self.V: list[int] = V
        self.dist_matrix: list[list[float]] = [[0] * self.n for _ in range(self.n)]
        self.sp_matrix: list[list[list[int]]] = [[[]] * self.n for _ in range(self.n)]
        self._make_dist_matrix()
        self.tour = (_ := CHI(self.dist_matrix)).solve()
        self.min_cost: float = self.calc_cost(self.tour)
        self.tour_osmid: list[int] = [self.V[i] for i in self.tour]
        self.tour_paths = [self.sp_matrix[self.tour[i]][self.tour[i+1]] for i in range(self.n - 1)]

    def _make_dist_matrix(self) -> None:
        """ 頂点間の距離行列を計算する関数 """
        for v in self.V:
            min_cost = super().solve(v)
            for u in self.V:
                self.dist_matrix[self.V.index(v)][self.V.index(u)] = min_cost[u]
                self.sp_matrix[self.V.index(v)][self.V.index(u)] = self.get_shortest_path(v, u)

    def _two_opt_swap(self, i: int, j: int) -> list[int]:
        """ 2-OPT のエッジ交換操作を行う関数 \n
        Args:
            i (int): 交換するエッジのインデックス
            j (int): 交換するエッジのインデックス
        Returns:
            new_tour (list[int]): エッジ交換後の巡回路
        """
        new_tour = self.tour[:i] + self.tour[i:j][::-1] + self.tour[j:]
        return new_tour
    
    def calc_cost(self, tour) -> float:
        """ 巡回路の総コストを計算 \n
        Args:
            tour (list[int]): 頂点の添字を要素として表現した巡回路
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
        improved = True
        while improved:
            improved = False
            for i in range(1, self.n - 1):
                for j in range(i + 1, self.n):
                    # 2-opt 近傍を探索
                    new_tour = self._two_opt_swap(i, j)
                    new_cost = self.calc_cost(new_tour)
                    if new_cost < self.min_cost:
                        self.tour = new_tour
                        self.min_cost = new_cost
                        improved = True  # 改善解の発見により近傍を再評価
                        break 
                if improved:
                    break
        self.tour_osmid = [self.V[i] for i in self.tour]
        self.tour_paths = [self.sp_matrix[self.tour[i]][self.tour[i+1]] for i in range(self.n - 1)]
        return {'tour_osmid': self.tour_osmid, 'cost': self.min_cost, 'multi_paths': self.tour_paths}
    