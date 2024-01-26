class Hammock:
    def __init__(self) -> None:
        self.sitting = []
        self.last_request = None
    def sitDown(self, person):
        if not self.sitting:
            self.sitting.append(person)
            self.last_request = person
            return "welcome!"
        elif person == self.last_request:
            self.sitting.append(person)
            return "welcome!"
        else:
            self.last_request = person
            return "sorry, no room"
    def leave(self):
        if not self.sitting: return 0 # you can't pop from empty list
        self.sitting.pop(0)
        return len(self.sitting)
    
# test
myHammock = Hammock()
print(f"-> myHammock.sitDown('George') \n {myHammock.sitDown('George')}")
print(f"-> myHammock.sitDown('Bobby') \n {myHammock.sitDown('Bobby')}")
print(f"-> myHammock.sitDown('Bobby')\n {myHammock.sitDown('Bobby')}")
print(f"-> myHammock.leave()\n {myHammock.leave()}")
print(f"-> myHammock.leave()\n {myHammock.leave()}")
print(f"-> myHammock.leave()\n {myHammock.leave()}")
print(f"-> myHammock.sitDown('Martha')\n {myHammock.sitDown('Martha')}")
print(f"-> myHammock.sitDown('Wilhelm')\n {myHammock.sitDown('Wilhelm')}")
print(f"-> myHammock.sitDown('Klaus')\n {myHammock.sitDown('Klaus')}")
print(f"-> myHammock.sitDown('Wilhelm')\n {myHammock.sitDown('Wilhelm')}")
print(f"-> myHammock.leave()\n {myHammock.leave()}")
