from collections import deque
import heapq

class Item:
    def __init__(self, hue):
        self.hue = hue  # "red", "blue", "gray"
        self.position = None

    def __str__(self):
        return self.hue[0].upper()

class Cell:
    def __init__(self, item, target):
        self.item = item  # عنصر المغناطيس أو None
        self.target = target  # هدف إذا كانت الخلية هدفا

    def __str__(self):
        return "G" if self.target == "goal" else str(self.item)

class GameBoard:
    def __init__(self, grid_layout):
        self.grid = grid_layout
        self.size = len(grid_layout)
        self.num_cols = len(grid_layout[0]) if self.size > 0 else 0

    def swap_item(self, x1, y1, item, new_x, new_y):
        self.grid[x1][y1].item = None
        self.grid[new_x][new_y].item = item
        item.position = (new_x, new_y)

    def bfs(self, start):
        print("Starting BFS...")
        queue = deque([start])
        visited = set()
        path = []

        while queue:
            current = queue.popleft()
            x, y = current
            visited.add(current)
            path.append(current)

            print(f"Visiting: {current}")  # طباعة العقد المزارة

            # تحقق من الوصول إلى الهدف
            if self.grid[x][y].target == "goal":
                print("BFS Path to solution:", path)
                return path

            # إضافة الجيران إلى الطابور
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < self.size and 0 <= new_y < self.num_cols and (new_x, new_y) not in visited:
                    queue.append((new_x, new_y))

        print("No solution found in BFS.")
        return None

    def dfs(self, x, y, visited, path):
        print(f"Visiting: {(x, y)}")  # طباعة العقد المزارة
        visited.add((x, y))
        path.append((x, y))

        # تحقق من الوصول إلى الهدف
        if self.grid[x][y].target == "goal":
            print("DFS Path to solution:", path)
            return path

        # إضافة الجيران
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < self.size and 0 <= new_y < self.num_cols and (new_x, new_y) not in visited:
                result = self.dfs(new_x, new_y, visited, path)
                if result:
                    return result

        path.pop()  # إزالة العقدة إذا لم تؤدي إلى الحل
        return None

    def ucs(self, start):
        print("Starting UCS...")
        queue = []
        heapq.heappush(queue, (0, start))  # (cost, position)
        visited = set()
        path = []

        while queue:
            cost, current = heapq.heappop(queue)
            x, y = current
            visited.add(current)
            path.append(current)

            print(f"Visiting: {current} with cost: {cost}")  # طباعة العقد المزارة

            # تحقق من الوصول إلى الهدف
            if self.grid[x][y].target == "goal":
                print("UCS Path to solution:", path)
                return path

            # إضافة الجيران مع تكلفة الحركة
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < self.size and 0 <= new_y < self.num_cols and (new_x, new_y) not in visited:
                    new_cost = cost + 1  # كلفة الحركة تساوي الواحد
                    heapq.heappush(queue, (new_cost, (new_x, new_y)))

        print("No solution found in UCS.")
        return None

    def heuristic(self, position):
        # حساب المسافة الإقليدية إلى أقرب هدف
        x, y = position
        goal_positions = [(i, j) for i in range(self.size) for j in range(self.num_cols) if self.grid[i][j].target == 'goal']
        return min(abs(x - gx) + abs(y - gy) for gx, gy in goal_positions)

    def hill_climbing(self, start):
        print("Starting Hill Climbing...")
        current = start
        visited = set()
        path = [current]

        while True:
            visited.add(current)
            x, y = current
            print(f"Visiting: {current} with heuristic: {self.heuristic(current)}")  # طباعة العقد المزارة

            # تحقق من الوصول إلى الهدف
            if self.grid[x][y].target == "goal":
                print("Hill Climbing Path to solution:", path)
                return path

            # استكشاف الجيران
            neighbors = []
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < self.size and 0 <= new_y < self.num_cols and (new_x, new_y) not in visited:
                    neighbors.append((new_x, new_y))

            # تحديد الجار الأفضل بناءً على الهيورستيك
            next_move = None
            best_heuristic = float('inf')
            for neighbor in neighbors:
                h = self.heuristic(neighbor)
                if h < best_heuristic:
                    best_heuristic = h
                    next_move = neighbor

            # إذا لم يكن هناك جيران أفضل، نخرج من الحلقة
            if next_move is None:
                print("No better neighbor found, stopping.")
                break

            path.append(next_move)
            current = next_move

        print("No solution found in Hill Climbing.")
        return None

    def a_star(self, start):
        print("Starting A*...")
        queue = []
        heapq.heappush(queue, (0, start))  # (f, position)
        g_costs = {start: 0}
        visited = set()
        path = []

        while queue:
            f, current = heapq.heappop(queue)
            x, y = current
            visited.add(current)
            path.append(current)

            print(f"Visiting: {current} with f: {f}")  # طباعة العقد المزارة

            # تحقق من الوصول إلى الهدف
            if self.grid[x][y].target == "goal":
                print("A* Path to solution:", path)
                return path

            # إضافة الجيران
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < self.size and 0 <= new_y < self.num_cols:
                    new_cost = g_costs[current] + 1  # كلفة الحركة تساوي الواحد
                    
                    if (new_x, new_y) not in visited or new_cost < g_costs.get((new_x, new_y), float('inf')):
                        g_costs[(new_x, new_y)] = new_cost
                        f = new_cost + self.heuristic((new_x, new_y))  # حساب f
                        heapq.heappush(queue, (f, (new_x, new_y)))

        print("No solution found in A*.")
        return None

