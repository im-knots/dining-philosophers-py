import threading
import random
import time

attendees = ["plato", "aristotle", "camus", "sartre", "foucault"]

class Philosopher:
    def __init__(self, name, forkLeft, forkRight, lastAte):
        self.name = name
        self.forkLeft = forkLeft
        self.forkRight = forkRight
        self.lastAte = lastAte
    
    def pick_up_fork_left(self):
        global fork
        fork.acquire()
        self.forkLeft = True
        print(self.name + " took a fork on the left")
        print(self.name + " " + str(self.forkLeft) + " " + str(self.forkRight))
    
    def pick_up_fork_right(self):
        global fork
        fork.acquire()
        self.forkRight = True
        print(self.name + " took a fork on the right")
        print(self.name + " " + str(self.forkLeft) + " " + str(self.forkRight))
    
    def check_forks(self):
        if self.forkLeft & self.forkRight == True:
            print(self.name + " is ready to eat")
            return True
        elif self.forkLeft & self.forkRight == False:
            print(self.name + " is not ready to eat")
            print(self.name + " " + str(self.forkLeft) + " " + str(self.forkRight))
            return False

    def thinking(self):
        print(self.name + " is thinking")
        time.sleep(10)

    def eating(self):
        global fork
        print(self.name + " is eating")
        time.sleep(5)
        print(self.name + " is done eating, puts down their forks, and goes to think")
        for i in range(2):
            fork.release()
        self.forkLeft = False
        self.forkRight = False
        print(self.name + " " + str(self.forkLeft) + " " + str(self.forkRight))
        self.lastAte = time.time()

   
    def hungry(self):
        print(self.name + " is hungry")
    
    def share_fork(self):
        global fork
        print(self.name + " isnt hungry so will share a fork")
        fork.release()

    def __str__(self):
        return "Name: {}, LFork: {}, RFork: {}".format(self.name, self.forkLeft, self.forkRight)  


def activity(name):
    p = Philosopher(name, False, False, time.time())

    def get_forks():
        while p.check_forks() == False:
            random.choice([p.pick_up_fork_left(), p.pick_up_fork_right()])
            print(p.name + " last ate " + format(time.time() - p.lastAte, 'f') + " seconds ago")
            if int(time.time() - p.lastAte) > 5:
                p.hungry()
    while True:
        get_forks()
        p.eating()
        p.thinking()
