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

class Random:
    def __init__(self):
        self._seed = 74755

    def next(self):
        self._seed = ((self._seed * 1309) + 13849) & 65535

        return self._seed



class Storage():
    def __init__(self):
        self._count = 0

    def benchmark(self):
        random = Random()
        self._count = 0
        self._build_tree_depth(7, random)
        return self._count

    def _build_tree_depth(self, depth, random):
        self._count += 1
        if depth == 1:
            return [None] * (random.next() % 10 + 1)

        arr = [None] * 4
        for i in range(4):
            arr[i] = self._build_tree_depth(depth - 1, random)
        return arr

    def verify_result(self, result):
        return result == 5461
    
    def inner_benchmark_loop(self, inner_iterations):
        for _ in range(inner_iterations):
            if not self.verify_result(self.benchmark()):
                return False
        return True


import time
class Run:
    def __init__(self, name):
        self._name = name
        self._benchmark_suite = Storage
        self._total = 0
        self._num_iterations = 3200
        self._inner_iterations = 1

    def run_benchmark(self):
        print("Starting " + self._name + " benchmark ...")

        self._do_runs(self._benchmark_suite())
        self._report_benchmark()
        print()

    def measure(self, bench):
        start_time = time.perf_counter_ns()
        if not bench.inner_benchmark_loop(self._inner_iterations):
            raise Exception("Benchmark failed with incorrect result")

        end_time = time.perf_counter_ns()
        run_time = (end_time - start_time)

        #self._print_result(run_time)

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
            + str((self._total/1000000) / self._num_iterations)
            + "ms total: "
            + str(self._total/1000000)
            + "ms\n"
        )

    #def _print_result(self, run_time):
        #print(self._name + ": iterations=1 runtime: " + str(run_time/1000000) + "ms")


    def print_total(self):
        print("Total Runtime: " + str(self._total) + "ms")

    def set_num_iterations(self, num_iterations):
        self._num_iterations = num_iterations

    def set_inner_iterations(self, inner_iterations):
        self._inner_iterations = inner_iterations

test = Run("Storage")
test.run_benchmark()
