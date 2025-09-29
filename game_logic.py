import pygame
import random
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLUE, RED, GREEN, YELLOW, BLACK, PURPLE
from player import Player
from falling_object import FallingObject
from particle import Particle

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
    
    def draw(self, screen):
        if self.game_state == "start":
            self.draw_start_screen(screen)
        elif self.game_state == "game_over":
            self.draw_game_over_screen(screen)
        else:  # playing
            self.draw_gameplay(screen)
        
        pygame.display.flip()
    
    def run(self, screen, clock):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw(screen)
            clock.tick(60)
        
        pygame.quit()
        sys.exit()