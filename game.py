import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SIZE = 50
OBJECT_SIZE = 30
PLAYER_SPEED = 5
OBJECT_SPEED = 3
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Catch Game")
clock = pygame.time.Clock()

# Player class
class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - PLAYER_SIZE - 10
        self.width = PLAYER_SIZE
        self.height = PLAYER_SIZE
        self.speed = PLAYER_SPEED
    
    def draw(self):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))
    
    def move(self, direction):
        if direction == "left" and self.x > 0:
            self.x -= self.speed
        if direction == "right" and self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed

# Falling object class
class FallingObject:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH - OBJECT_SIZE)
        self.y = -OBJECT_SIZE
        self.width = OBJECT_SIZE
        self.height = OBJECT_SIZE
        self.speed = OBJECT_SPEED
    
    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))
    
    def fall(self):
        self.y += self.speed
        return self.y > SCREEN_HEIGHT
    
    def collides_with(self, player):
        return (self.x < player.x + player.width and
                self.x + self.width > player.x and
                self.y < player.y + player.height and
                self.y + self.height > player.y)

# Game class
class Game:
    def __init__(self):
        self.player = Player()
        self.objects = []
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.game_over = False
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move("left")
        if keys[pygame.K_RIGHT]:
            self.player.move("right")
        
        return True
    
    def update(self):
        if not self.game_over:
            # Add new falling objects randomly
            if random.randint(1, 30) == 1:
                self.objects.append(FallingObject())
            
            # Update falling objects
            for obj in self.objects[:]:
                if obj.fall():
                    self.objects.remove(obj)
                elif obj.collides_with(self.player):
                    self.objects.remove(obj)
                    self.score += 1
            
            # Check for game over condition (catching too many objects)
            if self.score >= 50:
                self.game_over = True
    
    def draw(self):
        screen.fill(WHITE)
        self.player.draw()
        
        for obj in self.objects:
            obj.draw()
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        
        # Draw game over message
        if self.game_over:
            game_over_text = self.font.render("Game Over! You Win!", True, BLACK)
            screen.blit(game_over_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2))
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            clock.tick(60)
        
        pygame.quit()
        sys.exit()

# Main function
if __name__ == "__main__":
    game = Game()
    game.run()