import random as r
import generation as g
import character 
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

    def __init__(self, clauses, operators, action):
        self.clause_list = clauses
        self.operators = operators
        self.action = action
        self.match = False

    def matches(character):
        for clause in clause_list:
            for operator in operators:
                log.info("clause.matches(character) operator self.match")

    def do_action(character):
        log.info('Doing action')
        character.do_action(self.action)

class Clause:
    def __init__(self, identifier, values, clause_type):
        self.type_list = ['eq', 'ne', 'btw', 'gt', 'lt']
        self.type_calls = {
            'eq' : self.eq, 
            'ne' : self.ne, 
            'btw' : self.btw, 
            'gt' : self.gt, 
            'lt' : self.lt
        }
        self.id = identifier
        self.values = values
        self.type = clause_type

    def matches(self, other):
        print self.type_list[self.type_list.index(self.type)]
        return self.type_calls[self.type](other)

    def eq(self, other):
        #Value of other.id == self.values[0]
        return getattr(other, self.id) == self.values[0]

    def ne(self, other):
        return getattr(other, self.id) is not self.values[0]

    def btw(self, other):
        #Value of other.id = x is self.values[0] > x > self.values[1]
        #Assert two values
        #Assert val of 0 < 1
        if len(self.values<2):
            return False
        return self.values[0] <= getattr(other, self.id) <= self.values[1]

    def gt(self, other):
        #other.value > self.value
        return getattr(other, self.id) > self.values[0]

    def lt(self, other):
        #other.value < self.value
        return getattr(other, self.id) < self.values[0]

clause1 = Clause('age', [15], 'gt')
clause2 = Clause('profession', ['police'], 'eq')
rule1 = Rule([clause1, clause2], ['and'], 'nothing')

c = character.Character()
print clause1.matches(c)
print clause2.matches(c)

