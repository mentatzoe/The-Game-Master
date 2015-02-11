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
    def __init__(self, clauses, action):
        self.clause_list = clauses
        self.action = action

    def __str__(self):
        string = [clause.id for clause in self.clause_list]
        return str(self.__dict__) + str(string)

    def matches(self, character):
        match = self.clause_list[0].matches(character)
        for clause in self.clause_list:
            match = match and clause.matches(character)
        return match

    def do_action(self, character, character_list):
        return character.do_action(self.action, character_list)

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
no health -> die 
sick - doctor available - has resources -> cure
sick - doctor available - not has resources - can work -> work
sick - doctor available - not has resources - not can work -> travel free
sick - no doctor available - can change location -> travel
sick - no doctor available - not can change location - can work -> work
sick - no doctor available - not can change location - not can work -> travel free
not sick - social - mood ok - friend in location - loving -> love (check if other character loves, calculate outcome)
not sick - social - mood ok - friend in location - not loving -> play game from location
not sick - social - mood ok - not friend in location - can change location -> travel (update resources)
not sick - social - mood ok - not friend in location - not can change location - needs resources - can work -> work
not sick - social - mood ok - not friend in location - not can change location - needs resources - not can work -> travel work location (free because it's for work so the company pays for it (?))
# not sick - social - mood ok - not friend in location - not can change location - not needs resources (meaning the place is full) - is greedy - can work -> work
# not sick - social - mood ok - not friend in location - not can change location - not needs resources (meaning the place is full) - is greedy - not can work -> play
# not sick - social - mood ok - not friend in location - not can change location - not needs resources (meaning the place is full) - not is greedy -> play
not sick - social - mood not ok - enemy in location - greedy - violent -> fight/maybe kill (and steal all their resources - it would be nice if everybody else changed their opinion)
not sick - social - mood not ok - enemy in location - greedy - not violent -> steal 
not sick - social - mood not ok - enemy in location - not greedy - not violent -> argue 
not sick - social - mood not ok - enemy not in location - can change location -> travel (update resources)
not sick - social - mood not ok - enemy not in location - not can change location - needs resources - can work -> work
not sick - social - mood not ok - enemy not in location - not can change location - needs resources - not can work -> travel work location (free because it's for work so the company pays for it (?))
# not sick - social - mood not ok - enemy not in location - not can change location - not needs resources (meaning the place is full) - is greedy - can work -> work
# not sick - social - mood not ok - enemy not in location - not can change location - not needs resources (meaning the place is full) - is greedy - not can work -> play
# not sick - social - mood not ok - enemy not in location - not can change location - not needs resources (meaning the place is full) - not is greedy -> play
not sick - not social - greedy - violent - not loving  -> steal 
not sick - not social - mood ok - greedy - not violent - not loving  -> work
not sick - not social - mood ok - not greedy - not violent - loving ->  play 
not sick - not social - not mood ok - not greedy - violent - loving -> argue with enemy of friend
not sick - not social - awful mood - not greedy - not violent - not loving -> suicide


'''
def render_rules():
    #identifier, values, clause_type)
# self.type_calls = {
#             'eq' : self.eq, 
#             'ne' : self.ne, 
#             'btw' : self.btw, 
#             'gt' : self.gt, 
#             'lt' : self.lt,
#             'is' : self.is_attr,
#             'is_not' : self.is_not
#         }
    no_health = Clause('health', [0], 'eq')
    sick = Clause('sick', [], 'is')
    not_sick = Clause('sick', [], 'is_not')
    doctor_available = Clause('doctor_available', [], 'is')
    not_doctor_available = Clause('doctor_available', [], 'is_not')
    social = Clause('social_need', [49], 'gt')
    not_social = Clause('social_need', [50], 'lt')
    has_resources = Clause('resources', [399], 'gt')
    not_has_resources = Clause('resources', [400], 'lt')
    mood_ok = Clause('happiness', [49], 'gt')
    not_mood_ok = Clause('happiness', [50], 'lt')
    can_work = Clause('can_work', [], 'is')
    not_can_work = Clause('can_work', [], 'is_not')
    friend_in_location = Clause('friend_in_location', [], 'is')
    not_friend_in_location = Clause('friend_in_location', [], 'is_not')
    enemy_in_location = Clause('enemy_in_location', [], 'is')
    not_enemy_in_location = Clause('enemy_in_location', [], 'is_not')
    can_change_location = Clause('resources', [1299], 'gt')
    not_can_change_location = Clause('resources', [1300], 'lt')
    greedy = Clause('is_greedy', [], 'is')
    not_greedy = Clause('is_greedy', [], 'is_not')
    loving = Clause('is_romantic', [], 'is')
    not_loving = Clause('is_romantic', [], 'is_not')
    violent = Clause('is_violent', [], 'is')
    not_violent = Clause('is_violent', [], 'is_not')
    awful_mood = Clause('happiness', [10], 'lt')

    r1 = Rule([no_health], 'die')
    r2 = Rule([sick, doctor_available, has_resources], 'cure')
    r3 = Rule([sick, doctor_available, not_has_resources, can_work],'work')
    r4 = Rule([sick, doctor_available, not_has_resources, not_can_work],'travel_free')
    r5 = Rule([sick, not_doctor_available, can_change_location],'travel')
    r6 = Rule([sick, not_doctor_available, not_can_change_location, can_work],'work')
    r7 = Rule([sick, not_doctor_available, not_can_change_location, not_can_work],'travel_free')
    r8 = Rule([not_sick, social, mood_ok, friend_in_location, loving],'love')
    r9 = Rule([not_sick, social, mood_ok, friend_in_location],'play')
    r10 = Rule([not_sick, social, mood_ok, not_friend_in_location, can_change_location],'travel_friend')
    r11 = Rule([not_sick, social, mood_ok, not_friend_in_location, not_can_change_location, can_work],'work')
    r12 = Rule([not_sick, social, mood_ok, not_friend_in_location, not_can_change_location, not_can_work],'travel_friend_free')
    r13 = Rule([not_sick, social, not_mood_ok, enemy_in_location, greedy, violent], 'fight')
    r14 = Rule([not_sick, social, not_mood_ok, enemy_in_location, greedy, not_violent],'steal')
    r15 = Rule([not_sick, social, not_mood_ok, enemy_in_location],'argue')
    r16 = Rule([not_sick, social, not_mood_ok, not_enemy_in_location, can_change_location],'travel_enemy')
    r17 = Rule([not_sick, social, not_mood_ok, not_enemy_in_location, not_can_change_location, can_work],'work')
    r18 = Rule([not_sick, social, not_mood_ok, not_enemy_in_location, not_can_change_location, not_can_work],'travel_enemy_free')
    
    r19 = Rule([not_sick, mood_ok, not_social, greedy, violent], 'play')
    r20 = Rule([not_sick, mood_ok, not_social, greedy, not_violent], 'work')

    r21 = Rule([not_sick, not_mood_ok, not_social, greedy, violent], 'steal')
    r22 = Rule([not_sick, not_mood_ok, not_social, greedy, not_violent], 'work')

    r23 = Rule([not_sick, awful_mood, not_greedy, not_violent, not_loving], 'suicide')

    r24 = Rule([not_sick, not_social], 'play_alone')

    

    rule_list = [r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, 
    r11, r12, r13, r14, r15, r16, r17, r18, r19, r20, r21, r22, r23, r24]

    return rule_list
    log.info("Aloha")
