import random as r
import generation as g
import logging
import operator
import math 
import sys

log = logging.getLogger(__name__)

class Character:
    def __init__(self):
        self.id = 0
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

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)


    def fill_social_vector(self, characters):
        #Filling social vector according to who other characters are
        #"Affinity" is decreasing, as we want to use a value that reflects how alike characters are
        log.info("Filling social Vector")
        self.social_vector = {char.id : self.calculate_affinity(char) for char in characters if char is not self}
        
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
        log.info("Action is " + action)
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
            'die': self.die,
            'cure': self.cure,
            'suicide': self.suicide

        }

        if action not in actions:
            return "SOMETHING WENT WRONG WITH " + action

        kwargs = {}
        words = action.split('_')[0]

        if len(words) > 1 and words[0] == 'travel':
            if len(words) > 2 and action.split('_')[1] == 'friend':
                log.info(max(self.social_vector.iteritems(), key=operator.itemgetter(1))[0])
                kwargs['friend'] = character_list[min(self.social_vector.iteritems(), key=operator.itemgetter(1))[0]]
            elif len(words) > 2 and action.split('_')[1] == 'enemy':
                kwargs['enemy'] = character_list[max(self.social_vector.iteritems(), key=operator.itemgetter(1))[0]]
            elif len(words) > 2 and action.split('_')[1] == 'free':
                kwargs['free'] = True
            if len(words) > 3 and words[2] == 'free':
                kwargs['free'] = True

        if action in ['steal', 'fight', 'argue', 'travel_enemy']:
            kwargs['enemy'] = character_list[max(self.social_vector.iteritems(), key=operator.itemgetter(1))[0]]

        if action in ['die', 'suicide']:
            kwargs['character_list'] = character_list


        return actions[action](**kwargs)

    def get_attribute(self, attr):
        return self.attr

    def update_booleans(self, characters, other = None):
        if characters[min(self.social_vector.iteritems(), key=operator.itemgetter(1))[0]].location == self.location:
            log.info("Friend is "+characters[min(self.social_vector.iteritems(), key=operator.itemgetter(1))[0]].name)
            self.friend_in_location_atr = True
        if characters[max(self.social_vector.iteritems(), key=operator.itemgetter(1))[0]].location == self.location:
            log.info("Enemy is "+characters[max(self.social_vector.iteritems(), key=operator.itemgetter(1))[0]].name)
            self.enemy_in_location_atr = True
        if self.profession in self.location.actions['work']:
            self.can_work_atr = True
        characters_in_loc = [c for c in characters if c.location == self.location and c.profession == 'doctor']
        if len(characters_in_loc) > 0:
            self.doctor_available_atr = True

    def log_booleans(self):
        log.info("friend_in_location_atr " + str(self.friend_in_location_atr))
        log.info("enemy_in_location_atr " + str(self.enemy_in_location_atr))
        log.info("sick " + str(self.sick_atr))
        log.info("social " + str(self.social_need))
        log.info("can_work " + str(self.can_work()))
        log.info("doctor_available " + str(self.doctor_available_atr))
        log.info("personality " + str(self.personality))
        log.info("is greedy " + str(self.is_greedy()))
        log.info("is loving " + str(self.is_romantic()))
        log.info("is violent " + str(self.is_violent()))


    def update_health(self):
        if self.sick:
            self.health -= 10
        else:
            self.health -= 2

        if self.health <20:
            log.info(r.random()*100 < 30)
            self.sick_atr = r.random()*100 < 3


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
        new_location = None

        if 'friend' in kwargs:
            new_location = kwargs['friend'].location
        if 'enemy' in kwargs:
            new_location = kwargs['enemy'].location
        if 'work' in kwargs:
            new_location = kwargs['work']
            log.info("Location here")

        

        #Need to specify location
        for id_num in range(len(self.location.connections)):
            if self.location.connections[id_num] is not 0 and self.location.connections[id_num].can_work(self):
                new_location = self.location.connections[id_num]
                log.info("Location here")
        if new_location is None:
            return self.name + " wanted to travel but couldn't."

        self.location.ocupation -= 1
        new_location.increase_ocupation()
        if 'free' not in kwargs or kwargs['free'] == False:
            price = self.location.connections[new_location.id].price
            self.resources -= price
        self.location.inhabitants.remove(self)
        self.location = new_location
        self.location.inhabitants.append(self)
        return self.name + " went to " + self.location.name + "."

    def die(self, **kwargs):
        if 'character_list' in kwargs:
            log.info((len(kwargs['character_list'])))
            kwargs['character_list'].remove(self)
            log.info((len(kwargs['character_list'])))
            for c in kwargs['character_list']:
                c.fill_social_vector(kwargs['character_list'])
            return self.name + " died."
        else:
            return "SOMETHING WENT WRONG"

    def play(self, other = None, **kwargs):
        game = self.location.actions['play'][r.randint(0, len(self.location.actions['play'])-1)]
        players = [self]
        if game[2] > 1:
            for i in range(game[2]-1):
                log.info(range(game[2]-1))
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

        playerList = ""
        players.remove(self)
        for player in players:
            if player == self:
                pass
            else:
                playerList += player.name + ", "
        return self.name + " played " + game[0] + " with " + playerList + " and " + won

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

    def cure(self):
        self.sick_atr = False
        self.health += 50
        return self.name + "saw a doctor and got cured."

    def suicide(self, **kwargs):
        if 'character_list' in kwargs:
            kwargs['character_list'].remove(self)
            for c in kwargs['character_list']:
                c.fill_social_vector(kwargs['character_list'])
            return self.name + "committed suicide."
        else:
            return "SOMETHING WENT WRONG"
