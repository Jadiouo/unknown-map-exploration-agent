"""Unknown-map exploration agent: information gain + distance + radius-2 clustering.

Only this file needs to replace the assignment's agent.py.
"""
from collections import deque

MOVES = {
    "UP": (-1, 0),
    "DOWN": (1, 0),
    "LEFT": (0, -1),
    "RIGHT": (0, 1),
}


class Agent:
    # Selected using separate training and validation synthetic maps.
    ALPHA = 1.0  # Number of unseen neighbors at the next frontier
    BETA = 1.0   # Shortest known travel distance to the frontier
    GAMMA = 0.0  # No wall penalty
    DELTA = 2.0  # Radius-two unknown cluster bonus

    def __init__(self):
        self.reset(0, 0, (0, 0))

    def reset(self, rows, cols, start_position):
        self.rows = rows
        self.cols = cols
        self.known = {tuple(start_position): "FREE"}
        self.visited = set()

    def act(self, percept):
        position = tuple(percept["position"])
        self.known[position] = "FREE"
        self.visited.add(position)

        for action, status in percept["neighbors"].items():
            dr, dc = MOVES[action]
            neighbor = (position[0] + dr, position[1] + dc)
            self.known[neighbor] = status
            if status == "GOAL":
                return action

        # A single BFS produces shortest paths to all reachable known cells.
        queue = deque([position])
        distances = {position: 0}
        first_steps = {position: None}
        while queue:
            current = queue.popleft()
            for action, (dr, dc) in MOVES.items():
                nxt = (current[0] + dr, current[1] + dc)
                if nxt not in distances and self.known.get(nxt) in ("FREE", "GOAL"):
                    distances[nxt] = distances[current] + 1
                    first_steps[nxt] = action if current == position else first_steps[current]
                    queue.append(nxt)

        frontiers = [p for p in distances if p not in self.visited]
        if frontiers:
            def score(p):
                unseen = 0
                walls = 0
                for dr, dc in MOVES.values():
                    r, c = p[0] + dr, p[1] + dc
                    if 0 <= r < self.rows and 0 <= c < self.cols:
                        if (r, c) not in self.known:
                            unseen += 1
                    if self.known.get((r, c)) == "WALL":
                        walls += 1
                cluster = 0
                for dr in range(-2, 3):
                    for dc in range(-2, 3):
                        if abs(dr) + abs(dc) != 2:
                            continue
                        r, c = p[0] + dr, p[1] + dc
                        if 0 <= r < self.rows and 0 <= c < self.cols:
                            if (r, c) not in self.known:
                                cluster += 1
                return (self.ALPHA * unseen - self.BETA * distances[p]
                        - self.GAMMA * walls + self.DELTA * cluster / 2.0)

            target = max(frontiers, key=lambda p: (score(p), -distances[p], -p[0], -p[1]))
            return first_steps[target]

        # Unreachable under the assignment's reachable-goal guarantee.
        for action, (dr, dc) in MOVES.items():
            if self.known.get((position[0] + dr, position[1] + dc)) == "FREE":
                return action
        return "UP"