# تعريف الرقع
grids = {
    (5, 5): [
        [
            [Cell(None, None), Cell(None, None), Cell(None, 'goal'), Cell(None, None), Cell(None, None)],
            [Cell(None, None), Cell(None, None), Cell(Item('gray'), None), Cell(None, None), Cell(None, None)],
            [Cell(None, 'goal'), Cell(Item('gray'), None), Cell(None, 'goal'), Cell(Item('gray'), None), Cell(None, 'goal')],
            [Cell(None, None), Cell(None, None), Cell(Item('gray'), None), Cell(None, None), Cell(None, None)],
            [Cell(Item('red'), None), Cell(None, None), Cell(None, 'goal'), Cell(None, None), Cell(Item('blue'), None)]
        ],
        [
            [Cell(None, None), Cell(Item('red'), None), Cell(None, None), Cell(None, 'goal'), Cell(None, None)],
            [Cell(Item('gray'), None), Cell(None, None), Cell(None, None), Cell(None, None), Cell(None, None)],
            [Cell(None, 'goal'), Cell(None, None), Cell(Item('gray'), None), Cell(None, None), Cell(None, None)],
            [Cell(None, None), Cell(None, None), Cell(None, None), Cell(Item('gray'), None), Cell(None, None)],
            [Cell(None, None), Cell(None, None), Cell(Item('blue'), None), Cell(None, 'goal'), Cell(None, None)]
        ]
    ],
    (3, 2): [
        [
            [Cell(Item('blue'), None),  Cell(None, 'goal')],
            [Cell(None, None), Cell(Item('gray'), None)],
            [Cell(None, None), Cell(None, 'goal')]
        ]
    ]
}

def main():
    print("اختر رقعة:\n1. 5x5\n2. 3x2")
    grid_choice = int(input("اختر الرقم المناسب: ")) - 1

    if grid_choice == 0:
        grid_layout = grids[(5, 5)][0]  # اختيار الرقعة الأولى من 5x5
    elif grid_choice == 1:
        grid_layout = grids[(5, 5)][1]  # اختيار الرقعة الثانية من 5x5
    elif grid_choice == 2:
        grid_layout = grids[(3, 2)][0]  # اختيار الرقعة من 3x2
    else:
        print("اختيار غير صحيح.")
        return

    board = GameBoard(grid_layout)

    print("اختر خوارزمية:\n1. BFS\n2. DFS\n3. UCS\n4. Hill Climbing\n5. A*")
    algorithm_choice = int(input("اختر الرقم المناسب: "))

    start_position = (0, 0)  # بدء من الزاوية العليا اليسرى
    if algorithm_choice == 1:
        board.bfs(start_position)
    elif algorithm_choice == 2:
        visited = set()
        board.dfs(0, 0, visited, [])
    elif algorithm_choice == 3:
        board.ucs(start_position)
    elif algorithm_choice == 4:
        board.hill_climbing(start_position)
    elif algorithm_choice == 5:
        board.a_star(start_position)
    else:
        print("اختيار غير صحيح.")

if __name__ == "__main__":
    main()
