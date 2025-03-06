from puzzle import *

class Solution:
    def __init__(self):
        self._puzzle = None
        self._answer = None

    def solve(self, method: Method):
        self._puzzle = Puzzle(method)


if __name__ == "__main__":
    Solution().solve(ConsoleMethod())