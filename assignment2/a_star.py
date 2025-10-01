# writing your code here
from collections import deque
from node import Node
import heapq

# 曼哈顿距离启发函数：H(n) = |x1 - x2| + |y1 - y2|
def heuristic(node1, node2):
    """计算两个节点之间的曼哈顿距离作为启发成本 H(n)"""
    x1, y1 = node1.x, node1.y
    x2, y2 = node2.x, node2.y
    return abs(x1 - x2) + abs(y1 - y2)

#a_star算法是对Dijkstra算法的优化，在保留g_score的基础上增加了h_score（离终点距离），最终检查g_score+h_score，确保后续检索时不再探索绕弯节点
def a_star(start, end):
    # 开放列表 (Open List)：使用 heapq 实现的最小堆，存储 (F_score, node)F_score 必须是元组的第一个元素，确保 heapq 优先比较它

    #初始化计数器
    push_count = 0

    # 初始化起点的 G_score 为 0，F_score 为 H(start)
    start.g_score = 0
    start.f_score = heuristic(start, end)
    open_heap = [(start.f_score, push_count, start)]# 连计数器也一起存储进去
    came_from = {}
    visit_history = []

    while open_heap:
        # 取出 F_score 最小的节点; heapq.heappop() 移除并返回最小元素; Python 的 heap 是最小堆
        current_f_score, _, current = heapq.heappop(open_heap)# 但计数器本身不必取出
        # 避免处理已经找到更优路径的节点 (在堆中可能存在旧的、F值更高的副本)
        if current_f_score > current.f_score:
            continue
        visit_history.append(current)
        if current == end:
            return reconstruct_path(came_from, current), visit_history
        # 遍历邻居
        for neighbor in current.get_neighbors():
            if neighbor.type == 'wall':
                continue
            # 假设网格移动成本为 1
            tentative_g_score = current.g_score + 1
            # A* 核心判断：如果找到一条更优（G值更小）的路径
            if tentative_g_score < neighbor.g_score:
                # 记录新的最优路径和 G_score
                came_from[neighbor] = current
                neighbor.g_score = tentative_g_score
                # 计算 H_score 和新的 F_score
                h_score = heuristic(neighbor, end)
                neighbor.f_score = neighbor.g_score + h_score
                # 更新计数器
                push_count += 1
                # 将节点推入开放列表（优先队列）；重点：push_count作为平局的补丁，跳过未定义的对Node的比较。
                heapq.heappush(open_heap, (neighbor.f_score, push_count, neighbor))

    return None # No path found

def reconstruct_path(came_from, current):
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path