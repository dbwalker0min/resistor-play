from itertools import combinations
from itertools import product

def closest_resistor_combo(resistors, target, max_resistors=3):
    """
    Finds the combination of 1, 2, or 3 resistors (in series) whose total resistance is closest to the target value.

    Args:
        resistors (list of float): Available resistor values.
        target (float): Desired resistance value.
        max_resistors (int): Maximum number of resistors to use (default 3).

    Returns:
        tuple: (best_combo, best_total, error)
            best_combo (tuple): The resistor values chosen.
            best_total (float): The total resistance of the combination.
            error (float): The absolute difference from the target.
    """
    # Filter out resistors less than 1% of target and greater than target
    min_resistor = target * 0.01
    filtered = [r for r in resistors if min_resistor <= r <= target]

    best_combo = None
    best_total = None
    min_error = float('inf')

    for n in range(1, max_resistors + 1):
        for combo in product(filtered, repeat=n):
            total = sum(combo)
            error = abs(total - target)
            if error < min_error:
                min_error = error
                best_combo = combo
                best_total = total

    return best_combo, best_total, min_error

# Example usage:
if __name__ == "__main__":
    resistors = [100, 220, 330, 470, 680, 1000]
    target = 743
    combo, total, error = closest_resistor_combo(resistors, target)
    print(f"Best combo: {combo}, Total: {total}, Error: {error}")