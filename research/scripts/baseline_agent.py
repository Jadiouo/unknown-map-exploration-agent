"""Unknown-map explorer using a discovered-map BFS frontier policy."""
from collections import deque

MOVES = {
    "UP": (-1, 0),
    "DOWN": (1, 0),
    "LEFT": (0, -1),
    "RIGHT": (0, 1),
}


class Agent:
    def __init__(self):
        self.reset(0, 0, (0, 0))

    def reset(self, rows, cols, start_position):
        self.rows = rows
        self.cols = cols
        self.start_position = tuple(start_position)
        self.known = {self.start_position: "FREE"}
        self.visited = set()

    def act(self, percept):
        position = tuple(percept["position"])
        self.visited.add(position)
        self.known[position] = "FREE"
        for direction, state in percept["neighbors"].items():
            dr, dc = MOVES[direction]
            neighbor = (position[0] + dr, position[1] + dc)
            self.known[neighbor] = state
            if state == "GOAL":
                return direction

        # The nearest observed, traversable but not yet visited square is
        # a frontier. All BFS edges must be confirmed traversable.
        queue = deque([position])
        first_move = {position: None}
        while queue:
            current = queue.popleft()
            if current not in self.visited:
                return first_move[current]
            for direction, (dr, dc) in MOVES.items():
                neighbor = (current[0] + dr, current[1] + dc)
                if (neighbor not in first_move and
                        self.known.get(neighbor) in ("FREE", "GOAL")):
                    first_move[neighbor] = (direction if current == position
                                            else first_move[current])
                    queue.append(neighbor)
        # Under the assignment's guarantee, this is unreachable before goal.
        return next((direction for direction, (dr, dc) in MOVES.items()
                     if self.known.get((position[0]+dr, position[1]+dc)) == "FREE"),
                    "UP")