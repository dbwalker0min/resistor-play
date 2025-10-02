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
    """
    Finds the best pair of resistors in series from a given list to match a target resistance.
    Args:
        rtarget (float): The target resistance value to match.
        resistor_values (list[Resistor]): A list of available resistor objects, assumed to be sorted from smallest to largest by resistance value.
    Returns:
        list[Resistor]: A list containing the two Resistor objects whose series combination most closely matches the target resistance.
    Notes:
        - The function avoids repeating combinations by only considering resistor values greater than half the target resistance.
        - If a single resistor value just above the target is a better match, it will be selected as one of the pair (with the other being zero or the closest possible).
        - Requires the helper functions `best1`, `error`, and `series` to be defined elsewhere.
    """
    # Start with the closest resistor value less than the target.
    # Assume that the resistor values are sorted from smallest to largest
    
    best = None
    best_error = math.inf

    # Select a subset of resistor values to search. 
    # I want to start at half the resistance value.
    # In this way, I don't repeat combinations.
    # I want to end at the resistor value that's just larger than the target value. 
    # If that resistor's better, than I want to use it. 
    # The example is 1.499k, I want to be able to use 1.5k + 0 instead of 1.0k + 470.
    for r in (rv for rv in resistor_values if rv.value > rtarget/2):
        # calculate the other resistor value needed to hit the target
        r_other = best1(rtarget - r.value, resistor_values)

        if (e := abs(error(rtarget, series(r, r_other)))) < best_error:
            best_error = e
            best = [r, r_other]
        
        if r.value >= rtarget:
            break
    
    return best
        
def best2p(rtarget: float, resistor_values: list[Resistor]) -> list[Resistor]:
    """
    Finds the best pair of resistors from a list whose parallel combination most closely matches a target resistance.
    Args:
        rtarget (float): The target resistance value to approximate.
        resistor_values (list[Resistor]): A list of available Resistor objects to choose from.
    Returns:
        list[Resistor]: A list containing the two Resistor objects whose parallel combination best approximates the target resistance.
                        If the target resistance exactly matches one of the resistor values, returns that resistor and an infinite resistor.
    Notes:
        - Assumes the existence of a Resistor class and helper functions: best1, error, and parallel.
        - Handles the case where the target resistance is exactly one of the available resistor values by returning it and an infinite resistor to avoid division by zero.
        - Searches for the pair of resistors that minimizes the absolute error between the target resistance and the parallel combination.
    """
    best = None
    best_error = math.inf

    # If the target resistance is exactly one of the resistor values, return it and an infinite resistor.
    # This will eliminate the possibility of a divide by zero error later.
    if rtarget in (res.value for res in resistor_values):
        return [best1(rtarget, resistor_values), Resistor('inf', math.inf)]

    # Start at the value just less than the target resistance
    # End when the other resistor value less than twice the target resistance.
    for r in (rv for rv, rvnext in zip(resistor_values, resistor_values[1:]) if rvnext.value >= rtarget and rv.value <= 2*rtarget):
        # calculate the other resistor value needed to hit the target
        rval_other = rtarget*r.value / (r.value - rtarget) if r.value > rtarget else math.inf
        r_other = best1(rval_other, resistor_values) if rval_other is not math.inf else Resistor('inf', math.inf)

        # calcuate the error with the real resistor
        err = abs(error(rtarget, parallel(r, r_other)))

        # if this is the last resistor value, then using 'inf' may be better.
        if r == resistor_values[-1]:
            if (e := abs(error(rtarget, r.value))) < err:
                r_other = Resistor('inf', math.inf)
                err = e

        if err < best_error:
            best_error = err
            best = [r, r_other]
        
    return best

def best_rho_1r1r(rho_target: float, resistor_values: list[Resistor], rseries: float, scale: float = math.sqrt(5)) -> dict[str, Resistor]:
    """
    Finds the best pair of resistors with ratio `rho` and nominal series resistance `rseries` from a given list of resistors. The
    total resistance scales by 1/`scale` to `scale`. The default of sqrt(5) is chosen to cover a decade for rseries.
    Args:
        rho_target (float): The target resistance ratio.
        resistor_values (list[Resistor]): A list of available resistor objects, assumed to be sorted from smallest to largest by resistance value.
        rseries (float): The nominal series resistance to be added to the combined resistance of the two resistors.
        scale (float): A scaling factor applied to the series resistance.
    """
    best = None
    best_error = math.inf

    # iterate over all the top resistor values from rseries/scale to rseries*scale
    for rtop in (rv for rv in resistor_values if rseries*scale >= rv.value >= rseries/scale):
        # calculate the other resistor value needed to hit the target
        rbot = best1(rtop/rho_target, resistor_values)

        if (e := abs(error(rho_target, rtop/rbot))) < best_error:
            best_error = e
            best = dict(rtop=rtop, rbot=rbot)
            
    return best

