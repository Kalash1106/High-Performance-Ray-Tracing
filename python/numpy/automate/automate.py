from automan.api import Problem, Automator, mdict, Simulation, filter_cases
from matplotlib import pyplot as plt
import numpy as np


class SimpleRayTracer(Problem):
    def get_name(self):
        return "simpleraytracer"

    def setup(self):
        base_cmd = "python ../main.py"
        opts = mdict(depth=[5, 50, 100], samples=[5], nspheres=[1, 2, 3])
        self.cases = [
            Simulation(
                root=self.input_path(
                    f"n{kw['nspheres']}_d{kw['depth']}_s{kw['samples']}"
                ),
                base_command=base_cmd,
                **kw,
            )
            for kw in opts
        ]

    def run(self):
        self.make_output_dir()

        s50d5_cases = filter_cases(self.cases, samples=5, depth=5)
        times_s50d5 = []
        for c in s50d5_cases:
            with open(c.input_path('stdout.txt')) as fd:
                times_s50d5.append(float(fd.read()))
        
        s50d50_cases = filter_cases(self.cases, samples=5, depth=50)
        times_s50d50 = []
        for c in s50d50_cases:
            with open(c.input_path('stdout.txt')) as fd:
                times_s50d50.append(float(fd.read()))
        
        s50d100_cases = filter_cases(self.cases, samples=5, depth=100)
        times_s50d100 = []
        for c in s50d100_cases:
            with open(c.input_path('stdout.txt')) as fd:
                times_s50d100.append(float(fd.read()))
        
        nspheres = np.array([1, 2, 3], dtype=np.uint8)

        plt.figure()
        plt.grid()
        plt.plot(nspheres, times_s50d5, marker='o', label='MAX_DEPTH = 5')
        plt.plot(nspheres, times_s50d50, marker='o', label='MAX_DEPTH = 50')
        plt.plot(nspheres, times_s50d100, marker='o', label='MAX_DEPTH = 100')
        plt.ylabel('Time, s')
        plt.xlabel('Number of spheres')
        plt.title('Render time for 5 samples, idiomatic Python and numpy')
        plt.legend()
        plt.savefig(self.output_path('plot_s5.png'))
        plt.close()



if __name__ == "__main__":
    a = Automator(
        simulation_dir="outputs",
        output_dir="manuscript/figures",
        all_problems=[SimpleRayTracer],
    )
    a.run()
