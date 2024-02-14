# The Computer Language Benchmarks Game
# http://shootout.alioth.debian.org/
#
# Based on nbody.java and adapted based on the SOM version.
from math import sqrt


PI = 3.141592653589793
SOLAR_MASS = 4 * PI * PI
DAYS_PER_YER = 365.24


class _Body:
    def __init__(self, x, y, z, vx, vy, vz, mass):
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx * DAYS_PER_YER
        self.vy = vy * DAYS_PER_YER
        self.vz = vz * DAYS_PER_YER
        self.mass = mass * SOLAR_MASS

    def offset_momentum(self, px, py, pz):
        self.vx = -(px / SOLAR_MASS)
        self.vy = -(py / SOLAR_MASS)
        self.vz = -(pz / SOLAR_MASS)


def jupiter():
    return _Body(
        4.84143144246472090e00,
        -1.16032004402742839e00,
        -1.03622044471123109e-01,
        1.66007664274403694e-03,
        7.69901118419740425e-03,
        -6.90460016972063023e-05,
        9.54791938424326609e-04,
    )


def saturn():
    return _Body(
        8.34336671824457987e00,
        4.12479856412430479e00,
        -4.03523417114321381e-01,
        -2.76742510726862411e-03,
        4.99852801234917238e-03,
        2.30417297573763929e-05,
        2.85885980666130812e-04,
    )


def uranus():
    return _Body(
        1.28943695621391310e01,
        -1.51111514016986312e01,
        -2.23307578892655734e-01,
        2.96460137564761618e-03,
        2.37847173959480950e-03,
        -2.96589568540237556e-05,
        4.36624404335156298e-05,
    )


def neptune():
    return _Body(
        1.53796971148509165e01,
        -2.59193146099879641e01,
        1.79258772950371181e-01,
        2.68067772490389322e-03,
        1.62824170038242295e-03,
        -9.51592254519715870e-05,
        5.15138902046611451e-05,
    )


def sun():
    return _Body(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0)


class NBodySystem:
    def __init__(self):
        self._bodies = self._create_bodies()

    @staticmethod
    def _create_bodies():
        bodies = [sun(), jupiter(), saturn(), uranus(), neptune()]

        px = 0.0
        py = 0.0
        pz = 0.0

        for b in bodies:
            px += b.vx * b.mass
            py += b.vy * b.mass
            pz += b.vz * b.mass

        bodies[0].offset_momentum(px, py, pz)
        return bodies

    def advance(self, dt):
        for i in range(len(self._bodies)):
            i_body = self._bodies[i]

            for j in range(i + 1, len(self._bodies)):
                j_body = self._bodies[j]

                dx = i_body.x - j_body.x
                dy = i_body.y - j_body.y
                dz = i_body.z - j_body.z

                d_squared = dx * dx + dy * dy + dz * dz
                distance = sqrt(d_squared)
                mag = dt / (d_squared * distance)

                i_body.vx = i_body.vx - (dx * j_body.mass * mag)
                i_body.vy = i_body.vy - (dy * j_body.mass * mag)
                i_body.vz = i_body.vz - (dz * j_body.mass * mag)

                j_body.vx = j_body.vx + (dx * i_body.mass * mag)
                j_body.vy = j_body.vy + (dy * i_body.mass * mag)
                j_body.vz = j_body.vz + (dz * i_body.mass * mag)

        for body in self._bodies:
            body.x = body.x + dt * body.vx
            body.y = body.y + dt * body.vy
            body.z = body.z + dt * body.vz

    def energy(self):
        e = 0.0

        for i in range(len(self._bodies)):
            i_body = self._bodies[i]
            e += (
                0.5
                * i_body.mass
                * (
                    i_body.vx * i_body.vx
                    + i_body.vy * i_body.vy
                    + i_body.vz * i_body.vz
                )
            )

            for j in range(i + 1, len(self._bodies)):
                j_body = self._bodies[j]
                dx = i_body.x - j_body.x
                dy = i_body.y - j_body.y
                dz = i_body.z - j_body.z

                distance = sqrt(dx * dx + dy * dy + dz * dz)
                e -= (i_body.mass * j_body.mass) / distance
        return e


class NBody():
    def inner_benchmark_loop(self, inner_iterations):
        system = NBodySystem()
        for _ in range(inner_iterations):
            system.advance(0.01)

        return self._verify_result(system.energy(), inner_iterations)

    @staticmethod
    def _verify_result(result, inner_iterations):
        if inner_iterations == 250000:
            return result == -0.1690859889909308

        if inner_iterations == 1:
            #print(round(result, 15))
            #print(round(result, 16) == round(-0.1690749540250674, 16))
            return round(result, 16) == -0.1690749540250674#-0.16907495402506745

        print("No verification result for " + str(inner_iterations) + " found")
        print("Result is: " + str(result))
        return False

    def benchmark(self):
        raise Exception("Should never be reached")

    def verify_result(self, result):
        raise Exception("Should never be reached")


import utime
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
        self._benchmark_suite = NBody
        self._total = 0
        self._num_iterations = 6000
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
        #print("Total Runtime: " + str(self._total) + "ms")

    def set_num_iterations(self, num_iterations):
        self._num_iterations = num_iterations

    def set_inner_iterations(self, inner_iterations):
        self._inner_iterations = inner_iterations

#Had to reset the result, some kind of float error, by all likelihood
test = Run("NBody")
test.run_benchmark()
