LENGTH = {
    "km": 1000, "kilometers": 1000, "kilometer": 1000,
    "m": 1, "meters": 1, "meter": 1,
    "cm": 0.01, "centimeters": 0.01, "centimeter": 0.01,
    "mm": 0.001, "millimeters": 0.001, "millimeter": 0.001,
    "miles": 1609.344, "mile": 1609.344, "mi": 1609.344,
    "yards": 0.9144, "yard": 0.9144, "yd": 0.9144,
    "feet": 0.3048, "foot": 0.3048, "ft": 0.3048,
    "inches": 0.0254, "inch": 0.0254, "in": 0.0254,
    "nautical_miles": 1852, "nautical_mile": 1852, "nm": 1852,
}

WEIGHT = {
    "kg": 1, "kilograms": 1, "kilogram": 1,
    "g": 0.001, "grams": 0.001, "gram": 0.001,
    "mg": 0.000001, "milligrams": 0.000001, "milligram": 0.000001,
    "t": 1000, "tonnes": 1000, "tonne": 1000, "metric_tons": 1000,
    "lbs": 0.453592, "lb": 0.453592, "pounds": 0.453592, "pound": 0.453592,
    "oz": 0.0283495, "ounces": 0.0283495, "ounce": 0.0283495,
    "stone": 6.35029, "stones": 6.35029, "st": 6.35029,
    "short_tons": 907.185, "short_ton": 907.185,
}

VOLUME = {
    "l": 1, "liters": 1, "liter": 1, "litres": 1, "litre": 1,
    "ml": 0.001, "milliliters": 0.001, "milliliter": 0.001,
    "cl": 0.01, "centiliters": 0.01,
    "m3": 1000, "cubic_meters": 1000,
    "cm3": 0.001, "cubic_centimeters": 0.001,
    "gallons": 3.78541, "gallon": 3.78541, "gal": 3.78541,
    "quarts": 0.946353, "quart": 0.946353, "qt": 0.946353,
    "pints": 0.473176, "pint": 0.473176, "pt": 0.473176,
    "cups": 0.236588, "cup": 0.236588,
    "fl_oz": 0.0295735, "fluid_ounces": 0.0295735, "fluid_ounce": 0.0295735,
    "tbsp": 0.0147868, "tablespoons": 0.0147868, "tablespoon": 0.0147868,
    "tsp": 0.00492892, "teaspoons": 0.00492892, "teaspoon": 0.00492892,
    "imperial_gallons": 4.54609, "imperial_gallon": 4.54609,
}

AREA = {
    "m2": 1, "square_meters": 1, "square_meter": 1,
    "km2": 1_000_000, "square_kilometers": 1_000_000,
    "cm2": 0.0001, "square_centimeters": 0.0001,
    "ha": 10000, "hectares": 10000, "hectare": 10000,
    "ft2": 0.092903, "square_feet": 0.092903, "square_foot": 0.092903,
    "in2": 0.00064516, "square_inches": 0.00064516,
    "yd2": 0.836127, "square_yards": 0.836127,
    "acres": 4046.86, "acre": 4046.86,
    "mi2": 2_589_988, "square_miles": 2_589_988,
}

SPEED = {
    "m/s": 1, "meters_per_second": 1,
    "km/h": 1 / 3.6, "kmh": 1 / 3.6, "kph": 1 / 3.6, "kilometers_per_hour": 1 / 3.6,
    "mph": 0.44704, "miles_per_hour": 0.44704,
    "knots": 0.514444, "knot": 0.514444, "kt": 0.514444,
    "ft/s": 0.3048, "feet_per_second": 0.3048,
}

TIME = {
    "s": 1, "seconds": 1, "second": 1, "sec": 1,
    "ms": 0.001, "milliseconds": 0.001, "millisecond": 0.001,
    "min": 60, "minutes": 60, "minute": 60,
    "h": 3600, "hours": 3600, "hour": 3600, "hr": 3600,
    "days": 86400, "day": 86400, "d": 86400,
    "weeks": 604800, "week": 604800, "w": 604800,
    "months": 2_629_746, "month": 2_629_746,
    "years": 31_556_952, "year": 31_556_952, "yr": 31_556_952,
}

DATA = {
    "b": 1, "bytes": 1, "byte": 1,
    "kb": 1024, "kilobytes": 1024, "kilobyte": 1024,
    "mb": 1024 ** 2, "megabytes": 1024 ** 2, "megabyte": 1024 ** 2,
    "gb": 1024 ** 3, "gigabytes": 1024 ** 3, "gigabyte": 1024 ** 3,
    "tb": 1024 ** 4, "terabytes": 1024 ** 4, "terabyte": 1024 ** 4,
    "pb": 1024 ** 5, "petabytes": 1024 ** 5, "petabyte": 1024 ** 5,
    "bits": 0.125, "bit": 0.125,
    "kbits": 125, "kilobits": 125, "kilobit": 125,
    "mbits": 125_000, "megabits": 125_000,
    "gbits": 125_000_000, "gigabits": 125_000_000,
}

