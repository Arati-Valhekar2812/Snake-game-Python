import turtle
import random
import time
import winsound   # For sound on Windows

delay = 0.25
sc = 0
hs = 0
bodies = []

game_running = False
game_paused = False

# Creating a screen
s = turtle.Screen()
s.title("Snake Game")
s.bgcolor("black")
s.setup(width=600, height=600)
s.tracer(0)

# Draw walls (border)
wall = turtle.Turtle()
wall.speed(0)
wall.color("white")
wall.penup()
wall.goto(-290, -290)
wall.pendown()
wall.pensize(3)
for _ in range(4):
    wall.forward(580)
    wall.left(90)
wall.hideturtle()

# creating a head
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("yellow")
head.fillcolor("red")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# creating a food
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

# score board
sb = turtle.Turtle()
sb.ht()
sb.penup()
sb.goto(-250, 260)
sb.color("white")

# Message turtle (start, pause, game over)
msg = turtle.Turtle()
msg.ht()
msg.penup()
msg.color("white")
msg.goto(0, 0)

def update_score():
    sb.clear()
    sb.write("Score: {} | Highest Score: {}".format(sc, hs), font=("Arial", 14, "normal"))

def show_start_screen():
    s.bgcolor("black")
    msg.clear()
    msg.goto(0, 40)
    msg.write("🐍 SNAKE GAME 🐍", align="center", font=("Arial", 26, "bold"))
    msg.goto(0, 0)
    msg.write("Press SPACE to Start", align="center", font=("Arial", 18, "normal"))
    msg.goto(0, -30)
    msg.write("Press P to Pause/Resume", align="center", font=("Arial", 14, "normal"))

def start_game():
    global game_running, sc, delay
    if not game_running:
        msg.clear()
        game_running = True
        head.goto(0, 0)
        head.direction = "stop"
        sc = 0
        delay = 0.25
        update_score()

def toggle_pause():
    global game_paused
    if game_running:
        game_paused = not game_paused
        msg.clear()
        if game_paused:
            msg.goto(0, 0)
            msg.write("⏸ PAUSED", align="center", font=("Arial", 30, "bold"))
        else:
            msg.clear()

def moveup():
    if not game_paused and head.direction != "down":
        head.direction = "up"

def movedown():
    if not game_paused and head.direction != "up":
        head.direction = "down"

def moveleft():
    if not game_paused and head.direction != "right":
        head.direction = "left"

def moveright():
    if not game_paused and head.direction != "left":
        head.direction = "right"

def movestop():
    if not game_paused:
        head.direction = "stop"

def move():
    if game_paused:
        return

    if head.direction == "up":
        head.sety(head.ycor() + 20)
    if head.direction == "down":
        head.sety(head.ycor() - 20)
    if head.direction == "left":
        head.setx(head.xcor() - 20)
    if head.direction == "right":
        head.setx(head.xcor() + 20)

# event handling
s.listen()
s.onkey(moveup, "Up")
s.onkey(movedown, "Down")
s.onkey(moveleft, "Left")
s.onkey(moveright, "Right")
s.onkey(movestop, "space")
s.onkey(start_game, "space")
s.onkey(toggle_pause, "p")

# Show start screen initially
show_start_screen()

# mainloop
while True:
    s.update()

    if not game_running or game_paused:
        time.sleep(0.1)
        continue

    # ❌ Wall collision (Game Over)
    if head.xcor() > 280 or head.xcor() < -280 or head.ycor() > 280 or head.ycor() < -280:
        winsound.PlaySound("gameover.wav", winsound.SND_ASYNC)
        s.bgcolor("dark red")
        msg.clear()
        msg.goto(0, 0)
        msg.write("GAME OVER", align="center", font=("Arial", 36, "bold"))
        s.update()
        time.sleep(2)
        s.bgcolor("black")
        msg.clear()
        game_running = False

        for body in bodies:
            body.ht()
        bodies.clear()
        head.goto(0, 0)
        head.direction = "stop"
        sc = 0
        delay = 0.25
        update_score()
        show_start_screen()
        continue

    # check collision with food
    if head.distance(food) < 20:
        winsound.PlaySound("eat.wav", winsound.SND_ASYNC)

        x = random.randint(-260, 260)
        y = random.randint(-260, 260)
        food.goto(x, y)

        body = turtle.Turtle()
        body.speed(0)
        body.penup()
        body.shape("circle")
        body.color("sky blue")
        bodies.append(body)

        sc += 10
        update_score()
        delay = max(0.05, delay - 0.001)

    # move the snake bodies
    for index in range(len(bodies) - 1, 0, -1):
        bodies[index].goto(bodies[index - 1].xcor(), bodies[index - 1].ycor())

    if len(bodies) > 0:
        bodies[0].goto(head.xcor(), head.ycor())

    move()
    time.sleep(delay)

    # check collision with body
    for body in bodies:
        if body.distance(head) < 20:
            winsound.PlaySound("gameover.wav", winsound.SND_ASYNC)
            s.bgcolor("dark red")
            msg.clear()
            msg.goto(0, 0)
            msg.write("GAME OVER", align="center", font=("Arial", 36, "bold"))
            s.update()
            time.sleep(2)
            s.bgcolor("black")
            msg.clear()
            game_running = False

            for body in bodies:
                body.ht()
            bodies.clear()
            head.goto(0, 0)
            head.direction = "stop"
            sc = 0
            delay = 0.25
            update_score()
            show_start_screen()
            break

s.mainloop()
