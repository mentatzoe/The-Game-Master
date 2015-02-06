import random as r
import generation as g
import logging
import operator
import math 
import sys

log = logging.getLogger(__name__)

'''
Rule
Has clause that can be a... List of... Dictionaries?
And a ... Like... Operator?
match = False
For clause in rule:
    For operator in rule.operators:
        match  and o(clause.matches(character))
'''
class Rule:
    self.clause = ''
    def action(bindings):
        pass

    def andClauses(self):

class Clause:
    self.typeList = ['eq', 'ne', 'btw', 'gt', 'lt']
    #I think I'll have to add getters and setters in order to take full advantage of this
    self.id = ''
    self.values = []
    def matches(self, other):
        self.typeList[self.type](self, other)

    def eq(self, other):
        #Value of other.id == self.values[0]
        pass

    def ne(self, other):
        #Value of other.id != self.values[0]
        pass

    def btw(self, other):
        #Value of other.id = x is self.values[0] > x > self.values[1]
        #Assert two values
        #Assert val of 0 < 1
        pass

    def gt(self, other):
        #other.value > self.value
        pass

    def lt(self, other):
        #other.value < self.value
        pass


