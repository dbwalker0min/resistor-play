import os
from pathlib import Path
import re

from kicad_symlib_utility import KiCadSymbolLibrary


def real_resistor_value(value_str: str) -> float:
    """Convert a string representation of a resistor value to a float.

    Args:
        value_str (str): The string representation of the resistor value.

    Returns:
        float: The numeric value of the resistor.
    """
    multipliers = {
        "k": 1e3,
        "K": 1e3,
        "M": 1e6,
        "G": 1e9,
        "m": 1e-3,
    }
    assert value_str, "Input string is empty."

    # Remove trailing non-numeric, non-unit characters (e.g., Ω, Ohms, spaces)
    value_str = value_str.strip()
    # Remove all uppercase Omega symbols
    value_str = value_str.replace("\u03A9", "")
    # Remove "Ohm(s)" from the end (case insensitive)
    value_str = re.sub(r"\s*ohm(s)?$", "", value_str, flags=re.IGNORECASE)

    # Try IEC format: e.g., 4K7, 1M0, 10R, 2k2
    match = re.match(r"^(\d+)([kKMGmR])(\d*)$", value_str)
    if match:
        base, unit, decimal = match.groups()
        if unit in multipliers:
            num = float(base)
            if decimal:
                num += float("0." + decimal)
            return num * multipliers[unit]
        elif unit == "R":
            num = float(base)
            if decimal:
                num += float("0." + decimal)
            return num

    # Standard format: e.g., 4700, 4.7k, 1M
    match = re.match(r"^([0-9.]+)([kKMGm]?)$", value_str)
    if match:
        base, unit = match.groups()
        if unit in multipliers:
            return float(base) * multipliers[unit]
        else:
            return float(base)
    raise ValueError(f"Could not parse resistor value: {value_str}")


def read_resistor_values(library_name: str, keywords: list[str] | None = None) -> dict[str, float]:
    """Read resistor values from a KiCad symbol library file.

    Args:
        library_name (str): The name of the KiCad symbol library file.
        keywords (list[str]): A list of keywords to search for in the file.

    Returns:
        list[float]: A list of resistor values found in the file.
    """

    # Library files are located in the environment variable MY_SYM_DIR
    if "MY_SYM_DIR" not in os.environ:
        raise EnvironmentError("Environment variable 'MY_SYM_DIR' is not set.")
    library_path = Path(os.environ["MY_SYM_DIR"]).joinpath(library_name)

    lib = KiCadSymbolLibrary(library_path)

    resistor_values = {}
    for s, props in lib.get_all_symbols().items():
        # Skip template symbols
        if s.startswith('~'):
            continue
        ki_keywords = set(props.get("ki_keywords", "").split(" "))
        # if keywords is specified, skip symbols that do not match any keyword
        if keywords and ki_keywords.isdisjoint(keywords):
            continue

        value_str = props["Value"]
        try:
            value = real_resistor_value(value_str)
            resistor_values[s] = value
        except ValueError as e:
            if str(e).startswith("Could not parse resistor value:"):
                print(f"Warning: {e}")
            else:
                raise e from e

    return resistor_values
