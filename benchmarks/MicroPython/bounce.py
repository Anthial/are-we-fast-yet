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


class Ball:
    def __init__(self, random):
        self._x = random.next() % 500
        self._y = random.next() % 500
        self._x_vel = (random.next() % 300) - 150
        self._y_vel = (random.next() % 300) - 150

    def bounce(self):
        x_limit = 500
        y_limit = 500
        bounced = False

        self._x += self._x_vel
        self._y += self._y_vel

        if self._x > x_limit:
            self._x = x_limit
            self._x_vel = -abs(self._x_vel)
            bounced = True

        if self._x < 0:
            self._x = 0
            self._x_vel = abs(self._x_vel)
            bounced = True

        if self._y > y_limit:
            self._y = y_limit
            self._y_vel = -abs(self._y_vel)
            bounced = True

        if self._y < 0:
            self._y = 0
            self._y_vel = abs(self._y_vel)
            bounced = True

        return bounced


class Bounce():
    def inner_benchmark_loop(self, inner_iterations):
        for _ in range(inner_iterations):
            if not self.verify_result(self.benchmark()):
                return False
        return True

    def benchmark(self):
        random = Random()

        ball_count = 100
        bounces = 0
        balls = [None] * ball_count

        for i in range(ball_count):
            balls[i] = Ball(random)

        for i in range(50):
            for ball in balls:
                if ball.bounce():
                    bounces += 1

        return bounces

    def verify_result(self, result):
        return result == 1331
import utime

class Run:

    def __init__(self, name):
        self._name = name
        self._benchmark_suite = Bounce
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
            + str((self._total) / self._num_iterations)
            + "ms total: "
            + str(self._total)
            + "ms\n"
        )

    def _print_result(self, run_time):
        print(self._name + ": iterations=1 runtime: " + str(run_time) + "ms")


    #def print_total(self):
    #    print("Total Runtime: " + str(self._total) + "ms")

    def set_num_iterations(self, num_iterations):
        self._num_iterations = num_iterations

    def set_inner_iterations(self, inner_iterations):
        self._inner_iterations = inner_iterations
#STACK SIZE 4096*1024
test = Run("Bounce")
test.run_benchmark()
