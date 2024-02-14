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

class Permute():
    def __init__(self):
        self._count = 0
        self._v = None

    def benchmark(self):
        self._count = 0
        self._v = [0] * 6
        self._permute(6)

        return self._count

    def _permute(self, n):
        self._count += 1
        if n != 0:
            n1 = n - 1
            self._permute(n1)
            for i in range(n1, -1, -1):
                self._swap(n1, i)
                self._permute(n1)
                self._swap(n1, i)

    def _swap(self, i, j):
        tmp = self._v[i]
        self._v[i] = self._v[j]
        self._v[j] = tmp

    def verify_result(self, result):
        return result == 8660
    
    def inner_benchmark_loop(self, inner_iterations):
        for _ in range(inner_iterations):
            if not self.verify_result(self.benchmark()):
                return False
        return True


import utime
class Run:
    def __init__(self, name):
        self._name = name
        self._benchmark_suite = Permute
        self._total = 0
        self._num_iterations = 200
        self._inner_iterations = 1

    def run_benchmark(self):
        print("Starting " + self._name + " benchmark ...")

        self._do_runs(self._benchmark_suite())
        self._report_benchmark()
        print()

    def measure(self, bench):
        start_time = utime.ticks_ms()
        if not bench.inner_benchmark_loop(self._inner_iterations):
            raise Exception("Benchmark failed with incorrect result")

        end_time = utime.ticks_ms()
        run_time = utime.ticks_diff(end_time, start_time)
        

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
            + str(round(self._total / self._num_iterations))
            + "ms total: "
            + str(self._total)
            + "ms\n"
        )

    def _print_result(self, run_time):
        print(self._name + ": iterations=1 runtime: " + str(run_time) + "ms")

    #def print_total(self):
        #print("Total Runtime: " + str(self._total) + "ms")

    def set_num_iterations(self, num_iterations):
        self._num_iterations = num_iterations

    def set_inner_iterations(self, inner_iterations):
        self._inner_iterations = inner_iterations


test = Run("Permute")
test.run_benchmark()