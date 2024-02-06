from Journey import Journey


class User:

    def __init__(self, username, biowake, asleep):
        self.username = username
        self.biowake = biowake
        self.asleep = asleep
        self.journey = None
        self.coordinates = []

    def get_username(self):
        return self.username

    def get_biowake(self):
        return self.biowake

    def get_asleep(self):
        return self.asleep

    def get_journey(self):
        return self.journey

    def get_coordinates(self):
        return self.coordinates

    def add_coordinates(self):
        self.coordinates.append(self.journey.get_loc())

    def add_journey(self, Dcity, Acity, land, nights):
        self.journey = Journey(Dcity, Acity, land, nights)



