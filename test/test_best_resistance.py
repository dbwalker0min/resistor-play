from best_resistance.one_resistor import closest1
from best_resistance.two_resistors import closest2_series
import pickle

with open("test/data/resistor_values.pkl", "rb") as f:
    all_resistors = pickle.load(f)


def test_best_resistance1():
    bests = []
    for resistance in range(1000, 2000, 1):
        r = float(resistance)
        best = closest1(r, all_resistors)
        bests.append((r, best[1]))

    bests = [bests[0]] + [
        curr for prev, curr in zip(bests, bests[1:]) if curr[1] != prev[1]
    ]
    assert bests == [
        (1000.0, 1000.0),
        (1051.0, 1100.0),
        (1151.0, 1200.0),
        (1351.0, 1500.0),
        (1651.0, 1800.0),
        (1901.0, 2000.0),
    ]


def test_best_resistance2_series():
    bests = []
    for resistance in range(1000, 2000, 1):
        r = float(resistance)
        best = closest2_series(r, all_resistors)
        bests.append((r, best, 100*(best[0] + best[1] - r) / r))

    best_abs = list(map(abs, (b[2] for b in bests)))
    print(min(best_abs), max(best_abs))

    assert all(abs(b[2]) < 0.71 for b in bests)

def test_best_resistance2_parallel():
    pass
    # TODO