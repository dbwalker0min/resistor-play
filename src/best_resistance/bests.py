from best_resistance.types import Resistor
import math

def error(expected: float, actual: float) -> float:
    """Return the error (as a decimal) between an expected and actual result"""
    return ((actual - expected)/expected)

def series(*args: list[Resistor]) -> float:
    return sum([a.value for a in args])

def parallel(*args: list[Resistor]) -> float:
    if any(a.value == 0 for a in args):
        return 0
    return 1/sum([1/a.value for a in args])

def best1(resistance: float | int, resistor_values: list[Resistor]) -> Resistor:
    """Find the closest resistor value from a list of resistor values.

    Args:
        resistance (float): The target resistance value.
        resistor_values (list of float): A list of available resistor values.

    Returns:
        float: The closest resistor value from the list.
    """
    return min(resistor_values, key=lambda k: abs(k.value - resistance))
    

def best2s(rtarget: float, resistor_values: list[Resistor]) -> list[Resistor]:
    """This computes the best pair of resistors in series to match a target resistance"""
    # Start with the closest resistor value less than the target.
    # Assume that the resistor values are sorted from smallest to largest
    
    best = None
    best_error = math.inf
    # Select a subset of resistor values to search. I want to start at half the resistance value.
    # By starting here, I don't repeat combinations.
    # I want to end at the resistor value that's just larger than the target value. If that resistor's
    # better, than I want to use it. The example is 1.999k
    last_candidate = [r for r in resistor_values if r.value > rtarget][0]
    print(f'{rtarget=}, {last_candidate.value=}')
    candidates = [r for r in resistor_values if rtarget/2 <= r.value <= last_candidate.value]
    for r_base in candidates:
        rval_other = rtarget - r_base.value
        r_other = best1(rval_other, resistor_values) if rval_other > 0 else Resistor('0', 0)
        if error(rtarget, series(r_base, r_other)) < best_error:
            best = [r_base, r_other]
    
    return best
        
def best2p(rtarget: float, resistor_values: list[Resistor]) -> list[Resistor]:
    best = None
    best_error = math.inf

    # Go between 50% of the target resistance to twice the resistance
    first_candidate = [r for r in resistor_values if r.value < rtarget][-1]
    candidates = [r for r in resistor_values if 2*rtarget > r.value >= first_candidate.value]

    # if it solves exactly, just return it. This will avoid a divide-by-zero error
    if any((r_exact := r).value == rtarget for r in candidates):
        return [r_exact, Resistor('inf', math.inf)]

    for r in candidates:
        rval_other = rtarget*r.value / (-rtarget + r.value)
        r_other = best1(rval_other, resistor_values) if rval_other > 0 else Resistor('inf', math.inf)
        error = abs(parallel(r_other, r) - rtarget)
        print(f'{r.value=}, {r_other.value=}, {rval_other=:.2f}, {error=}')
        if error < best_error:
            best_error = error
            best = [r, r_other]

    return best

