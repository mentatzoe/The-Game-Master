import random as r
import generation as g
import logging
import operator
import math 
import sys

log = logging.getLogger(__name__)

class Character:
    def __init__(self):
        self.age = r.randint(18, 35)
        self.gender = g.gender[r.randint(0,1)]
        self.name = g.first_names[self.gender][r.randint(0, len(g.first_names[self.gender])-1)] + " " + g.last_names[r.randint(0, len(g.last_names)-1)]
        self.attributes = {
            'str' : r.randint(3, 18),
            'con' : r.randint(3, 18),
            'dex' : r.randint(3, 18),
            'int' : r.randint(3, 18),
            'cha' : r.randint(3, 18)
        }
        self.personality = {
            'greedy' : int(r.random() * 100),
            'violent' : int(r.random() * 100),
            'romantic' : int(r.random() * 100),
        }
        possible_professions = g.professions[max(self.attributes.iteritems(), key=operator.itemgetter(1))[0]]
        self.profession = possible_professions[r.randint(0, len(possible_professions)-1)]
        self.resources = int(math.floor(g.profession_pays[self.profession] * (r.randint(18, self.age) * 12 * self.attributes['int'] * r.random())))
        self.health = int(((250-self.age) * self.attributes['con'] * r.random())%100)
        if self.health < 50:
            self.health += 25
        self.happiness = int(r.random() * 100)
        self.social_need = int((self.attributes['cha'] * r.random() * 100)%100)
        self.social_vector = []
        self.location = None
        self.married = None

    def __str__(self):
        return str(self.__dict__)
        #KISS
        # return """ 
        # Character Name: %s,
        # Age: %d,
        # Gender: %s,
        # Attributes:
        # STR %d 
        # CON %d
        # DEX %d
        # INT %d
        # CHA %d,
        # Profession: %s
        # Resources: %d 
        # Health: %d 
        # Starting happiness: %d
        # Starting social need: %d
        # """%(self.name, self.age, self.gender, self.attributes['str'], 
        #     self.attributes['con'], self.attributes['dex'], self.attributes['int'], 
        #     self.attributes['cha'], self.profession, self.resources,
        #     self.health, self.happiness, self.social_need)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def fill_social_vector(self, characters):
        #Filling social vector according to who other characters are
        #"Affinity" is decreasing, as we want to use a value that reflects how alike characters are
        log.info("Filling social Vector")
        self.social_vector = [self.calculate_affinity(char) for char in characters]
        
    def calculate_affinity(self, character):
        affinity = 0
        if self == character:
            return 'x'
        if self.location is not character.location:
            affinity = sys.maxint
        else:
            for attr in self.attributes:
                affinity += abs(self.attributes[attr] - character.attributes[attr])
            for trait in self.personality:
                affinity += abs(self.personality[trait] - character.personality[trait])
            if not self.profession == character.profession:
                affinity += 100
            affinity += abs(self.age - character.age)
            affinity += int(r.random() * 10) * r.choice([-1, 1])
            if self.is_greedy():
                if character.resources > self.resources:
                    affinity -= int(r.random() * 10)
        return affinity


    def set_location(self, location):
        self.location = location

    def is_greedy(self):
        return self.personality['greedy'] > 50
    def is_romantic(self):
        return self.personality['romantic'] > 50
    def is_violent(self):
        return self.personality['violent'] > 50

    def do_action(self, action, **kwargs):
        if action not in self.actions:
            return None
        self.actions[action]()

    def get_attribute(self, attr):
        return self.attr