PRESSURE = {
    "pa": 1, "pascal": 1, "pascals": 1,
    "kpa": 1000, "kilopascal": 1000, "kilopascals": 1000,
    "mpa": 1_000_000, "megapascal": 1_000_000,
    "bar": 100_000, "bars": 100_000,
    "mbar": 100, "millibar": 100, "millibars": 100,
    "atm": 101_325, "atmospheres": 101_325, "atmosphere": 101_325,
    "psi": 6894.76, "pounds_per_square_inch": 6894.76,
    "mmhg": 133.322, "torr": 133.322,
    "inhg": 3386.39, "inches_of_mercury": 3386.39,
}

ENERGY = {
    "j": 1, "joules": 1, "joule": 1,
    "kj": 1000, "kilojoules": 1000, "kilojoule": 1000,
    "cal": 4.184, "calories": 4.184, "calorie": 4.184,
    "kcal": 4184, "kilocalories": 4184, "kilocalorie": 4184,
    "wh": 3600, "watt_hours": 3600, "watt_hour": 3600,
    "kwh": 3_600_000, "kilowatt_hours": 3_600_000, "kilowatt_hour": 3_600_000,
    "btu": 1055.06, "btus": 1055.06,
    "ev": 1.60218e-19, "electronvolts": 1.60218e-19, "electronvolt": 1.60218e-19,
}

TEMPERATURE_UNITS = {
    "celsius", "c", "fahrenheit", "f", "kelvin", "k",
    "rankine", "r", "delisle", "de", "newton", "n",
    "reaumur", "re", "romer", "ro"
}

CATEGORY_MAP = [
    ("length", LENGTH),
    ("weight", WEIGHT),
    ("volume", VOLUME),
    ("area", AREA),
    ("speed", SPEED),
    ("time", TIME),
    ("data", DATA),
    ("pressure", PRESSURE),
    ("energy", ENERGY),
]


def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    fu, tu = from_unit.lower(), to_unit.lower()

    if fu in ("celsius", "c"):       c = value
    elif fu in ("fahrenheit", "f"):  c = (value - 32) * 5 / 9
    elif fu in ("kelvin", "k"):      c = value - 273.15
    elif fu in ("rankine", "r"):     c = (value - 491.67) * 5 / 9
    elif fu in ("delisle", "de"):    c = 100 - value * 2 / 3
    elif fu in ("newton", "n"):      c = value * 100 / 33
    elif fu in ("reaumur", "re"):    c = value * 5 / 4
    elif fu in ("romer", "ro"):      c = (value - 7.5) * 40 / 21
    else: raise ValueError(f"Unknown temperature unit: '{from_unit}'")

    if tu in ("celsius", "c"):       return c
    elif tu in ("fahrenheit", "f"):  return c * 9 / 5 + 32
    elif tu in ("kelvin", "k"):      return c + 273.15
    elif tu in ("rankine", "r"):     return (c + 273.15) * 9 / 5
    elif tu in ("delisle", "de"):    return (100 - c) * 3 / 2
    elif tu in ("newton", "n"):      return c * 33 / 100
    elif tu in ("reaumur", "re"):    return c * 4 / 5
    elif tu in ("romer", "ro"):      return c * 21 / 40 + 7.5
    else: raise ValueError(f"Unknown temperature unit: '{to_unit}'")


def find_category(unit: str):
    u = unit.lower()
    for cat_name, table in CATEGORY_MAP:
        if u in table:
            return cat_name, table
    return None


def convert_units(value: float, from_unit: str, to_unit: str):
    fu, tu = from_unit.lower(), to_unit.lower()

    if fu in TEMPERATURE_UNITS or tu in TEMPERATURE_UNITS:
        return convert_temperature(value, fu, tu), "temperature"

    from_cat = find_category(fu)
    to_cat   = find_category(tu)

    if from_cat is None:
        raise ValueError(f"Unknown unit: '{from_unit}'")
    if to_cat is None:
        raise ValueError(f"Unknown unit: '{to_unit}'")
    if from_cat[0] != to_cat[0]:
        raise ValueError(
            f"Cannot convert between '{from_unit}' ({from_cat[0]}) "
            f"and '{to_unit}' ({to_cat[0]})"
        )

    _, table = from_cat
    result = (value * table[fu]) / table[tu]
    return result, from_cat[0]


def fmt(value: float) -> str:
    if value == 0:
        return "0"
    abs_v = abs(value)
    if abs_v >= 1e15 or (abs_v < 1e-6 and abs_v > 0):
        return f"{value:.6e}"
    if abs_v >= 1000:
        return f"{value:,.6g}"
    return f"{value:.10g}"
