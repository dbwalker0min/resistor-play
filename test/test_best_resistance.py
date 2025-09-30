from pytest import approx
from best_resistance.bests import best1, best2s, best2p, error, series, parallel
from best_resistance.types import Resistor
from best_resistance.eseries import generate_e_series
import pickle
from pprint import pprint
import csv
from inline_snapshot import snapshot

with open("test/data/resistor_values.pkl", "rb") as f:
    all_resistors = pickle.load(f)

e6_resistors = generate_e_series(6, min_decade=0, max_decade=9)


def test_best_resistance1():
    bests = []
    for resistance in range(1000, 2000, 1):
        r = float(resistance)
        best = best1(r, e6_resistors)
        bests.append((r, best.sym, best.value))

    bests = [bests[0]] + [
        curr for prev, curr in zip(bests, bests[1:]) if curr[1] != prev[1]
    ]

    assert bests == snapshot()


def test_best_resistance2s():
    bests = []
    expected = [
        (1000.0, Resistor(sym="1.0k", value=1000.0), Resistor(sym="0", value=0), 0.0),
        (
            1001.0,
            Resistor(sym="1.0k", value=1000.0),
            Resistor(sym="1.0", value=1.0),
            0.0,
        ),
        (
            1002.0,
            Resistor(sym="1.0k", value=1000.0),
            Resistor(sym="2.2", value=2.2),
            0.0199600798403239,
        ),
        (
            1003.0,
            Resistor(sym="1.0k", value=1000.0),
            Resistor(sym="3.3", value=3.3),
            0.0299102691924182,
        ),
        (
            1005.0,
            Resistor(sym="1.0k", value=1000.0),
            Resistor(sym="4.7", value=4.7),
            -0.02985074626865219,
        ),
        (
            1006.0,
            Resistor(sym="1.0k", value=1000.0),
            Resistor(sym="6.8", value=6.8),
            0.07952286282305711,
        ),
        (
            1009.0,
            Resistor(sym="1.0k", value=1000.0),
            Resistor(sym="10", value=10.0),
            0.09910802775024777,
        ),
        (
            1013.0,
            Resistor(sym="1.0k", value=1000.0),
            Resistor(sym="15", value=15.0),
            0.19743336623889435,
        ),
        (
            1019.0,
            Resistor(sym="1.0k", value=1000.0),
            Resistor(sym="22", value=22.0),
            0.2944062806673209,
        ),
        (
            1028.0,
            Resistor(sym="1.0k", value=1000.0),
            Resistor(sym="33", value=33.0),
            0.48638132295719844,
        ),
        (
            1041.0,
            Resistor(sym="1.0k", value=1000.0),
            Resistor(sym="47", value=47.0),
            0.5763688760806917,
        ),
        (
            1058.0,
            Resistor(sym="1.0k", value=1000.0),
            Resistor(sym="68", value=68.0),
            0.945179584120983,
        ),
        (
            1085.0,
            Resistor(sym="1.0k", value=1000.0),
            Resistor(sym="100", value=100.0),
            1.3824884792626728,
        ),
        (
            1126.0,
            Resistor(sym="1.0k", value=1000.0),
            Resistor(sym="150", value=150.0),
            2.1314387211367674,
        ),
        (
            1186.0,
            Resistor(sym="1.0k", value=1000.0),
            Resistor(sym="220", value=220.00000000000003),
            2.866779089376054,
        ),
        (
            1276.0,
            Resistor(sym="1.0k", value=1000.0),
            Resistor(sym="330", value=330.0),
            4.231974921630094,
        ),
        (
            1401.0,
            Resistor(sym="1.0k", value=1000.0),
            Resistor(sym="470", value=470.0),
            4.925053533190578,
        ),
        (1500.0, Resistor(sym="1.5k", value=1500.0), Resistor(sym="0", value=0), 0.0),
        (
            1501.0,
            Resistor(sym="1.5k", value=1500.0),
            Resistor(sym="1.0", value=1.0),
            0.0,
        ),
        (
            1502.0,
            Resistor(sym="1.5k", value=1500.0),
            Resistor(sym="2.2", value=2.2),
            0.013315579227699431,
        ),
        (
            1503.0,
            Resistor(sym="1.5k", value=1500.0),
            Resistor(sym="3.3", value=3.3),
            0.019960079840316336,
        ),
        (
            1505.0,
            Resistor(sym="1.5k", value=1500.0),
            Resistor(sym="4.7", value=4.7),
            -0.019933554817272728,
        ),
        (
            1506.0,
            Resistor(sym="1.5k", value=1500.0),
            Resistor(sym="6.8", value=6.8),
            0.05312084993359592,
        ),
        (
            1509.0,
            Resistor(sym="1.5k", value=1500.0),
            Resistor(sym="10", value=10.0),
            0.06626905235255136,
        ),
        (
            1513.0,
            Resistor(sym="1.5k", value=1500.0),
            Resistor(sym="15", value=15.0),
            0.13218770654329146,
        ),
        (
            1519.0,
            Resistor(sym="1.5k", value=1500.0),
            Resistor(sym="22", value=22.0),
            0.19749835418038184,
        ),
        (
            1528.0,
            Resistor(sym="1.5k", value=1500.0),
            Resistor(sym="33", value=33.0),
            0.32722513089005234,
        ),
        (
            1541.0,
            Resistor(sym="1.5k", value=1500.0),
            Resistor(sym="47", value=47.0),
            0.3893575600259572,
        ),
        (
            1558.0,
            Resistor(sym="1.5k", value=1500.0),
            Resistor(sym="68", value=68.0),
            0.6418485237483954,
        ),
        (
            1585.0,
            Resistor(sym="1.5k", value=1500.0),
            Resistor(sym="100", value=100.0),
            0.9463722397476341,
        ),
        (
            1626.0,
            Resistor(sym="1.5k", value=1500.0),
            Resistor(sym="150", value=150.0),
            1.4760147601476015,
        ),
        (
            1686.0,
            Resistor(sym="1.5k", value=1500.0),
            Resistor(sym="220", value=220.00000000000003),
            2.0166073546856467,
        ),
        (
            1776.0,
            Resistor(sym="1.5k", value=1500.0),
            Resistor(sym="330", value=330.0),
            3.040540540540541,
        ),
        (
            1901.0,
            Resistor(sym="1.5k", value=1500.0),
            Resistor(sym="470", value=470.0),
            3.6296685954760655,
        ),
    ]
    for resistance in range(1000, 2000, 1):
        r = float(resistance)
        best = best2s(r, e6_resistors)
        bests.append((r, *best, 100 * error(resistance, series(*best))))

    if 0:
        with open("rser.csv", "w") as fid:
            writer = csv.writer(fid, lineterminator="\n")
            for b in bests:
                writer.writerow([b[0], b[1].value, b[2].value, b[3]])

    bests_trunc = [bests[0]] + [
        curr
        for prev, curr in zip(bests, bests[1:])
        if curr[1].value != prev[1].value or curr[2].value != prev[2].value
    ]

    assert bests_trunc == expected


def test_best_resistance2p():
    bests = []
    for resistance in range(1000, 2000, 1):
        r = float(resistance)
        best = best2p(r, e6_resistors)
        bests.append((r, *best, 100 * error(resistance, parallel(*best))))

    if 1:
        with open("rpar.csv", "w") as fid:
            writer = csv.writer(fid, lineterminator="\n")
            for b in bests:
                writer.writerow([b[0], b[1].value, b[2].value, b[3]])

    bests_trunc = [bests[0]] + [
        curr
        for prev, curr in zip(bests, bests[1:])
        if curr[1].value != prev[1].value or curr[2].value != prev[2].value
    ]
    pprint(bests_trunc)

    assert False

def test_par2_1002():
    par2 = best2p(1002, e6_resistors)
    print(par2)
    assert False