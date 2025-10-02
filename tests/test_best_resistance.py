import math
from pytest import approx
from best_resistance.bests import best1, best2s, best2p, error, series, parallel
from best_resistance.types import Resistor
from best_resistance.eseries import generate_e_series
from pprint import pprint
import csv
from inline_snapshot import snapshot

e6_resistors = generate_e_series(6, min_decade=0, max_decade=7)


def test_best_resistance1():
    bests = []
    for resistance in range(1000, 2000, 1):
        r = float(resistance)
        best = best1(r, e6_resistors)
        bests.append((r, best.sym, best.value))

    bests = [bests[0]] + [
        curr for prev, curr in zip(bests, bests[1:]) if curr[1] != prev[1]
    ]

    assert bests == snapshot([(1000.0 ,'1.0k',1000.0 ),(1251.0 ,'1.5k',1500.0 ),(1851.0 ,'2.2k',2200.0 )])

def test_best_resistance1_big():
    # 1GOhm is a big resistor
    best = best1(1e9, e6_resistors)
    print(best)
    assert best.value == approx(6.80e6)

def test_best_resistance2s():
    bests = []
    for resistance in [(1.01**i) * 1000 for i in range(int(1.0/math.log10(1.01)))]:
        r = float(resistance)
        best = best2s(r, e6_resistors)
        bests.append((r, *best, 100 * error(resistance, series(*best))))

    if 0:
        with open("rser.csv", "w") as fid:
            writer = csv.writer(fid, lineterminator="\n")
            for b in bests:
                writer.writerow([b[0], b[1].value, b[2].value, b[3]])

    bests_trunc = [bests[0]] + [
        (int(curr[0]), curr[1].sym, curr[2].sym) for prev, curr in zip(bests, bests[1:])
            if curr[1].value != prev[1].value or curr[2].value != prev[2].value
    ]
    pprint(bests_trunc)
    assert bests_trunc == snapshot([(1000.0 ,Resistor (sym ='1.0k',value =1000.0 ),Resistor (sym ='0',value =0 ),0.0 ),(1010 ,'680','330'),(1020 ,'1.0k','22'),(1030 ,'1.0k','33'),(1040 ,'1.0k','47'),(1061 ,'1.0k','68'),(1093 ,'1.0k','100'),(1126 ,'680','470'),(1196 ,'1.0k','220'),(1282 ,'1.0k','330'),(1347 ,'680','680'),(1361 ,'1.0k','330'),(1402 ,'1.0k','470'),(1488 ,'1.5k','0'),(1503 ,'1.5k','3.3'),(1518 ,'1.5k','22'),(1533 ,'1.5k','33'),(1549 ,'1.5k','47'),(1564 ,'1.5k','68'),(1596 ,'1.5k','100'),(1628 ,'1.5k','150'),(1677 ,'1.0k','680'),(1711 ,'1.5k','220'),(1780 ,'1.5k','330'),(1909 ,'1.5k','470'),(1986 ,'1.0k','1.0k'),(2006 ,'1.5k','470'),(2088 ,'1.5k','680'),(2194 ,'2.2k','0'),(2216 ,'2.2k','15'),(2238 ,'2.2k','33'),(2261 ,'2.2k','68'),(2306 ,'2.2k','100'),(2329 ,'2.2k','150'),(2400 ,'2.2k','220'),(2473 ,'1.5k','1.0k'),(2522 ,'2.2k','330'),(2625 ,'2.2k','470'),(2786 ,'2.2k','680'),(2958 ,'1.5k','1.5k'),(3017 ,'2.2k','680'),(3047 ,'2.2k','1.0k'),(3267 ,'3.3k','0'),(3333 ,'3.3k','33'),(3366 ,'3.3k','68'),(3400 ,'3.3k','100'),(3434 ,'3.3k','150'),(3503 ,'3.3k','220'),(3609 ,'3.3k','330'),(3682 ,'2.2k','1.5k'),(3756 ,'3.3k','470'),(3908 ,'3.3k','680'),(4149 ,'3.3k','1.0k'),(4360 ,'2.2k','2.2k'),(4404 ,'3.3k','1.0k'),(4537 ,'4.7k','0'),(4722 ,'4.7k','22'),(4769 ,'4.7k','68'),(4817 ,'3.3k','1.5k'),(4865 ,'4.7k','150'),(4913 ,'4.7k','220'),(5012 ,'4.7k','330'),(5113 ,'4.7k','470'),(5320 ,'4.7k','680'),(5482 ,'3.3k','2.2k'),(5648 ,'4.7k','1.0k'),(5995 ,'4.7k','1.5k'),(6428 ,'3.3k','3.3k'),(6623 ,'6.8k','0'),(6823 ,'6.8k','22'),(6892 ,'4.7k','2.2k'),(6960 ,'6.8k','150'),(7030 ,'6.8k','220'),(7100 ,'6.8k','330'),(7243 ,'6.8k','470'),(7389 ,'6.8k','680'),(7689 ,'6.8k','1.0k'),(7922 ,'4.7k','3.3k'),(8162 ,'6.8k','1.5k'),(8664 ,'6.8k','2.2k'),(9289 ,'4.7k','4.7k'),(9476 ,'6.8k','2.2k'),(9570 ,'10k','0')])

    # better, than I want to use it. The example is 1.499k, I want to be able to use 1.5k + 0 instead of 1.0k + 470.
