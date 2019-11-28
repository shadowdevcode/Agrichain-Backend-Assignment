# coding: utf-8

import unittest
from checkout import Checkout, PriceRules


__all__ = ['CheckoutTest', 'PriceRulesTest']


class CheckoutTest(unittest.TestCase):
    def setUp(self):
        self.co = Checkout()

    def test_no_item_returns_zero(self):
        self.co.scan('')
        self.assertEqual(0, self.co.price)

    def test_can_check_one_item(self):
        self.co.scan('A')
        self.assertEqual(50, self.co.price)

    def test_can_check_multiple_distinct_items(self):
        self.co.scan('A')
        self.co.scan('B')
        self.co.scan('C')
        self.co.scan('D')
        self.assertEqual(115, self.co.price)

    def test_can_deal_with_combo(self):
        self.co.scan('A')
        self.co.scan('A')
        self.co.scan('A')
        self.assertEqual(130, self.co.price)

    def test_can_deal_with_multiple_combos(self):
        self.co.scan('AAAA')
        self.assertEqual(180, self.co.price)

        self.co.scan('AAAAA')
        self.assertEqual(230, self.co.price)

        self.co.scan('AAAAAA')
        self.assertEqual(260, self.co.price)

    def test_can_deal_with_combos_from_distinct_products(self):
        self.co.scan('AAAB')
        self.assertEqual(160, self.co.price)

        self.co.scan('AAABBC')
        self.assertEqual(195, self.co.price)

    def test_can_deal_with_unsorted_items(self):
        self.co.scan('BABAAC')
        self.assertEqual(195, self.co.price)


class PriceRulesTest(unittest.TestCase):
    def setUp(self):
        self.pr = PriceRules()

    def test_can_add_rule(self):
        self.pr.add_rule('A', 10)
        self.assertEqual({1: {'A': 10}}, self.pr.rules)

        self.pr.add_rule('A', 25, 3)
        self.assertEqual({1: {'A': 10}, 3: {'A': 25}}, self.pr.rules)

    def test_raise_error_if_rule_item_has_more_than_one_character(self):
        self.assertRaises(ValueError, self.pr.add_rule, 'AA', 10)

    def test_not_raise_error_if_rule_item_is_unicode(self):
        self.pr.add_rule(u'☢', 10)
