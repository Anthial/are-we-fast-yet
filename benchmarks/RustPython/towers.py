# This code is based on the SOM class library.
#
# Copyright (c) 2001-2021 see AUTHORS.md file
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the 'Software'), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.



class _TowersDisk:
    def __init__(self, size):
        self.size = size
        self.next = None


class Towers():
    def __init__(self):
        self._piles = None
        self._moves_done = 0

    def _push_disk(self, disk, pile):
        top = self._piles[pile]

        if top is not None and disk.size >= top.size:
            raise Exception("Cannot put a big disk on a smaller one")

        disk.next = top
        self._piles[pile] = disk

    def _pop_disk_from(self, pile):
        top = self._piles[pile]
        if top is None:
            raise Exception("Attempting to remove a disk from an empty pile")

        self._piles[pile] = top.next
        top.next = None
        return top

    def _move_top_disk(self, from_pile, to_pile):
        self._push_disk(self._pop_disk_from(from_pile), to_pile)
        self._moves_done += 1

    def _build_tower_at(self, pile, disks):
        for i in range(disks, -1, -1):
            self._push_disk(_TowersDisk(i), pile)

    def _move_disks(self, disks, from_pile, to_pile):
        if disks == 1:
            self._move_top_disk(from_pile, to_pile)
        else:
            other_pile = (3 - from_pile) - to_pile
            self._move_disks(disks - 1, from_pile, other_pile)
            self._move_top_disk(from_pile, to_pile)
            self._move_disks(disks - 1, other_pile, to_pile)

    def benchmark(self):
        self._piles = [None, None, None]
        self._build_tower_at(0, 13)
        self._moves_done = 0
        self._move_disks(13, 0, 1)
        return self._moves_done

    def verify_result(self, result):
        return result == 8191
    
    def inner_benchmark_loop(self, inner_iterations):
        for _ in range(inner_iterations):
            if not self.verify_result(self.benchmark()):
                return False
        return True


import time
class Run:
    def __init__(self, name):
        self._name = name
        self._benchmark_suite = Towers
        self._total = 0
        self._num_iterations = 200
        self._inner_iterations = 1

    def run_benchmark(self):
        print("Starting " + self._name + " benchmark ...")

        self._do_runs(self._benchmark_suite())
        self._report_benchmark()
        print()

    def measure(self, bench):
        start_time = time.time()
        if not bench.inner_benchmark_loop(self._inner_iterations):
            raise Exception("Benchmark failed with incorrect result")

        end_time = time.time()
        run_time = (end_time - start_time)
        
        self._print_result(run_time)

        self._total += run_time

    def _do_runs(self, bench):
        for _ in range(self._num_iterations):
            self.measure(bench)

    def _report_benchmark(self):
        print(
            self._name
            + ": iterations="
            + str(self._num_iterations)
            + " average: "
            + str((self._total*1000) / self._num_iterations)
            + "ms total: "
            + str(self._total*1000)
            + "ms\n"
        )

    def _print_result(self, run_time):
        print(self._name + ": iterations=1 runtime: " + str(run_time* 1000) + "ms")

    def print_total(self):
        print("Total Runtime: " + str(self._total) + "ms")

    def set_num_iterations(self, num_iterations):
        self._num_iterations = num_iterations

    def set_inner_iterations(self, inner_iterations):
        self._inner_iterations = inner_iterations

test = Run("Towers")
test.run_benchmark()
