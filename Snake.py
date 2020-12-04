from sense_hat import SenseHat
import random
import time

# Joystick event parser
def GetJoyStickAction(Events):
    for Event in Events:
        if Event.action == "pressed" or Event.action == "held":
            return Event.direction
    return "none"

# Wrap snake around screen
def Wrap(Index):
    if Index == -1:
        return 7
    elif Index == 8:
        return 0
    return Index

# Game function
def Run():

    # Initialization
    Sense           = SenseHat()
    WHITE           = (255,255,255)
    RED             = (255,  0,  0)
    GREEN           = (  0,255,  0)
    Directions      = ("left","down","up","right")
    random.seed()
    Apple           = (random.randint(0,7),random.randint(0,7))  
    Snake           = [(random.randint(0,7),random.randint(0,7))]
    Direction       = random.choice(Directions)
    Score           = 100
    Coordinates     = []
    for X in range(0,8):
        for Y in range(0,8):
            Coordinates.append((X,Y))

    # NORMAL GAMEPLAY
    while True:
        
        # Check if pause
        JoyStickInput   = GetJoyStickAction(Sense.stick.get_events())
        if JoyStickInput == "middle":
            while True:
                if GetJoyStickAction(Sense.stick.get_events()) == "middle":
                    break

        # Move snake
        if JoyStickInput in Directions:
            Direction = JoyStickInput
        if Direction == "left":
            NewPoint = (Wrap(Snake[0][0]-1),Snake[0][1])
        elif Direction == "right":
            NewPoint = (Wrap(Snake[0][0]+1),Snake[0][1])
        elif Direction == "up":
            NewPoint = (Snake[0][0],Wrap(Snake[0][1]-1))
        elif Direction == "down":
            NewPoint = (Snake[0][0],Wrap(Snake[0][1]+1))
        Snake.insert(0,NewPoint)

        # Check if lost. Display score
        if len(Snake) > 1:
            for SnakeUnit in Snake[1:-1]:
                if Snake[0] == SnakeUnit:
                    Sense.show_message("Score: " + str(Score), 0.1, GREEN) 
                    while True:
                        if JoyStickInput == "middle":
                            return

        # Check if head on apple
        EmptySpots = list(set(Coordinates)^set(Snake))
        if Snake[0] == Apple:
            Apple = random.choice(EmptySpots)
            Score += 100
        else:
            Snake.pop(len(Snake)-1)        

        # Print out
        Sense.clear()
        for SnakeUnit in Snake:
            Sense.set_pixel(SnakeUnit[0],SnakeUnit[1],WHITE)
        Sense.set_pixel(Apple[0],Apple[1],RED)

        # Sleep
        time.sleep(0.25)

# Entrance point
if __name__ == "__main__":
    while True:
        Run()
         






