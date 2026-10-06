
class Interested:
    def __init__(self):
        self.events = []
    
    def set_notify(self, id:int):
        self.events.append(id)
        #print(self.events)

    def events_get(self):
        ret = self.events.copy()
        self.events = []
        return ret


Anchor:int = 1
Select:int = 2
Fill:int = 3

class Notify():
    def __init__(self, interested:list[Interested], id:int):
        self.interested = interested
        self.id = id

    def event(self):
        #print(self.interested)
        for i in self.interested:
            print("notify", self.id)
            i.set_notify(self.id)

    