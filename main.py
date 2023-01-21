import threading
import random
import time

class Philosopher:
    # Constructor
    def __init__(self, name, forkLeft, forkRight, seat, forks, lastAte):
        self.name = name
        self.forkLeft = forkLeft
        self.forkRight = forkRight
        self.seat = seat
        self.forks = forks
        self.lastAte = lastAte
    
    # Check if the Philosopher has a fork in both hands
    def check_forks(self):
        if self.forkLeft & self.forkRight == True:
            return True
        else:
            return False
    
    # Randomize which hand the Philosopher uses first, get the fork, then get the fork for the other hand
    def get_forks(self):
        choices = [Philosopher.pick_up_fork_left, Philosopher.pick_up_fork_right]
        choice = random.randint(0, 1)
        choices[choice](self)
        choices[choice - 1](self)

    # Getting a lock on the fork semaphore at the index to the "left"
    def pick_up_fork_left(self):
        self.forkLeft = self.forks[self.seat].acquire()
        print(Philosopher.__str__(self))
    
    # Getting a lock on the fork semaphore at the index to the "right"
    def pick_up_fork_right(self):
        self.forkRight = self.forks[self.seat - 1].acquire()
        print(Philosopher.__str__(self))

    # Chow time!
    def eating(self):
        print(self.name + " is eating")
        time.sleep(1)
        # Release locks on both fork semaphores in list forks
        self.forks[self.seat].release()
        self.forks[self.seat - 1].release()
        # Empty the Philosophers hands
        self.forkLeft = False
        self.forkRight = False
        # Log the last time the Philosopher ate
        self.lastAte = time.time()
    
    # Defines the str() object to be returned when print(p) is called
    def __str__(self):
        ateSecondsAgo = format(time.time() - self.lastAte, 'f')
        return "name: {}, seat: {}, forkLeft: {}, forkRight: {}, lastAte: {}s ago".format(self.name, self.seat, self.forkLeft, self.forkRight, ateSecondsAgo)


def actions(name, seat, forks):
    # They all just ate before they arrived :D
    lastAte = time.time()

    # Create the philosopher with both hands empty and knowledge of the list of semaphores
    p = Philosopher(name, False, False, seat, forks, lastAte)

    # Keep the party going forever
    while True:
        print(p)
        # Check to see if the philosopher has a fork in each hand
        while p.check_forks() == False:
            # Keep trying to get forks!
            p.get_forks()
        p.eating()


if __name__ == '__main__':
    # Construct a list of 5 semaphores, 1 for each fork
    forks = []
    for i in range(5):
        forks.append(threading.Semaphore())

    # Create the philosophers, assign them seats, and have then start taking actions
    attendees = ["plato", "aristotle", "camus", "sartre", "foucault"]
    for seat in range(len(attendees)):
        t = threading.Thread(target=actions, args=(attendees[seat], seat, forks,))
        t.start()
   