def test_best2s_1499():
    ser2 = best2s(1499, e6_resistors)
    print(ser2)
    assert ser2[0].sym == '1.5k'
    assert ser2[1].sym == '0'

def test_best_resistance2p():
    bests = []
    for resistance in [(1.01**i) * 1000 for i in range(int(1.0/math.log10(1.01)))]:
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

    modified = []
    for targ, r1, r2, _ in bests_trunc:
        modified.append((int(targ), r1.sym, r2.sym))
    pprint(modified)

    assert modified == snapshot([(1000 ,'1.0k','inf'),(1020 ,'1.5k','3.3k'),(1093 ,'1.5k','4.7k'),(1104 ,'2.2k','2.2k'),(1126 ,'1.5k','4.7k'),(1196 ,'1.5k','6.8k'),(1282 ,'1.5k','10k'),(1321 ,'2.2k','3.3k'),(1347 ,'1.5k','15k'),(1388 ,'1.5k','22k'),(1430 ,'1.5k','33k'),(1459 ,'1.5k','47k'),(1474 ,'1.5k','100k'),(1488 ,'1.5k','220k'),(1503 ,'1.5k','inf'),(1596 ,'2.2k','6.8k'),(1745 ,'2.2k','10k'),(1871 ,'2.2k','15k'),(1947 ,'3.3k','4.7k'),(1986 ,'2.2k','22k'),(2047 ,'2.2k','33k'),(2088 ,'2.2k','47k'),(2130 ,'2.2k','68k'),(2151 ,'2.2k','100k'),(2173 ,'2.2k','150k'),(2194 ,'2.2k','1.0M'),(2216 ,'3.3k','6.8k'),(2353 ,'4.7k','4.7k'),(2424 ,'3.3k','10k'),(2625 ,'3.3k','15k'),(2759 ,'4.7k','6.8k'),(2842 ,'3.3k','22k'),(2958 ,'3.3k','33k'),(3078 ,'3.3k','47k'),(3140 ,'3.3k','68k'),(3203 ,'4.7k','10k'),(3235 ,'3.3k','150k'),(3267 ,'3.3k','330k'),(3300 ,'3.3k','inf'),(3400 ,'6.8k','6.8k'),(3503 ,'4.7k','15k'),(3756 ,'4.7k','22k'),(3987 ,'6.8k','10k'),(4108 ,'4.7k','33k'),(4232 ,'4.7k','47k'),(4360 ,'4.7k','68k'),(4492 ,'4.7k','100k'),(4537 ,'4.7k','150k'),(4629 ,'4.7k','330k'),(4675 ,'4.7k','1.0M'),(4722 ,'4.7k','inf'),(5012 ,'10k','10k'),(5113 ,'6.8k','22k'),(5482 ,'6.8k','33k'),(5819 ,'6.8k','47k'),(5995 ,'10k','15k'),(6116 ,'6.8k','68k'),(6301 ,'6.8k','100k'),(6492 ,'6.8k','150k'),(6623 ,'6.8k','220k'),(6689 ,'6.8k','470k'),(6756 ,'6.8k','1.0M'),(6823 ,'6.8k','inf'),(6892 ,'10k','22k'),(7389 ,'10k','33k'),(7537 ,'15k','15k'),(7613 ,'10k','33k'),(8001 ,'10k','47k'),(8578 ,'10k','68k'),(8838 ,'15k','22k'),(9016 ,'10k','100k'),(9289 ,'10k','150k'),(9570 ,'10k','220k'),(9666 ,'10k','330k'),(9763 ,'10k','470k'),(9860 ,'10k','680k')])

def test_par2_1002():
    par2 = best2p(1002, e6_resistors)
    print(par2)
    assert par2[0].sym == '1.0k'
    assert par2[1].sym == 'inf'

def test_par2_999():
    par2 = best2p(999, e6_resistors)
    print(par2)
    assert par2[0].sym == '1.0k'
    assert par2[1].sym == '1.0M'