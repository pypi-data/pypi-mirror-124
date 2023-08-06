from functools import lru_cache, singledispatch
from typing import List, Tuple


@singledispatch
def search(pattern: str, source: str):
    return {criteria: search(criteria, source) for criteria in pattern}


@search.register(str)
def _(pattern: str, source: str) -> List[Tuple[int, int]]:
    good_suffix = suffix_shift(pattern)
    bad_char = bad_char_shift(pattern)
    r = []
    i = 0
    pattern_size = len(pattern)
    # while i < len(source) - len(pattern) + 1:
    while i < len(source) - pattern_size + 1:
        # j = len(pattern)
        j = pattern_size
        while j > 0 and pattern[j - 1] == source[i + j - 1]:
            j -= 1
        if j > 0:
            bad_charShift = bad_char.get(source[i + j - 1], len(pattern))
            good_suffixShift = good_suffix[len(pattern) - j]
            if bad_charShift > good_suffixShift:
                i += bad_charShift
            else:
                i += good_suffixShift
        else:
            r.append((i, i + len(pattern)))
            i = i + 1
    return r


@lru_cache(maxsize=5)
def bad_char_shift(pattern):
    pattern_len = len(pattern)
    return {pattern[i]: (pattern_len - (i + 1)) for i in range(0, pattern_len - 1)}


@lru_cache(maxsize=5)
def suffix_shift(pattern):
    pattern_len = len(pattern)
    skip_list = {}
    _buffer = ""
    for i in range(0, pattern_len):
        skip_list[len(_buffer)] = suffix_position(
            pattern[pattern_len - 1 - i], _buffer, pattern
        )
        _buffer = f"{pattern[pattern_len - 1 - i]}{_buffer}"
    return skip_list


def suffix_position(badchar: str, suffix: str, full_term):
    for offset in range(1, len(full_term) + 1)[::-1]:
        flag = True
        for suffix_index in range(0, len(suffix)):
            term_index = offset - len(suffix) - 1 + suffix_index
            if term_index > 0 or suffix[suffix_index] != full_term[term_index]:
                flag = False
        term_index = offset - len(suffix) - 1
        if flag and (term_index <= 0 or full_term[term_index - 1] != badchar):
            return len(full_term) - offset + 1
