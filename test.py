from graphics import *

win_size = 800
win = GraphWin(width=win_size, height=win_size)

border_size = 50

map_color = color_rgb(90, 110, 68)
player_color = color_rgb(57, 76, 189)
food_color = color_rgb(209, 206, 10)
obstacle_color = color_rgb(186, 17, 45)

# DRAW MAP
map_up_left = Point(border_size, border_size)
map_down_right = Point(win_size - border_size, win_size-border_size)

rect = Rectangle(map_up_left, map_down_right)
rect.setFill(map_color)
rect.setOutline('red')
rect.draw(win)

# DRAW FOODS

food = Circle(Point(200, 200), 7)
food.setFill(food_color)
food.draw(win)

# DRAW OBSTACLES

obs = Rectangle(Point(300, 300), Point(330, 330))
obs.setFill(obstacle_color)
obs.draw(win)

# DRAW PLAYER

x = 500
y = 500

vertices = [Point(x, y-15),
            Point(x-10, y+15),
            Point(x+10, y+15)]

player = Polygon(vertices)
player.setFill(player_color)
player.draw(win)

win.getMouse()
win.close()