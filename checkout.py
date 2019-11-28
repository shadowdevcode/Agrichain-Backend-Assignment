# coding: utf-8

from collections import OrderedDict


class PriceRules(object):

    def __init__(self):
        self._rules = {}

    def add_rule(self, item, price, quantity=1):
        if len(item) > 1:
            raise ValueError('Item name must have 1 character only')

        if quantity not in self._rules:
            self._rules[quantity] = {}

        self._rules[quantity][item] = price

    @property
    def rules(self):
        return OrderedDict(reversed(sorted(self._rules.items())))


price_rules = PriceRules()
price_rules.add_rule('A', 50)
price_rules.add_rule('B', 30)
price_rules.add_rule('C', 20)
price_rules.add_rule('D', 15)
price_rules.add_rule('B', 45, 2)
price_rules.add_rule('A', 130, 3)


class Checkout(object):
    items = ''

    def scan(self, item):
        self.items += item

    @property
    def price(self):
        self.items = ''.join(sorted(self.items))
        return self._compute_price(price_rules.rules)

    def _compute_price(self, rules):
        price = 0

        for quantity, items in rules.iteritems():
            for item, item_price in items.iteritems():
                item_pattern = item * quantity
                if item_pattern in self.items:
                    price += item_price * self.items.count(item_pattern)
                    self.items = self.items.replace(item_pattern, '')

        return price
