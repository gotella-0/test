import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SIZE, PLAYER_SPEED, BLUE

class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - PLAYER_SIZE - 10
        self.width = PLAYER_SIZE
        self.height = PLAYER_SIZE
        self.speed = PLAYER_SPEED
        self.lives = 3
    
    def draw(self, surface):
        # Draw a more interesting player shape
        pygame.draw.rect(surface, BLUE, (self.x, self.y, self.width, self.height), border_radius=10)
        pygame.draw.rect(surface, (0, 80, 200), (self.x+5, self.y+5, self.width-10, self.height-10), border_radius=5)
    
    def move(self, direction):
        if direction == "left" and self.x > 0:
            self.x -= self.speed
        if direction == "right" and self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed