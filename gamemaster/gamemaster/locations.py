#Locations file
'''
Temporarily generate locations statically
Info that we need: Name, Trip price, Work actions, Capacity, Ocupation, Connections
'''

class Location:
    def __init__(self, id, name, workactions, playactions, capacity, price):
        self.id = id
        self.name = name
        self.actions = {
            'work' : workactions,
            'play' : playactions
        }
        self.capacity = capacity
        self.ocupation = 0
        self.connections = {}
        self.inhabitants = []
        self.price = price

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def increase_ocupation(self):
        if self.ocupation < self.capacity:
            self.ocupation += 1
            return self.ocupation
        else:
            return False

    def set_connections(self, connections):
        self.connections = connections

    def is_full(self):
        return self.ocupation == self.capacity

    def can_work(self, c):
        return c.profession in self.actions['work']

def generate():
    location_list = []
    spaceship = Location(0, 'Horizon RK7', ['military', 'doctor', 'builder'], [('chess', 'int', 2), ('virtual sports', 'dex', 3)], 5, 3000)
    city = Location(1, 'Sydney Archology', ['police', 'scholar', 'doctor', 'artist', 'salesman', 'politician'], [('chess', 'int', 2), ('virtual sports', 'dex', 7), ('study', 'int', 1)], 12, 2000)
    colony = Location(2, 'Luthien Prime Colony', ['military', 'police', 'doctor', 'builder', 'salesman', 'politician'], [('chess', 'int', 2), ('virtual sports', 'dex', 5)], 7, 3500) 
    
    spaceship.set_connections({spaceship.id: 0, city.id: city, colony.id: colony})
    city.set_connections({spaceship.id: spaceship, city.id: 0, colony.id: colony})
    colony.set_connections({spaceship.id: spaceship, city.id: city, colony.id: 0})


    location_list.append(spaceship)
    location_list.append(city)
    location_list.append(colony)
    

    return location_list