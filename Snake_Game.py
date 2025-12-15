import turtle
import random
import time

delay = 0.25
sc = 0
hs = 0
bodies = []

#Creating a screen
s = turtle.Screen()
s.title("Snake Game")
s.bgcolor("black")
s.setup(width=600, height=600)

#creating a head
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("yellow")
head.fillcolor("red")
head.penup()
head.goto(0, 0)
head.direction = "stop"

#creating a food
food = turtle.Turtle()
food.speed(0)
food.shape("square")
food.color("red")
food.fillcolor("blue")
food.penup()
food.ht()
food.goto(150, 250)
food.st()
food.direction = "stop"

#score board
sb = turtle.Turtle()
sb.ht()
sb.penup()
sb.goto(-250, 250)
sb.color("white")
sb.write("Score: 0 | Highest Score: 0", font=("Arial", 14, "normal"))

def update_score():
    sb.clear()
    sb.write("Score: {} | Highest Score: {}".format(sc, hs), font=("Arial", 14, "normal"))

def moveup():
    if head.direction != "down":
        head.direction = "up"

def movedown():
    if head.direction != "up":
        head.direction = "down"

def moveleft():
    if head.direction != "right":
        head.direction = "left"

def moveright():
    if head.direction != "left":
        head.direction = "right"

def movestop():
    head.direction = "stop"

def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)

    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)

    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)

    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

#event handling
s.listen()
s.onkey(moveup, "Up")
s.onkey(movedown, "Down")
s.onkey(moveleft, "Left")
s.onkey(moveright, "Right")
s.onkey(movestop, "space")

#mainloop
while True:
    s.update()

    #check collision with border
    if head.xcor() > 290:
        head.setx(-290)
    if head.xcor() < -290:
        head.setx(290)
    if head.ycor() > 290:
        head.sety(-290)
    if head.ycor() < -290:
        head.sety(290)

    #check collision with food
    if head.distance(food) < 20:
        x = random.randint(-290, 290)
        y = random.randint(-290, 290)
        food.goto(x, y)

        #increase the length of snake
        body = turtle.Turtle()
        body.speed(0)
        body.penup()
        body.shape("circle")
        body.color("sky blue")
        bodies.append(body)

        #increase the score
        sc += 10
        if sc > hs:
            hs = sc
        update_score()

        #increase speed
        delay = max(0.05, delay - 0.001)

    #move the snake bodies
    for index in range(len(bodies) - 1, 0, -1):
        x = bodies[index - 1].xcor()
        y = bodies[index - 1].ycor()
        bodies[index].goto(x, y)

    if len(bodies) > 0:
        x = head.xcor()
        y = head.ycor()
        bodies[0].goto(x, y)

    move()
    time.sleep(delay)

    #check collision with body
    for body in bodies:
        if body.distance(head) < 20:
            time.sleep(1)
            head.goto(0, 0)
            head.direction = "stop"

            for body in bodies:
                body.ht()
            bodies.clear()
            sc = 0
            delay = 0.25
            update_score()

s.mainloop()
