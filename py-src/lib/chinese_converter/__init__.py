import json
import os
from collections import Counter, defaultdict, deque
from operator import itemgetter
from typing import Any, Deque, Dict, List, Optional, Tuple

__all__ = ['to_simplified', 'to_traditional']

BASE_PATH = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(BASE_PATH, 'traditional.txt')) as f, open(os.path.join(BASE_PATH, 'simplified.txt')) as g:
    traditional, simplified = f.read().strip(), g.read().strip()

with open(os.path.join(BASE_PATH, 'bigram.json')) as f, open(os.path.join(BASE_PATH, 'monogram.json')) as g:
    bigrams, monograms = Counter(json.load(f)), Counter(json.load(g))

simp_to_trad: Dict[str, List[str]] = defaultdict(list)
trad_to_simp = str.maketrans(traditional, simplified)

for s, t in zip(simplified, traditional):
    simp_to_trad[s].append(t)

simp_to_trad = dict(simp_to_trad)


def default_getter(l, i, default: Optional[Any] = None):
    try:
        return l[i]
    except IndexError:
        return default


def most_common_word(choices: List[str], prev_word: Optional[str] = None, next_word: Optional[str] = None) -> str:
    bigram_freqs: Deque[Tuple[str, int]] = deque()

    if prev_word is not None:
        bigram_freqs.extend((c, bigrams[prev_word + c]) for c in choices)

    if next_word is not None:
        bigram_freqs.extend((c, bigrams[c + next_word]) for c in choices)

    try:
        choices_max = max(bigram_freqs, key=itemgetter(1))

        if not choices_max[1]:
            return max(choices, key=lambda c: monograms[c])

        return choices_max[0]
    except ValueError:
        return choices[0]


def to_traditional(text: str) -> str:
    """
    Translates text to traditional chinese

    :param text:
    :return:
    """
    result: Deque[str] = deque()

    for i, s in enumerate(text):
        try:
            choices = simp_to_trad[s]

            if len(choices) > 1:
                result.append(most_common_word(choices, default_getter(result, -1), default_getter(text, i + 1)))
            else:
                result.append(choices[0])
        except KeyError:
            result.append(s)

    return ''.join(result)


def to_simplified(text: str) -> str:
    """
    Translates text to simplified chinese

    :param text:
    :return:
    """
    return text.translate(trad_to_simp)
