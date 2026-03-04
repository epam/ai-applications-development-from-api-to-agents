# Unit Converter — Examples

## Invocation examples

| User says                     | value  | from_unit    | to_unit   |
|-------------------------------|--------|--------------|-----------|
| "Convert 100 km to miles"     | `100`  | `km`         | `miles`   |
| "98.6°F in Celsius"           | `98.6` | `fahrenheit` | `celsius` |
| "5 kg to pounds"              | `5`    | `kg`         | `lbs`     |
| "How many MB is 1.5 TB?"      | `1.5`  | `tb`         | `mb`      |
| "60 mph in km/h"              | `60`   | `mph`        | `km/h`    |
| "3 cups of milk in ml"        | `3`    | `cups`       | `ml`      |
| "5 acres to hectares"         | `5`    | `acres`      | `ha`      |
| "Convert 0 Kelvin to Celsius" | `0`    | `kelvin`     | `celsius` |
| "1 atm in psi"                | `1`    | `atm`        | `psi`     |
| "How many seconds in a year?" | `1`    | `years`      | `seconds` |

## Expected output format

```
Category: length
Input:    100 km
Result:   62.1371 miles
```

## Supported units by category

**length** — km, m, cm, mm, miles, yards, feet, inches, nautical_miles

**weight** — kg, g, mg, tonnes, lbs, oz, stone, short_tons

**temperature** — celsius, fahrenheit, kelvin, rankine, delisle, newton, reaumur, romer

**volume** — l, ml, cl, m3, gallons, quarts, pints, cups, fl_oz, tbsp, tsp, imperial_gallons

**area** — m2, km2, cm2, ha, ft2, in2, yd2, acres, mi2

**speed** — m/s, km/h, mph, knots, ft/s

**time** — ms, s, min, h, days, weeks, months, years

**data** — bits, bytes, kb, mb, gb, tb, pb, kilobits, megabits, gigabits

**pressure** — pa, kpa, bar, mbar, atm, psi, mmhg, torr, inhg

**energy** — j, kj, cal, kcal, wh, kwh, btu, ev

## Error examples

```
# Incompatible categories
Error: Cannot convert between 'kg' (weight) and 'meters' (length)

# Unknown unit
Error: Unknown unit: 'stone_cold'
```