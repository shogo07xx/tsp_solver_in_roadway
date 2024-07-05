class Transportation:
    car = '車'

class DelayCoefficient:
    node = 0.02                 # 右左折時減速にかかる遅延時間と直進時の遅延時間の平均を仮定 [min]
    traffic_light = 0.25        # 赤信号遅延時間と青信号遅延時間の平均を仮定 (1 * 1/4 + 0 * 3/4) [min]
    departure_and_stop = 0.07   # 出発時と停止時にかかる遅延時間を仮定 [min]

class Spot:
    class Coordinate:
        kgu = (34.908257, 135.161987)
        uddhichuo = (34.909740, 135.183655)
        sawatani_public_hall = (34.914239, 135.168343)
    class Name:
        kgu = '関西学院大学三田キャンパス'
        uddhichuo = 'ウッディタウン中央駅'
        sawatani_public_hall = '沢谷公会堂'

class MarginDist:
    get_road_network_radius = 1000
    search_radius_for_nearest_node = 200

class Path:
    node_csv = 'out/roadway_node_kgu_uddhichuo.csv'
    edge_csv = 'out/roadway_edge_kgu_uddhichuo.csv'

class FontColor:
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'
    CYAN = '\033[36m'
    END = '\033[0m'
