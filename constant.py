class Spot:
    kgu = (34.91, 135.16)
    kgu_name = '関西学院大学三田キャンパス'
    uddhichuo = (34.91, 135.18)
    uddhichuo_name = 'ウッディタウン中央駅'

class MarginDist:
    get_road_network_radius = 1000
    search_radius_for_nearest_node = 200

class Path:
    node_csv = 'out/driveway_node_kgu_uddhichuo.csv'
    edge_csv = 'out/driveway_edge_kgu_uddhichuo.csv'

class FontColor:
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'
    CYAN = '\033[36m'
    END = '\033[0m'
