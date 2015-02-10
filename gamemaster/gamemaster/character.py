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
        self.sick_atr = False
        self.doctor_available_atr = False
        self.can_work_atr = True
        self.friend_in_location_atr = False
        self.enemy_in_location_atr = False

    def sick(self):
        return self.sick_atr
    def doctor_available(self):
        return self.doctor_available_atr
    def can_work(self):
        return self.can_work_atr
    def friend_in_location(self):
        return self.friend_in_location_atr
    def enemy_in_location(self):
        return self.enemy_in_location_atr
        
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
            affinity += int(3000 * r.random())
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

    def do_action(self, action, character_list, **kwargs):
        actions = {
            'work': self.work,
            'travel': self.travel,
            'travel_friend': self.travel,
            'travel_enemy': self.travel,
            'travel_free': self.travel,
            'travel_friend_free': self.travel,
            'travel_enemy_free': self.travel,
            'play': self.play,
            'love': self.love,
            'steal': self.steal,
            'fight': self.fight,
            'argue': self.argue,
            'die': self.die
        }

        if action not in actions:
            return "SOMETHING WENT WRONG WITH " + action

        kwargs = {}
        words = action.split('_')[0]

        if len(words) > 1 and words[0] == 'travel':
            if len(words) > 2 and action.split('_')[1] == 'friend':
                kwargs['friend'] = character_list[self.social_vector.index(min(self.social_vector))]
            if len(words) > 2 and action.split('_')[1] == 'enemy':
                kwargs['enemy'] = character_list[self.social_vector.index(max(self.social_vector))]
            if len(words) > 2 and action.split('_')[1] == 'free':
                kwargs['free'] = True
            if len(words) > 3 and words[2] == 'free':
                kwargs['free'] = True

        if action in ['steal', 'fight', 'argue', 'travel_enemy']:
            kwargs['enemy'] = character_list[self.social_vector.index(max(self.social_vector))]


        return actions[action](**kwargs)

    def get_attribute(self, attr):
        return self.attr

    def update_booleans(self, characters, other = None):
        if characters[self.social_vector.index(min(self.social_vector))].location == self.location:
            log.info("Friend is "+characters[self.social_vector.index(min(self.social_vector))].name)
            self.friend_in_location_atr = True
        if characters[self.social_vector.index(max(self.social_vector))].location == self.location:
            log.info("Enemy is "+characters[self.social_vector.index(max(self.social_vector))].name)
            self.enemy_in_location_atr = True
        if self.profession in self.location.actions['work']:
            self.can_work_atr = True
        characters_in_loc = [c for c in characters if c.location == self.location and c.profession == 'doctor']
        if len(characters_in_loc) > 0:
            self.doctor_available_atr = True

    def update_health(self):
        if self.sick:
            self.health -= 10
        else:
            self.health -= 2

    def update_happiness(self, factor):
        log.info("luck " + str(int(r.random() * max(self.attributes.iteritems(), key=operator.itemgetter(1))[1] * 100)%100))
        log.info("Happiness factor " + str(factor))
        if (factor * 100)%100 > 50:
            self.happiness += factor
            self.happiness %= 100
        else:
            self.happiness -= factor
            if self.happiness < 0:
                self.happiness = 0

    def work(self, **kwargs):
        luck = int(r.random() * max(self.attributes.iteritems(), key=operator.itemgetter(1))[1])
        self.resources += int(math.floor(g.profession_pays[self.profession] * (luck)))
        self.update_happiness(luck)
        return self.name + " worked."

    def travel(self, free = False, **kwargs):
        if 'friend' in kwargs:
            new_location = kwargs['friend'].location
        if 'enemy' in kwargs:
            new_location = kwargs['enemy'].location
        if 'work' in kwargs:
            new_location = kwargs['work']

        #Need to specify location
        for id_num in range(len(self.location.connections)):
            if self.location.connections[id_num] is not 0 and self.location.connections[id_num].can_work(self):
                new_location = self.location.connections[id_num]

        self.location.ocupation -= 1
        new_location.increase_ocupation()
        if 'free' not in kwargs or kwargs['free'] == False:
            price = self.location.connections[new_location.id]
            self.resources -= price
        self.location.inhabitants.remove(self)
        self.location = new_location
        self.location.inhabitants.append(self)
        return self.name + " went to " + self.location.name + "."

    def die(self):
        return self.name + " died."

    def play(self, other = None, **kwargs):
        game = self.location.actions['play'][r.randint(0, len(self.location.actions['play'])-1)]
        players = [self]
        if game[2] > 1:
            for i in range(game[2]):
                players.append(self.location.inhabitants[r.randint(0, len(self.location.inhabitants)-1)])
        game_attribute = game[1]
        scores = {p.name : r.random() * 10 * p.attributes[game_attribute] for p in players}
        winner = max(scores.iteritems(), key=operator.itemgetter(1))[0]
        if winner == self.name:
            factor = (r.random()*self.personality['greedy'])
            log.info(factor)
            self.happiness += 20 * factor
            won = 'won.'
        else:
            won = "didn't win."
        return self.name + " played " + game[0] + " with " + str(players) + " and " + won

    def love(self, other = None, **kwargs):
        luck = int(r.random() * 10 * max(self.attributes.iteritems(), key=operator.itemgetter(1))[1])%100
        self.update_happiness(luck)
        return self.name + " loved."

    def argue(self, other = None, **kwargs):
        luck = int(r.random() * 10 * max(self.attributes.iteritems(), key=operator.itemgetter(1))[1])%100
        if 'enemy' in kwargs:
            enemy = kwargs['enemy']
        self.update_happiness(luck)
        return self.name + " argued."

    def fight(self, other = None, **kwargs):
        luck = int(r.random() * 10 * max(self.attributes.iteritems(), key=operator.itemgetter(1))[1])%100
        self.update_happiness(luck)
        return self.name + " fought."

    def steal(self, other = None, **kwargs):
        luck = int(r.random() * 10 *  max(self.attributes.iteritems(), key=operator.itemgetter(1))[1])%100
        self.update_happiness(luck)
        return self.name + " stole."
