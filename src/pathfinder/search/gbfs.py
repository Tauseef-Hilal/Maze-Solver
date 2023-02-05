from __future__ import annotations
import time

from ..models.frontier import PriorityQueueFrontier
from ..models.grid import Grid
from ..models.solution import NoSolution, Solution


class GreedyBestFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using A* Search

        Args:
            grid (Grid): Grid of points
            callback (Optional[Visualiser], optional): Callback for 
            visualisation. Defaults to None.

        Returns:
            Solution: Solution found
        """
        start_time = time.time()

        # Create Node for the source cell
        node = grid.get_node(pos=grid.start)

        # Instantiate PriorityQueue frontier and add node into it
        frontier = PriorityQueueFrontier()
        frontier.add(
            node,
            priority=GreedyBestFirstSearch.heuristic(grid.start, grid.end)
        )

        # Keep track of G scores
        cost_so_far = {grid.start: 0}

        while True:
            # Return empty Solution object for no solution
            if frontier.is_empty():
                return NoSolution(
                    [], list(cost_so_far), (time.time() - start_time) * 1000
                )

            # Remove node from the frontier
            node = frontier.pop()

            # If reached destination point
            if node.state == grid.end:

                # Generate path and return a Solution object
                cells = []

                temp = node
                while temp.parent != None:
                    cells.append(temp.state)
                    temp = temp.parent

                cells.append(grid.start)
                cells.reverse()

                return Solution(
                    cells, list(cost_so_far), (time.time() - start_time) * 1000
                )

            # Determine possible actions
            for action, state in grid.get_neighbours(node.state).items():
                new_cost = cost_so_far[node.state] + grid.get_cost(state)

                if state not in cost_so_far or new_cost < cost_so_far[state]:
                    cost_so_far[state] = new_cost

                    n = grid.get_node(pos=state)
                    n.parent = node

                    if not n.action:
                        n.action = action

                    frontier.add(
                        node=n,
                        priority=GreedyBestFirstSearch.heuristic(
                            state, grid.end
                        )
                    )

    @staticmethod
    def heuristic(state: tuple[int, int], goal: tuple[int, int]) -> int:
        """Heuristic function for edtimating remaining distance

        Args:
            state (tuple[int, int]): Initial
            goal (tuple[int, int]): Final

        Returns:
            int: Distance
        """
        x1, y1 = state
        x2, y2 = goal

        return abs(x1 - x2) + abs(y1 - y2)