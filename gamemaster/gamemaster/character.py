import random as r
import generation as g
import logging
import operator
import math 

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

    def fillSocialVector(self, characters):
        #Filling social vector according to who other characters are
        log.info("Filling social Vector")

    def set_location(self, location):
        self.location = location