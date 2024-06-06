import pandas as pd
import numpy as np
import constant as c

def extract_node_datas(node_csv_file: str) -> list[dict]:
    """
    Args:
        node_csv_file (str): 頂点に関する情報を持つ csv ファイルの path
    Returns:
        data (list[dict]): 頂点の情報を格納したリスト
            'osmid': ある頂点 v の osmid
            'y': ある頂点 v の緯度
            'x': ある頂点 v の経度
    """
    df = pd.read_csv(node_csv_file)
    data = df[['osmid', 'y', 'x']].to_dict('records')
    return data

def extract_edge_datas(edge_csv_file: str) -> list[dict]:
    """ 辺の情報を持つ csv ファイルから必要な情報のみを抽出して整形
    Args:
        edge_csv_file (str): 辺に関する情報を持つ csv ファイルの path
    Returns:
        data (list[dict]): 辺の情報を格納したリスト
            'u': 頂点 u の osmid
            'v': 頂点 v の osmid
            'osmid': 辺 (u, v) の osmid
            'oneway': 一方通行かどうかを示す真偽値
            'reversed': 終点から始点への一方通行の場合、真
            'length': 辺の距離 [m]
            'maxspeed': 最高速度 [km/h]
    """
    df = pd.read_csv(edge_csv_file)
    df.replace('nan', np.nan, inplace=True)
    df['maxspeed'].fillna(40, inplace=True)
    data = df[['u', 'v', 'osmid', 'oneway', 'reversed', 'length', 'maxspeed']].to_dict('records')
    return data

if __name__ == '__main__':
    node = extract_node_datas(c.Path.node_csv)
    edge = extract_edge_datas(c.Path.edge_csv)
    print(node)
    print(edge)
    print(c.FontColor.YELLOW + 'Program ran successfully' + c.FontColor.END)
    