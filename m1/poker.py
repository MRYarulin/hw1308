#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -----------------
# Реализуйте функцию best_hand, которая принимает на вход
# покерную "руку" (hand) из 7ми карт и возвращает лучшую
# (относительно значения, возвращаемого hand_rank)
# "руку" из 5ти карт. У каждой карты есть масть(suit) и
# ранг(rank)
# Масти: трефы(clubs, C), пики(spades, S), червы(hearts, H), бубны(diamonds, D)
# Ранги: 2, 3, 4, 5, 6, 7, 8, 9, 10 (ten, T), валет (jack, J), дама (queen, Q), король (king, K), туз (ace, A)
# Например: AS - туз пик (ace of spades), TH - дестяка черв (ten of hearts), 3C - тройка треф (three of clubs)

# Задание со *
# Реализуйте функцию best_wild_hand, которая принимает на вход
# покерную "руку" (hand) из 7ми карт и возвращает лучшую
# (относительно значения, возвращаемого hand_rank)
# "руку" из 5ти карт. Кроме прочего в данном варианте "рука"
# может включать джокера. Джокеры могут заменить карту любой
# масти и ранга того же цвета, в колоде два джокерва.
# Черный джокер '?B' может быть использован в качестве треф
# или пик любого ранга, красный джокер '?R' - в качестве черв и бубен
# любого ранга.

# Одна функция уже реализована, сигнатуры и описания других даны.
# Вам наверняка пригодится itertoolsю
# Можно свободно определять свои функции и т.п.
# -----------------
from itertools import product, combinations


def check_hand(func):
    """
    проверка входных данных
    :type func: функции-потребители входных данных
    """

    def wrapper(hand, *args):
        check = all({len(c) == 2 for c in hand})
        if not check:
            raise ValueError("Do not cardsharp!\n", hand)
        else:
            return func(hand, *args)

    return wrapper


@check_hand
def hand_rank(hand):
    """Возвращает значение определяющее ранг 'руки'"""
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):
        return (8, max(ranks))
    elif kind(4, ranks):
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):
        return (5, ranks)
    elif straight(ranks):
        return (4, max(ranks))
    elif kind(3, ranks):
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):
        return (1, kind(2, ranks), ranks)
    else:
        return (0, ranks)


@check_hand
def card_ranks(hand):
    """Возвращает список рангов (его числовой эквивалент),
    отсортированный от большего к меньшему"""
    position = '0023456789TJQKA'
    res = [position.index(rank) for rank, suit in hand if rank in position]
    res.sort(reverse=True)
    return res


@check_hand
def flush(hand):
    """Возвращает True, если все карты одной масти"""
    return len(set([suit for rank, suit in hand])) == 1


def straight(ranks):
    """Возвращает True, если отсортированные ранги формируют последовательность 5ти,
    где у 5ти карт ранги идут по порядку (стрит)"""
    # ranks.sort(reverse = True)
    return len(set(ranks)) == 5 and (ranks[0] - ranks[-1] == 4)


def kind(n, ranks):
    """Возвращает первый ранг, который n раз встречается в данной руке.
    Возвращает None, если ничего не найдено"""
    res = [r for r in ranks if ranks.count(r) == n]
    return len(res) and res[0] or None


def two_pair(ranks):
    """Если есть две пары, то возврщает два соответствующих ранга,
    иначе возвращает None"""
    res = list({r for r in ranks if ranks.count(r) == 2})
    return len(res) >= 2 and res[:2] or None


@check_hand
def best_hand(hand, size=5):
    """Из "руки" в 7 карт возвращает лучшую "руку" в 5 карт """
    res = max(combinations(hand, size), key=hand_rank)
    return list(res)


@check_hand
def best_wild_hand(hand):
    """best_hand но с джокерами"""
    jocker = {'?B': ["C", "S"],
              '?R': ["H", "D"]}
    ranks = list('23456789TJQKA')
    jockers = {c for c in hand if '?' in c}
    hand_clear = set(hand) - jockers
    best = best_hand(hand_clear, 5 - len(jockers))
    '''
    Гипотеза: "лучшая по ранку перестановка 4изN плюс джокер сильнее остальных четвёрок + джокер" не верна, 
    т.к. её следствие о двух джокерах не выдерживает тестового испытания. 
    
    for j in jockers:
        options = [best + [''.join(c)] for c in itertools.product(ranks, jocker.get(j, []))]
        best = max(options, key=hand_rank)
        print "best", best
    return best
    
    >>> hand    [‘TD’, ‘TC’, ‘5H’, ‘5C’, ‘7C’, ‘?R’, ‘?B’]
    >>> best    [‘7C’, ‘5C’, ‘TC’]
    >>> best [‘7C’, ‘5C’, ‘TC’, ‘TH’]
    >>> best [‘7C’, ‘5C’, ‘TC’, ‘TH’, ‘TC’]
    '''

    options = []
    if len(jockers) > 1:
        '''
        по итогам тестирования, пришел к заключению, что джокер не дублирует карты в руке...
        иначе ответ был бы 7C TD TC TC TH  
        '''
        o1 = {''.join(c) for c in product(ranks, jocker.get('?B'))} - hand_clear
        o2 = {''.join(c) for c in product(ranks, jocker.get('?R'))} - hand_clear
        options = [best_hand(sum(i, [])) for i in product([list(hand_clear)], map(list, product(o1, o2)))]
    elif len(jockers) == 1:
        options = [best + [''.join(c)] for c in product(ranks, jocker.get(jockers.pop(), []))]
    if options:
        best = max(options, key=hand_rank)
    return best


def test_best_hand():
    print "test_best_hand..."
    assert (sorted(best_hand("6C 7C 8C 9C TC 5C JS".split()))
            == ['6C', '7C', '8C', '9C', 'TC'])
    assert (sorted(best_hand("TD TC TH 7C 7D 8C 8S".split()))
            == ['8C', '8S', 'TC', 'TD', 'TH'])
    assert (sorted(best_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    print 'OK'


def test_best_wild_hand():
    print "test_best_wild_hand..."
    assert (sorted(best_wild_hand("6C 7C 8C 9C TC 5C ?B".split()))
            == ['7C', '8C', '9C', 'JC', 'TC'])
    assert (sorted(best_wild_hand("TD TC 5H 5C 7C ?R ?B".split()))
            == ['7C', 'TC', 'TD', 'TH', 'TS'])
    assert (sorted(best_wild_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    print 'OK'


def test_card_ranks():
    print "test_card_ranks..."
    assert card_ranks("6C 7C 8C 9C TC 5C JS".split()) == [11, 10, 9, 8, 7, 6, 5]
    assert card_ranks("qw er ty".split()) == []
    assert card_ranks("1? 2? 3? 4? 5? 6? 7? 8? 9? T? J? Q? K? A?".split()) \
           == [14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2]


if __name__ == '__main__':
    test_card_ranks()
    test_best_hand()
    test_best_wild_hand()
