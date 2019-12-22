# Source: https://gist.github.com/shello/efa2655e8a7bce52f273
# Please give him a star!

from itertools import accumulate
from bisect import bisect
from random import randrange

EMOJI_RANGES_UNICODE = [
    ('\U0001F300', '\U0001F320'),
    ('\U0001F330', '\U0001F335'),
    ('\U0001F337', '\U0001F37C'),
    ('\U0001F380', '\U0001F393'),
    ('\U0001F3A0', '\U0001F3C4'),
    ('\U0001F3C6', '\U0001F3CA'),
    ('\U0001F3E0', '\U0001F3F0'),
    ('\U0001F400', '\U0001F43E'),
    ('\U0001F440', '\U0001F4F7'),
    ('\U0001F4F9', '\U0001F4FC'),
    ('\U0001F500', '\U0001F53D'),
    ('\U0001F550', '\U0001F567'),
    ('\U0001F5FB', '\U0001F5FF')
]


def random_emoji():
    # Weighted distribution
    count = [ord(r[-1]) - ord(r[0]) + 1 for r in EMOJI_RANGES_UNICODE]
    weight_distr = list(accumulate(count))

    # Get one point in the multiple ranges
    point = randrange(weight_distr[-1])

    # Select the correct range
    emoji_range_idx = bisect(weight_distr, point)
    emoji_range = EMOJI_RANGES_UNICODE[emoji_range_idx]

    # Calculate the index in the selected range
    point_in_range = point
    if emoji_range_idx is not 0:
        point_in_range = point - weight_distr[emoji_range_idx - 1]

    # Emoji 😄
    emoji = chr(ord(emoji_range[0]) + point_in_range)

    return emoji
