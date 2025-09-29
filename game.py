import pygame
import random
import sys
import math

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SIZE = 50
OBJECT_SIZE = 30
PLAYER_SPEED = 5
OBJECT_SPEED = 3
WHITE = (255, 255, 255)
BLUE = (0, 120, 255)
RED = (255, 50, 50)
GREEN = (50, 200, 50)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
PURPLE = (180, 0, 255)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Upgraded Catch Game")
clock = pygame.time.Clock()

# Particle class for effects
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(2, 5)
        self.speed_x = random.randint(-3, 3)
        self.speed_y = random.randint(-3, 3)
        self.life = 30
    
    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.life -= 1
        self.size = max(0, self.size - 0.1)
        return self.life > 0
    
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.size))

# Player class
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

# Falling object class
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

# Game class
class Game:
    def __init__(self):
        self.player = Player()
        self.objects = []
        self.particles = []
        self.score = 0
        self.level = 1
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        self.game_state = "start"  # start, playing, game_over
        self.spawn_timer = 0
        self.spawn_delay = 60  # frames between spawns
    
    def spawn_object(self):
        # Determine object type based on probability
        rand = random.random()
        if rand < 0.7:
            obj_type = "normal"
        elif rand < 0.85:
            obj_type = "bonus"
        elif rand < 0.95:
            obj_type = "life"
        else:
            obj_type = "bomb"
        
        self.objects.append(FallingObject(obj_type))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if self.game_state == "start" and event.key == pygame.K_SPACE:
                    self.game_state = "playing"
                elif self.game_state == "game_over" and event.key == pygame.K_r:
                    self.__init__()  # Reset game
                    self.game_state = "playing"
        
        if self.game_state == "playing":
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.move("left")
            if keys[pygame.K_RIGHT]:
                self.player.move("right")
        
        return True
    
    def update_particles(self):
        for particle in self.particles[:]:
            if not particle.update():
                self.particles.remove(particle)
    
    def update(self):
        if self.game_state == "playing":
            # Level progression
            self.level = 1 + self.score // 10
            
            # Spawn objects
            self.spawn_timer += 1
            if self.spawn_timer >= self.spawn_delay:
                self.spawn_object()
                self.spawn_timer = 0
                # Increase spawn rate with level
                self.spawn_delay = max(10, 60 - self.level * 2)
            
            # Update falling objects
            for obj in self.objects[:]:
                if obj.fall():
                    self.objects.remove(obj)
                    # Only lose life if it's not a bomb
                    if obj.type != "bomb":
                        self.player.lives -= 1
                        if self.player.lives <= 0:
                            self.game_state = "game_over"
                elif obj.collides_with(self.player):
                    self.objects.remove(obj)
                    
                    # Handle different object types
                    if obj.type == "bomb":
                        self.player.lives -= 1
                        if self.player.lives <= 0:
                            self.game_state = "game_over"
                        # Create explosion particles
                        for _ in range(30):
                            self.particles.append(Particle(
                                obj.x + obj.width//2, 
                                obj.y + obj.height//2, 
                                RED
                            ))
                    else:
                        self.score += obj.points
                        # Add life for life objects
                        if obj.type == "life":
                            self.player.lives = min(5, self.player.lives + 1)
                        
                        # Create collection particles
                        for _ in range(15):
                            self.particles.append(Particle(
                                obj.x + obj.width//2, 
                                obj.y + obj.height//2, 
                                obj.color
                            ))
            
            # Update particles
            self.update_particles()
    
    def draw_start_screen(self, surface):
        surface.fill(WHITE)
        
        # Title
        title = self.big_font.render("UPGRADED CATCH GAME", True, BLUE)
        surface.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 150))
        
        # Instructions
        instructions = self.font.render("Use LEFT and RIGHT arrows to move", True, BLACK)
        surface.blit(instructions, (SCREEN_WIDTH//2 - instructions.get_width()//2, 250))
        
        start_text = self.font.render("Press SPACE to start", True, GREEN)
        surface.blit(start_text, (SCREEN_WIDTH//2 - start_text.get_width()//2, 300))
        
        # Object descriptions
        obj_desc = [
            "Red Circle: Normal object (+1 point)",
            "Green Diamond: Bonus object (+5 points)",
            "Yellow Oval: Extra life",
            "Purple Square: Bomb (lose life)"
        ]
        
        for i, desc in enumerate(obj_desc):
            text = self.font.render(desc, True, BLACK)
            surface.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 350 + i*30))
    
    def draw_game_over_screen(self, surface):
        surface.fill(WHITE)
        
        # Game over text
        game_over = self.big_font.render("GAME OVER", True, RED)
        surface.blit(game_over, (SCREEN_WIDTH//2 - game_over.get_width()//2, 150))
        
        # Final score
        score_text = self.font.render(f"Final Score: {self.score}", True, BLACK)
        surface.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, 250))
        
        level_text = self.font.render(f"Level Reached: {self.level}", True, BLACK)
        surface.blit(level_text, (SCREEN_WIDTH//2 - level_text.get_width()//2, 290))
        
        # Restart instructions
        restart_text = self.font.render("Press R to restart", True, GREEN)
        surface.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, 350))
    
    def draw_gameplay(self, surface):
        surface.fill(WHITE)
        self.player.draw(surface)
        
        for obj in self.objects:
            obj.draw(surface)
        
        for particle in self.particles:
            particle.draw(surface)
        
        # Draw UI
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        surface.blit(score_text, (10, 10))
        
        level_text = self.font.render(f"Level: {self.level}", True, BLACK)
        surface.blit(level_text, (10, 50))
        
        lives_text = self.font.render(f"Lives: {self.player.lives}", True, BLACK)
        surface.blit(lives_text, (10, 90))
        
        # Draw object legend
        legend_y = SCREEN_HEIGHT - 40
        pygame.draw.circle(surface, RED, (30, legend_y), 10)
        surface.blit(self.font.render(":1 pt", True, BLACK), (45, legend_y - 10))
        
        pygame.draw.polygon(surface, GREEN, [(90, legend_y-10), (100, legend_y), (90, legend_y+10), (80, legend_y)])
        surface.blit(self.font.render(":5 pts", True, BLACK), (110, legend_y - 10))
        
        pygame.draw.ellipse(surface, YELLOW, (160, legend_y-8, 16, 16))
        surface.blit(self.font.render(":Life", True, BLACK), (185, legend_y - 10))
        
        pygame.draw.rect(surface, PURPLE, (240, legend_y-8, 16, 16), border_radius=5)
        surface.blit(self.font.render(":Bomb", True, BLACK), (265, legend_y - 10))
    
    def draw(self):
        if self.game_state == "start":
            self.draw_start_screen(screen)
        elif self.game_state == "game_over":
            self.draw_game_over_screen(screen)
        else:  # playing
            self.draw_gameplay(screen)
        
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
