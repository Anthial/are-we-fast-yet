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


class Element:
    def __init__(self, v):
        self._val = v
        self.next = None

    def length(self):
        if self.next is None:
            return 1
        return 1 + self.next.length()


class List():
    def benchmark(self):
        result = self.tail(self.make_list(15), self.make_list(10), self.make_list(6))
        return result.length()

    def make_list(self, length):
        if length == 0:
            return None

        e = Element(length)
        e.next = self.make_list(length - 1)
        return e
    
    def inner_benchmark_loop(self, inner_iterations):
        for _ in range(inner_iterations):
            if not self.verify_result(self.benchmark()):
                return False
        return True

    @staticmethod
    def is_shorter_than(x, y):
        x_tail = x
        y_tail = y

        while y_tail is not None:
            if x_tail is None:
                return True

            x_tail = x_tail.next
            y_tail = y_tail.next

        return False

    def tail(self, x, y, z):
        if self.is_shorter_than(y, x):  # pylint: disable=arguments-out-of-order
            return self.tail(
                self.tail(x.next, y, z),
                self.tail(y.next, z, x),
                self.tail(z.next, x, y),
            )
        return z

    def verify_result(self, result):
        return result == 10

import time
class Run:
    def __init__(self, name):
        self._name = name
        self._benchmark_suite = List
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

test = Run("List")
test.run_benchmark()
