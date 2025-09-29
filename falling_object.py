import pygame
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, OBJECT_SIZE, OBJECT_SPEED, RED, GREEN, YELLOW, PURPLE

class FallingObject:
    def __init__(self, obj_type="normal"):
        self.x = random.randint(0, SCREEN_WIDTH - OBJECT_SIZE)
        self.y = -OBJECT_SIZE
        self.width = OBJECT_SIZE
        self.height = OBJECT_SIZE
        self.type = obj_type
        self.speed = OBJECT_SPEED
        
        # Different types of objects
        if self.type == "normal":
            self.color = RED
            self.points = 1
        elif self.type == "bonus":
            self.color = GREEN
            self.points = 5
            self.width = OBJECT_SIZE - 10
            self.height = OBJECT_SIZE - 10
        elif self.type == "life":
            self.color = YELLOW
            self.points = 0
            self.width = OBJECT_SIZE - 15
            self.height = OBJECT_SIZE - 15
        elif self.type == "bomb":
            self.color = PURPLE
            self.points = 0
            self.width = OBJECT_SIZE + 5
            self.height = OBJECT_SIZE + 5
    
    def draw(self, surface):
        if self.type == "normal":
            pygame.draw.circle(surface, self.color, (self.x + self.width//2, self.y + self.height//2), self.width//2)
        elif self.type == "bonus":
            pygame.draw.polygon(surface, self.color, [
                (self.x + self.width//2, self.y),
                (self.x + self.width, self.y + self.height//2),
                (self.x + self.width//2, self.y + self.height),
                (self.x, self.y + self.height//2)
            ])
        elif self.type == "life":
            pygame.draw.ellipse(surface, self.color, (self.x, self.y, self.width, self.height))
        elif self.type == "bomb":
            pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height), border_radius=15)
    
    def fall(self):
        self.y += self.speed
        return self.y > SCREEN_HEIGHT
    
    def collides_with(self, player):
        return (self.x < player.x + player.width and
                self.x + self.width > player.x and
                self.y < player.y + player.height and
                self.y + self.height > player.y)