furnace
=======

Furnace is the initial module of what will eventually become an entire technology foraging tool chain geared toward extracting some technology progress data from science news, en masse.

Furnace spec:
At the very least (this is an early spec), Furnace requires passing a sourcestring to be parsed into a result. This string can be comprised of any combination/formatting of units, although the more it follows a consistent, style manual pattern the easier it will be to parse.

Furnace will calculate the impact of leading integers and reals, prefixes, and exponentials (ie cm^3 has centi as a prefix, or .01, but also ^3 meaning that cm^3 = (.01^3)m^3 instead of .01m^3), and convert non-standardized output to standardized output.

Type of output will depend on specific dict chosen, with possible other formatting options (if you know the unit you are looking for, you can specify output format).

Output will, tentatively, take the form of a numeric scalar comprised of all leading integers and reals, prefixes, and exponentials handled in one number (so as to compare evenly between equivalent units) as well as a desired unit format (ie 1 Watt Hour is 3600 Joules)
