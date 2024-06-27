

# サンプルデータ (距離行列)
dist_matrix = [
    [0, 2, 12, 10],
    [2, 0, 6, 4],
    [7, 6, 0, 15],
    [10, 4, 5, 0]
]

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

    def calculate_cost(self) -> float:
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
    
# 初期巡回路の生成
chi = CHI(dist_matrix)

# 初期巡回路の表示
print("Initial tour:", chi.tour)
print("Initial cost:", chi.calculate_cost())


# 完成した巡回路の表示
chi.solve()
print("Final tour:", chi.tour)
print("Final cost:", chi.calculate_cost())
