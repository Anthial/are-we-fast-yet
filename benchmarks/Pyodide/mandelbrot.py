# This benchmark has been modified based on the SOM benchmark.
#
# Copyright (C) 2004-2013 Brent Fulgham
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#
#   * Neither the name of "The Computer Language Benchmarks Game" nor the name
#     of "The Computer Language Shootout Benchmarks" nor the names of its
#     contributors may be used to endorse or promote products derived from this
#     software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# The Computer Language Benchmarks Game
# http://benchmarksgame.alioth.debian.org
#
#  contributed by Karl von Laudermann
#  modified by Jeremy Echols
#  modified by Detlef Reichl
#  modified by Joseph LaFata
#  modified by Peter Zotov

# http://benchmarksgame.alioth.debian.org/u64q/program.php?test=mandelbrot&lang=yarv&id=3


class Mandelbrot():
    def inner_benchmark_loop(self, inner_iterations):
        return self._verify_result(self._mandelbrot(inner_iterations), inner_iterations)

    def benchmark(self):
        raise Exception("Should never be reached")

    def verify_result(self, result):
        raise Exception("Should never be reached")

    @staticmethod
    def _verify_result(result, inner_iterations):
        if inner_iterations == 500:
            return result == 191
        if inner_iterations == 750:
            return result == 50
        if inner_iterations == 1:
            return result == 128

        print("No verification result for " + str(inner_iterations) + " found")
        print("Result is: " + str(result))
        return False

    @staticmethod
    def _mandelbrot(size):
        _sum = 0
        byte_acc = 0
        bit_num = 0

        y = 0

        while y < size:
            ci = (2.0 * y / size) - 1.0
            x = 0

            while x < size:
                zrzr = 0.0
                zi = 0.0
                zizi = 0.0
                cr = (2.0 * x / size) - 1.5

                z = 0
                not_done = True
                escape = 0
                while not_done and z < 50:
                    zr = zrzr - zizi + cr
                    zi = 2.0 * zr * zi + ci

                    zrzr = zr * zr
                    zizi = zi * zi

                    if zrzr + zizi > 4.0:
                        not_done = False
                        escape = 1
                    z += 1

                byte_acc = (byte_acc << 1) + escape
                bit_num = bit_num + 1

                if bit_num == 8:
                    _sum ^= byte_acc
                    byte_acc = 0
                    bit_num = 0
                elif x == size - 1:
                    byte_acc <<= 8 - bit_num
                    _sum ^= byte_acc
                    byte_acc = 0
                    bit_num = 0
                x += 1
            y += 1

        return _sum


import time
#The following Run class falls under:
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
class Run:
    def __init__(self, name):
        self._name = name
        self._benchmark_suite = Mandelbrot
        self._total = 0
        self._num_iterations = 1600*3200
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


test = Run("Mandelbrot")
test.run_benchmark()
