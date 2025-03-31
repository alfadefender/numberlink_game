from puzzle import *


class Solution:
    def __init__(self):
        self._puzzle = None
        self._answer = None

    def solve(self, method_in, method_out):
        self._puzzle = Puzzle(method_in, method_out)
        self._puzzle.input_puzzle("graph11.txt")
        self._puzzle.solve_puzzle(1)
        self._puzzle.output_answer()


if __name__ == "__main__":
    Solution().solve(GRAPH_FROM_FILE, GRAPH_TO_IMG)