from videdit.exceptions import InvalidIntervalFormat, InvalidTimeFormat


def time(timestring: str):
    number_of_figures = timestring.count(":") + 1
    if number_of_figures > 3:
        raise InvalidTimeFormat(timestring)

    figures = []
    for figure in (3-number_of_figures)*[0] + timestring.split(":"):
        x = int(figure)
        figures.append(str(x).zfill(2))
    return ":".join(figures)


def interval(intervalstring: str):
    if intervalstring.count("-") != 1:
        raise InvalidIntervalFormat(intervalstring)

    return tuple(time(timestring) for timestring in intervalstring.split('-'))
