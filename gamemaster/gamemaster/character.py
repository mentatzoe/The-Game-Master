import random as r
import generation as g
import logging
import operator
import math 
import sys
import Image
import os

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
        if self.gender == 'male':
            self.pronoun = 'He'
        else:
            self.pronoun = 'She'
        self.generate_picture()

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

    def generate_picture(self):
        log.info("Generating picture")
        dirname = os.path.dirname(os.path.realpath(__file__))
        if self.gender == 'male':
            faces = 10
            hairs = 5
            outfits = 3
            route = dirname + "/static/images/male/"
        else:
            faces = 10
            hairs = 2
            outfits = 2
            route = dirname + "/static/images/female/"
        background = Image.open(route + "base.png")
        face_number = r.randint(1, faces)
        face = Image.open(route + "face" + str(face_number) +".png")
        background.paste(face, (0,0), face)
        hair_number = r.randint(1, hairs)
        outfit_number = r.randint(1, outfits)
        outfit = Image.open(route + "outfit" + str(outfit_number) +".png")
        hair = Image.open(route + "hair" + str(hair_number) +".png")
        background.paste(hair, (0,0), hair)
        background.paste(outfit, (0,0), outfit)
        self.picture = "/static/images/characters/" + str(r.random()) + "_" + self.name + ".png"
        background.save(dirname + self.picture)
        

    def fill_social_vector(self, characters):
        #Filling social vector according to who other characters are
        #"Affinity" is decreasing, as we want to use a value that reflects how alike characters are
        log.info("Filling social Vector")
        self.social_vector = {characters[char].id : self.calculate_affinity(characters[char]) for char in characters if characters[char] is not self}
        
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

    def is_best_friend(self, other):
        return other.id == min(self.social_vector.iteritems(), key=operator.itemgetter(1))[0]

    def is_enemy(self, other):
        return other.id == max(self.social_vector.iteritems(), key=operator.itemgetter(1))[0]

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
            'play_alone': self.play_alone,
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

        if action in ['travel_free', 'travel_friend_free', 'travel_enemy_free']:
            kwargs['free'] = True

        if action in ['steal', 'fight', 'argue', 'travel_enemy', 'travel_enemy_free']:
            kwargs['enemy'] = character_list[max(self.social_vector.iteritems(), key=operator.itemgetter(1))[0]]

        if action in ['love', 'travel_friend', 'travel_friend_free']:
            kwargs['friend'] = character_list[min(self.social_vector.iteritems(), key=operator.itemgetter(1))[0]]
            log.info(kwargs['friend'].id)

        kwargs['character_list'] = character_list


        return actions[action](**kwargs)

    def get_attribute(self, attr):
        return self.attr

    def update_booleans(self, characters, other = None):
        friend = characters[min(self.social_vector.iteritems(), key=operator.itemgetter(1))[0]]
        enemy = characters[max(self.social_vector.iteritems(), key=operator.itemgetter(1))[0]]

        if friend.location == self.location:
            self.friend_in_location_atr = True

        if enemy.location == self.location:
            self.enemy_in_location_atr = True

        if self.profession in self.location.actions['work']:
            self.can_work_atr = True

        doctors_in_loc = [characters[char] for char in characters if characters[char].location == self.location and characters[char].profession == 'doctor']
        if len(doctors_in_loc) > 0:
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
            self.health -= 0.1

        if self.health <20:
            self.sick_atr = r.random()*100 < 3


    def update_happiness(self, factor):
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
        self.social_need += 20
        return self.pronoun + " worked."

    def travel(self, free = False, **kwargs):
        new_location = None
        reason = ""
        if 'friend' in kwargs:
            new_location = kwargs['friend'].location
            log.info("friend in travel " + str(kwargs['friend'])+ " " + kwargs['friend'].location.name)
            reason = " searching for " + kwargs['friend'].name
        if 'enemy' in kwargs:
            new_location = kwargs['enemy'].location
            reason = " searching for " + kwargs['enemy'].name
            log.info("enemy in travel " + str(kwargs['enemy']) + " " + kwargs['enemy'].location.name)
        if 'work' in kwargs:
            new_location = kwargs['work']

        #Need to specify location
        if new_location is None:
            for id_num in range(len(self.location.connections)):
                if self.location.connections[id_num] is not 0 and self.location.connections[id_num].can_work(self):
                    new_location = self.location.connections[id_num]
            if new_location is None:
                return self.pronoun + " wanted to travel but couldn't."

        self.location.ocupation -= 1
        new_location.increase_ocupation()
        if 'free' not in kwargs or kwargs['free'] == False:
            log.info(self.location)
            try:
                price = self.location.connections[new_location.id].price
            except:
                price = 3000
            self.resources -= price
        old_location = self.location
        self.location.inhabitants.remove(self)
        self.location = new_location
        self.location.inhabitants.append(self)
        log.info(new_location.name + ": ")
        for c in new_location.inhabitants:
            log.info(c.name)
        log.info(self in old_location.inhabitants)
        for c in kwargs['character_list']:
            kwargs['character_list'][c].update_booleans(kwargs['character_list'])

        return self.pronoun + " went to " + self.location.name + reason + "."

    def die(self, **kwargs):
        return self.pronoun + " died."

    def play(self, other = None, **kwargs):
        if len(self.location.inhabitants) == 1:
            return self.play_alone()
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
            factor = int((r.random()*self.personality['greedy']) *10)
            log.info(factor)
            self.happiness += factor
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
        return self.pronoun + " played " + game[0] + " with " + playerList + " and " + won


    def play_alone(self, other = None, **kwargs):
        game = self.location.actions['play_alone'][r.randint(0, len(self.location.actions['play'])-1)]
        self.attributes[game[1]] += 1
        previous = self.social_need
        self.social_need += int(10 + previous * 0.1)
        self.happiness += 10
        return self.pronoun + " " + game[0] + "."

    def love(self, other = None, **kwargs):
        other = kwargs['friend']
        log.info(other)
        if other.is_romantic():
            if other.is_best_friend(self):
                if not self.married and not other.married:
                    self.social_vector[other.id] -= 30
                    other.social_vector[self.id] -= 30
                    self.married = True
                    self.spouse = other
                    other.married = True
                    other.spouse = self
                    self.social_need -= 20
                    self.happiness += 50
                    return self.pronoun + " and " + other.name + " got married."
                else:
                    self.social_vector[other.id] -= 15
                    other.social_vector[self.id] -= 15
                    self.social_need -= 20
                    self.happiness += 30
                    return self.pronoun + " and " + other.name + " spent some time together."
            else:
                self.social_vector[other.id] += 10
                self.social_need -= 20
                self.happiness -= 30
                return self.pronoun + " was rejected by " + other.name + "."
        else:
            self.social_vector[other.id] -= 15
            other.social_vector[self.id] -= 15
            self.social_need -= 20
            self.happiness += 20
            return self.pronoun + " and " + other.name + " spent some time together."

    def argue(self, other = None, **kwargs):
        if 'enemy' in kwargs:
            other = kwargs['enemy']
        
        modifier = ""
        if self.attributes['int'] > other.attributes['int']:
            self.happiness += 20
            other.happiness -= 5
        else:
            self.happiness -= 20
            other.happiness += 5
        if r.randint(0,1) == 1:
            modifier = " but they became closer from it"
            self.social_vector[other.id] -= 30
            other.social_vector[self.id] -= 30
        else:
            self.social_vector[other.id] += 15
            other.social_vector[self.id] += 15
        return self.pronoun + " argued with " + other.name + modifier + "."
 
    def fight(self, other = None, **kwargs):
        if other is not None:
            enemy = other
        else:
            enemy = kwargs['enemy']

        if not enemy.is_violent:
            if self.personality['violent'] > 90:
                if enemy.attributes['con'] < 16:
                    #decrease enemy health
                    #decrease enemy happiness
                    #incre enemy unaffinity
                    #increase self happiness
                    enemy.health -= abs(int(enemy.attributes['con'] - self.attributes['str'] * r.random()))
                    enemy.happiness -= 60
                    enemy.social_vector[self.id] += 300
                    self.happiness += 40
                    self.social_need -= 40
                    return self.pronoun + " gave " + enemy.name + " a beating."
                else:
                    enemy.happiness -= 20
                    enemy.social_vector[self.id] += 300
                    self.happiness -= 10
                    self.social_need -= 40
                    return self.pronoun + " tried to give " + enemy.name + " a beating but wasn't strong enough."
            else:
                enemy.happiness -= 20
                enemy.social_vector[self.id] += 100
                self.happiness -= 1
                self.social_need -= 40
                return self.pronoun + " volently confronted " + enemy.name + ", who surrendered."
        else:
            if self.attributes['str'] > enemy.attributes['str']:
                if enemy.attributes['con'] < 16:
                    #decrease enemy health
                    #decrease enemy happiness
                    #incre enemy unaffinity
                    #increase self happiness
                    enemy.health -= abs(int(enemy.attributes['con'] - self.attributes['str'] * r.random()))
                    enemy.happiness -= 20
                    enemy.social_vector[self.id] += 100
                    self.happiness += 40
                    self.social_need -= 40
                    return self.pronoun + " fought " + enemy.name + " and won."
                else:
                    enemy.happiness += 20
                    enemy.social_vector[self.id] += 300
                    self.health -= abs(int(self.attributes['con'] - enemy.attributes['str'] * r.random()))
                    self.happiness -= 10
                    self.social_need -= 40
                    return self.pronoun + " fought " + enemy.name + " and lost."
            else:
                if self.attributes['con'] < 16:
                    #decrease enemy health
                    #decrease enemy happiness
                    #incre enemy unaffinity
                    #increase self happiness
                    self.health -= abs(int(self.attributes['con'] - enemy.attributes['str'] * r.random()))
                    self.happiness -= 20
                    self.social_vector[enemy.id] += 100
                    enemy.happiness += 40
                    enemy.social_need -= 40
                    return self.pronoun + " fought " + enemy.name + " and won."
                else:
                    self.happiness += 20
                    self.social_vector[enemy.id] += 300
                    enemy.health -= abs(int(enemy.attributes['con'] - self.attributes['str'] * r.random()))
                    enemy.happiness -= 10
                    enemy.social_need -= 40
                    return self.pronoun + " fought " + enemy.name + " and lost."                


        luck = int(r.random() * 10 * max(self.attributes.iteritems(), key=operator.itemgetter(1))[1])%100

        self.update_happiness(luck)
        return self.pronoun + " fought."

    def steal(self, other = None, **kwargs):
        if len(self.location.inhabitants) == 1:
            return self.play_alone()
        victim = self.location.inhabitants[r.randint(0, len(self.location.inhabitants)-1)]
        result = ""
        while victim == self:
            victim = self.location.inhabitants[r.randint(0, len(self.location.inhabitants)-1)]
        success_skills = self.attributes['dex'] + self.attributes['int'] > victim.attributes['int'] + victim.attributes['dex'] and r.randint(0,100) > 40
        success_strength = self.attributes['str'] > victim.attributes['str'] or self.attributes['str'] > victim.attributes['con'] and r.randint(0,100) > 60
        if success_skills:
            self.happiness += 50
            self.social_need += 20
            amount = int(victim.resources * r.random())
            victim.resources -= amount
            self.resources += amount
            if r.randint(0,1) == 1:
                result = ", who found out about it"
                victim.social_vector[self.id] += 100
            return self.pronoun + " stole " + str(amount) + " credits from " + victim.name + result + "."
        elif success_strength:
            self.happiness += 10
            self.social_need += 20
            amount = int(victim.resources * r.random())
            victim.resources -= amount
            self.resources += amount
            victim.social_vector[self.id] += 300
            victim.happiness -= 30
            return self.pronoun + " violently stole " + str(amount) + " credits from " + victim.name + result + "."
        elif not success_strength and not success_skills:
            #will never succeed
            return self.fight(victim)
        else:
            self.happiness -= 10
            self.social_need -= 20
            if r.randint(0,1) == 1:
                result = " but was found out"
                victim.social_vector[self.id] += 100
            return self.pronoun + " tried to steal from " + victim.name + result + "."

        return self.pronoun + " stole."

    def cure(self, **kwargs):
        self.sick_atr = False
        self.health += 50
        return self.pronoun + " saw a doctor and got cured."

    def suicide(self, **kwargs):
        if 'character_list' in kwargs:
            return self.pronoun + " committed suicide."
        else:
            return "SOMETHING WENT WRONG"
