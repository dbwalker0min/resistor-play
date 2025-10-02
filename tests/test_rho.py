from best_resistance.bests import best_rho_1r1r
from best_resistance.eseries import generate_e_series
from best_resistance.types import Resistor
from kicad_sym_lib_access.get_lib_symbols import read_resistor_values
from pytest import approx


e24_resistors = generate_e_series(24, min_decade=0, max_decade=7)

jlcpcb_resistors = read_resistor_values("!Resistor-0603.kicad_sym")

def test_rho_1r1r_simple():
    rseries = 10e3
    rho_target = 5 / 3.3 - 1
    best = best_rho_1r1r(rho_target, e24_resistors, rseries)
    print(best)
    assert best["rtop"].sym == "4.7k"
    assert best["rbot"].sym == "9.1k"


def test_rho_1r1r_jlcpcb1():
    rseries = 41e3
    rho_target = 5 / 0.763 - 1
    best = best_rho_1r1r(rho_target, jlcpcb_resistors, rseries)
    print(best)
    assert best["rtop"].sym == "20kΩ"
    assert best["rbot"].sym == "3.6kΩ"

def test_rho_1r1r_jlcpcb2():
    rseries = 41e3
    rho_target = 3.3 / 0.763 - 1
    best = best_rho_1r1r(rho_target, jlcpcb_resistors, rseries)
    print(best)
    assert best["rtop"].sym == "49.9kΩ"
    assert best["rbot"].sym == "15kΩ"
    