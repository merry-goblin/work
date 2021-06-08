
import os
import math
import arcade 
import pymunk
import timeit 
from PIL import Image 

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Angry Birds"

class PhysicsSprite(arcade.Sprite):

    def __init__(self, pymunk_shape, filename):

        super().__init__(pymunk_shape, filename, center_x=pymunk_shape.body.position.x, center_y=pymunk_shape.body.position.y)
        self.pymunk_shape = pymunk_shape

class CircleSprite(PhysicsSprite):

    def __init__(self, pymunk_shape, filename):

        super().__init__(pymunk_shape, filename)
        self.width = pymunk_shape.radius * 2
        self.height = pymunk_shape.radius * 2

class BoxSprite(PhysicsSprite):

    def __init__(self, pymunk_shape, filename, width, height):

        super().__init__(pymunk_shape, filename)
        self.width = width
        self.height = height

def make_sprite(mass, image, position, space):

    width, height = Image.open(image).size 
    mass = mass 
    moment = pymunk.moment_for_box(mass, (width, height))
    body = pymunk.Body(mass, moment)
    body.position = pymunk.Vec2d(position[0], position[1])
    shape = pymunk.Poly.create_box(body, (width, height))
    shape.friction = 0.3
    space.add(body, shape)
    sprite = BoxSprite(shape, image, width=width, height=height)

    return sprite

class MyGame(arcade.Window):

    def __init__(self, width, height, title):

        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)

        self.parabolic_points = []
        self.dx = self.dy = 0
        self.space = pymunk.Space()
        self.space.gravity = (0.0, -900.0)
        self.background = arcade.Sprite("assets/images/background.png")
        self.background.left = self.background.bottom = 0
        self.sprite_list = arcade.SpriteList()
        self.static_lines = []
        self.shape_being_dragged = None
        self.last_mouse_position = 0, 0
        self.draw_time = 0
        self.processing_time = 0

        floor_height = 80
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        shape = pymunk.Segment(body, [0, floor_height], [SCREEN_WIDTH, floor_height], 0.0)
        shape.friction = 10
        self.space.add(body, shape)
        self.static_lines.append(shape)

        box = make_sprite(43, "assets/images/boxCrate_double.png", (1000, 130), self.space)
        self.sprite_list.append(box)
        box = make_sprite(43, "assets/images/boxCrate_double.png", (1000, 230), self.space)
        self.sprite_list.append(box)
        box = make_sprite(43, "assets/images/boxCrate_double.png", (1000, 330), self.space)
        self.sprite_list.append(box)
        box = make_sprite(43, "assets/images/boxCrate_double.png", (1000, 430), self.space)
        self.sprite_list.append(box)
        box = make_sprite(43, "assets/images/boxCrate_double.png", (1000, 530), self.space)
        self.sprite_list.append(box)
        box = make_sprite(43, "assets/images/boxCrate_double.png", (1000, 630), self.space)
        self.sprite_list.append(box)
        
        sprite = make_sprite(33, "assets/images/pig.png", (1000,620), self.space)
        self.sprite_list.append(sprite)
        sprite = make_sprite(33, "assets/images/platform.png", (160,160), self.space)
        self.sprite_list.append(sprite)
        self.shoot_position = pymunk.Vec2d(160, 290)
        self.physic_bird = make_sprite(33, "assets/images/bird.png", self.shoot_position, self.space)
        self.sprite_list.append(self.physic_bird)
        self.virtual_bird = arcade.Sprite("assets/images/bird.png")
        self.virtual_bird.center_x = self.shoot_position[0]
        self.virtual_bird.center_y = self.shoot_position[1]
        self.reset_shoot = True"""

def main():
    MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()

main()
