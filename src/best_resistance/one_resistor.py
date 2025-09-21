


def closest1(resistance: float | int, resistor_values: dict[str, float]) -> tuple[str, float]:
    """Find the closest resistor value from a list of resistor values.

    Args:
        resistance (float): The target resistance value.
        resistor_values (list of float): A list of available resistor values.

    Returns:
        float: The closest resistor value from the list.
    """
    closest_key = min(resistor_values, key=lambda k: abs(resistor_values[k] - resistance))
    closest = resistor_values[closest_key]
    return (closest_key, closest)