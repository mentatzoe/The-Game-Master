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

    def matches(self, character):
        match = self.clause_list[0].matches(character)
        for clause in self.clause_list:
            match = match and clause.matches(character)
        return match

    def do_action(character):
        log.info('Doing action')
        character.do_action(self.action)

class Clause:
    def __init__(self, identifier, values, clause_type):
        self.type_calls = {
            'eq' : self.eq, 
            'ne' : self.ne, 
            'btw' : self.btw, 
            'gt' : self.gt, 
            'lt' : self.lt,
            'is' : self.is_attr,
            'is_not' : self.is_not
        }
        self.id = identifier
        self.values = values
        self.type = clause_type

    def matches(self, other):
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

    def is_attr(self, other):
        return getattr(other, self.id)()

    def is_not(self, other):
        return not getattr(other, self.id)()

    def __str__(self):
        return str(self.__dict__)

''' 
Creating set of rules and storing them somewhere
social - mood ok - friend in location - loving -> love (check if other character loves, calculate outcome)
social - mood ok - friend in location - not loving -> play game from location
social - mood ok - not friend in location - can change location -> travel (update resources)
social - mood ok - not friend in location - not can change location - needs resources - can work -> work
social - mood ok - not friend in location - not can change location - needs resources - not can work -> travel work location (free because it's for work so the company pays for it (?))
social - mood ok - not friend in location - not can change location - not needs resources (meaning the place is full) - is greedy - can work -> work
social - mood ok - not friend in location - not can change location - not needs resources (meaning the place is full) - is greedy - not can work -> play
social - mood ok - not friend in location - not can change location - not needs resources (meaning the place is full) - not is greedy -> play
social - mood not ok - enemy in location - greedy - violent -> fight/maybe kill (and steal all their resources - it would be nice if everybody else changed their opinion)
social - mood not ok - enemy in location - greedy - not violent -> steal 
social - mood not ok - enemy in location - not greedy - not violent -> argue 
social - mood not ok - enemy not in location - can change location -> travel (update resources)

'''
def render_rules():

