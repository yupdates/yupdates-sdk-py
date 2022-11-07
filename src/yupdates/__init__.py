def normalize_item_time(item_time):
    """Accept many forms of item time, validate it, and return a normalized version

    Parameters
    ----------
    item_time : str or int
        An item time is a unix ms from 0 to 9_999_999_999_999. It has an optional 5 digit suffix.
        Valid inputs: 1234, 1661564013555, "1661564013555", "1661564013555.00003"

    Returns
    -------
    item_time: str

    Raises
    ------
    ValueError
        If the input is invalid, e.g. out of range
    """
    item_time_str = str(item_time)
    if '.' in item_time_str:
        parts = item_time_str.split(".")
        base = int(parts[0])
        slot = int(parts[1])
    else:
        base = int(item_time)
        slot = 0
    if not 0 <= base <= 9999999999999:
        raise ValueError("item_time timestamp is out of range")
    if not 0 <= slot <= 99999:
        raise ValueError("item_time suffix is out of range")
    return "%s.%s" % (str(base).zfill(13), str(slot).zfill(5))
