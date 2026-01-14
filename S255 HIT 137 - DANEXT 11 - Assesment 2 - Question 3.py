import turtle

#Question 3 Generate A Geometric Pattern

print("╔════════════════════════════════════════╗")
print("║    Generate A Geometric Pattern        ║")
print("║  Created by: Craig, Jarrah, Mark, Dan  ║")
print("╚════════════════════════════════════════╝\n")
print("╔════════════════════════════════════════╗")
print("║   This program will generate a shape   ║")
print("║  of your design Just follow the prompt ║")
print("╚════════════════════════════════════════╝\n")

#Group Name:[DAN/EXT 11]
#[Team Members]
#[Jarrah Brain]-[S392191]
#[Mark Campbell]-[S385026]
#[Craig Shaw]-[S396655]
#[Dan Williams]-[S391056]


def draw_fractal_edge(t, length, depth):

    if depth == 0:
        t.forward(length)
    else:
        length /= 3.0
        draw_fractal_edge(t, length, depth - 1)
        t.left(60)
        draw_fractal_edge(t, length, depth - 1)
        t.right(120)
        draw_fractal_edge(t, length, depth - 1)
        t.left(60)
        draw_fractal_edge(t, length, depth - 1)


def draw_fractal_polygon(sides, length, depth):

    if sides < 3:
        print("Please enter a valid number of sides (3 or more).")
        return

    screen = turtle.Screen()
    screen.setup(width=800, height=800)
    screen.bgcolor("white")
    screen.title(f"Fractal Polygon (Sides: {sides}, Depth: {depth})")

    t = turtle.Turtle()
    t.speed("fastest")
    t.penup()
    t.goto(-length / 2, length / 2)
    t.pendown()
    t.color("Red")
    t.pensize(2)

    turn_angle = 360 / sides

    for _ in range(sides):
        draw_fractal_edge(t, length, depth)
        t.left(turn_angle)

    screen.exitonclick()


def get_user_input():
    try:
        sides = int(input("Please Enter the number of sides (e.g., 3 for triangle, 4 for square and so on..): "))
        length = int(input("Enter the side length (pixels (TRY 200)): "))
        depth = int(input("Enter the recursion depth: (start with 3)"))
        return sides, length, depth
    except ValueError:
        print("Invalid input. Please enter integers.")
        return None


if __name__ == "__main__":
    params = get_user_input()
    if params:
        s, l, d = params
        draw_fractal_polygon(s, l, d)