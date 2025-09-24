from best_resistance.one_resistor import closest1


def _find_best_pair(
    target: float,
    test_values: list[float],
) -> tuple[float, float]:
    """Helper function to find the best pair of values that sum to the target value.

    Args:
        target (float): The target value.
        test_values (list[float]): The list of values to test.

    Returns:
        tuple[float, float]: The best pair of values found.
    """
    best_error = float("inf")
    closest_pair: tuple[float, float] = (0.0, 0.0)
    for r in test_values:
        r2_target = target - r

        # The target is exceeded, so skip
        if r2_target <= 0:
            continue

        # Find the resistor value in resistor_values closest to r2_target
        r2 = min(test_values, key=lambda x: abs(x - r2_target))
        error = abs((r + r2) - target)
        if error < best_error:
            best_error = error
            closest_pair = (r, r2)
    return closest_pair


def closest2_series(resistance: float | int, resistor_values: dict[str, float], tolerance: float = 0.01) -> list[tuple[str, float]]:
    """Find the closest two series resistor values from a list of resistor values.

    Args:
        resistance (float | int): The target resistance value.
        resistor_value (dict[str, float]): A dictionary of available resistor values.
        tolerance (float): The acceptable relative tolerance (default is 0.01 for 1%).

    Returns:
        list[tuple[str, float]]: A list of tuples containing the closest resistor values.
    """

    # reduce the range of resistors to consider based on tolerance
    test_resistors = [r for r in resistor_values.values() 
                      if r <= resistance and r >= resistance * tolerance / 2]
    test_resistors.sort()

    # make sure 0 is included to allow single resistor solutions
    if test_resistors[0] != 0:
        test_resistors.insert(0, 0)


    return _find_best_pair(resistance, test_resistors)


def closest2_parallel(resistance: float | int, resistor_values: dict[str, float], tolerance: float = 0.01) -> list[tuple[str, float]]:
    """Find the closest two parallel resistor values from a list of resistor values.

    Args:
        resistance (float | int): The target resistance value.
        resistor_value (dict[str, float]): A dictionary of available resistor values.
        tolerance (float): The acceptable relative tolerance (default is 0.01 for 1%).

    Returns:
        list[tuple[str, float]]: A list of tuples containing the closest resistor values.
    """

    # perform the calculation in terms of conductance to make it easier
    target = 1/resistance

    conductor_values = {1/v for k, v in resistor_values.values() if v != 0}
    test_conductances = [
        r
        for r in resistor_values.values()
        if r <= resistance and r >= resistance * tolerance / 2
    ]
    test_resistors.sort()

    # make sure 0 is included to allow single resistor solutions
    if test_resistors[0] != 0:
        test_resistors.insert(0, 0)

    best_error = float("inf")
    closest_pair: tuple[float, float] = (0.0, 0.0)
    # loop over all the resistors
    for r in test_resistors:
        r2_target = resistance - r
        if r2_target <= 0:
            # resistance of additional resistor netgative. This means r is already too large.
            continue
        r2 = closest1(r2_target, resistor_values)[1]
        error = abs((r + r2) - resistance)
        if error < best_error:
            best_error = error
            closest_pair = (r, r2)

    return closest_pair
