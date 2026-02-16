"""
A Top Down Zombie Survival Simulation

Features:
- Circular sound and smell emanation
- Circular entity representations
- Animals that attract zombies with sounds and smells
- Health system for all sentient characters
- Eating behavior for zombies
"""

import pygame
import math
import random
from typing import List, Tuple, Optional

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BROWN = (139, 69, 19)
GRAY = (128, 128, 128)
LIGHT_RED = (255, 100, 100)
LIGHT_YELLOW = (255, 255, 150)

# Entity constants
PLAYER_RADIUS = 10
ZOMBIE_RADIUS = 8
ANIMAL_RADIUS = 6

# Sound and smell ranges (circular)
PLAYER_SOUND_RANGE = 150
PLAYER_SMELL_RANGE = 100
ANIMAL_SOUND_RANGE = 120
ANIMAL_SMELL_RANGE = 80

# Health constants
PLAYER_MAX_HEALTH = 100
ZOMBIE_MAX_HEALTH = 80
ANIMAL_MAX_HEALTH = 50

# Behavior constants
ZOMBIE_EATING_RANGE = 15
EATING_DAMAGE = 5
EATING_HEALTH_GAIN = 3
ZOMBIE_SPEED = 1.5
PLAYER_SPEED = 3
ANIMAL_SPEED = 2


def distance(pos1: Tuple[float, float], pos2: Tuple[float, float]) -> float:
    """Calculate Euclidean distance between two points (circular distance)."""
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)


class Entity:
    """Base class for all entities in the simulation."""
    
    def __init__(self, x: float, y: float, radius: float, color: Tuple[int, int, int], max_health: int):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.max_health = max_health
        self.health = max_health
        self.alive = True
    
    def get_pos(self) -> Tuple[float, float]:
        """Get current position."""
        return (self.x, self.y)
    
    def take_damage(self, damage: int):
        """Take damage and update health."""
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.alive = False
    
    def heal(self, amount: int):
        """Heal health up to max."""
        self.health = min(self.health + amount, self.max_health)
    
    def draw(self, screen: pygame.Surface):
        """Draw the entity as a circle."""
        if self.alive:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
            # Draw health bar above entity
            self.draw_health_bar(screen)
    
    def draw_health_bar(self, screen: pygame.Surface):
        """Draw health bar above the entity."""
        bar_width = self.radius * 2
        bar_height = 3
        bar_x = self.x - self.radius
        bar_y = self.y - self.radius - 5
        
        # Background (red)
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
        # Foreground (green)
        health_width = (self.health / self.max_health) * bar_width
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, health_width, bar_height))


class Player(Entity):
    """Player character that emanates sound and smell in circles."""
    
    def __init__(self, x: float, y: float):
        super().__init__(x, y, PLAYER_RADIUS, BLUE, PLAYER_MAX_HEALTH)
        self.sound_range = PLAYER_SOUND_RANGE
        self.smell_range = PLAYER_SMELL_RANGE
        self.speed = PLAYER_SPEED
    
    def move(self, dx: float, dy: float):
        """Move the player."""
        if self.alive:
            self.x += dx * self.speed
            self.y += dy * self.speed
            
            # Keep within bounds
            self.x = max(self.radius, min(SCREEN_WIDTH - self.radius, self.x))
            self.y = max(self.radius, min(SCREEN_HEIGHT - self.radius, self.y))
    
    def draw(self, screen: pygame.Surface, show_ranges: bool = True):
        """Draw the player and optionally their sound/smell ranges."""
        if self.alive:
            if show_ranges:
                # Draw smell range (inner circle)
                pygame.draw.circle(screen, LIGHT_YELLOW, (int(self.x), int(self.y)), 
                                 int(self.smell_range), 1)
                # Draw sound range (outer circle)
                pygame.draw.circle(screen, LIGHT_RED, (int(self.x), int(self.y)), 
                                 int(self.sound_range), 1)
            
            super().draw(screen)


class Animal(Entity):
    """Animal NPC that makes sounds and smells that attract zombies."""
    
    def __init__(self, x: float, y: float):
        super().__init__(x, y, ANIMAL_RADIUS, BROWN, ANIMAL_MAX_HEALTH)
        self.sound_range = ANIMAL_SOUND_RANGE
        self.smell_range = ANIMAL_SMELL_RANGE
        self.speed = ANIMAL_SPEED
        self.wander_timer = 0
        self.wander_direction = random.uniform(0, 2 * math.pi)
    
    def update(self):
        """Update animal behavior (random wandering)."""
        if self.alive:
            self.wander_timer -= 1
            if self.wander_timer <= 0:
                # Change direction
                self.wander_direction = random.uniform(0, 2 * math.pi)
                self.wander_timer = random.randint(30, 120)
            
            # Move in current direction
            dx = math.cos(self.wander_direction)
            dy = math.sin(self.wander_direction)
            
            self.x += dx * self.speed
            self.y += dy * self.speed
            
            # Keep within bounds (bounce off walls)
            if self.x <= self.radius or self.x >= SCREEN_WIDTH - self.radius:
                self.wander_direction = math.pi - self.wander_direction
                self.x = max(self.radius, min(SCREEN_WIDTH - self.radius, self.x))
            if self.y <= self.radius or self.y >= SCREEN_HEIGHT - self.radius:
                self.wander_direction = -self.wander_direction
                self.y = max(self.radius, min(SCREEN_HEIGHT - self.radius, self.y))


class Zombie(Entity):
    """Zombie that is attracted to sounds and smells, and eats players/animals."""
    
    def __init__(self, x: float, y: float):
        super().__init__(x, y, ZOMBIE_RADIUS, GREEN, ZOMBIE_MAX_HEALTH)
        self.speed = ZOMBIE_SPEED
        self.eating_range = ZOMBIE_EATING_RANGE
        self.target: Optional[Entity] = None
        self.eating_cooldown = 0
    
    def find_target(self, player: Player, animals: List[Animal]):
        """Find the closest target within sound/smell range using circular distance."""
        if not self.alive:
            return
        
        closest_target = None
        closest_distance = float('inf')
        
        # Check player
        if player.alive:
            dist = distance(self.get_pos(), player.get_pos())
            # Check if within player's sound or smell range (circular detection)
            if dist <= player.sound_range or dist <= player.smell_range:
                if dist < closest_distance:
                    closest_distance = dist
                    closest_target = player
        
        # Check animals
        for animal in animals:
            if animal.alive:
                dist = distance(self.get_pos(), animal.get_pos())
                # Check if within animal's sound or smell range (circular detection)
                if dist <= animal.sound_range or dist <= animal.smell_range:
                    if dist < closest_distance:
                        closest_distance = dist
                        closest_target = animal
        
        self.target = closest_target
    
    def update(self, player: Player, animals: List[Animal]):
        """Update zombie behavior."""
        if not self.alive:
            return
        
        # Update cooldowns
        if self.eating_cooldown > 0:
            self.eating_cooldown -= 1
        
        # Find and move toward target
        self.find_target(player, animals)
        
        if self.target and self.target.alive:
            # Move toward target
            target_pos = self.target.get_pos()
            dx = target_pos[0] - self.x
            dy = target_pos[1] - self.y
            dist = math.sqrt(dx**2 + dy**2)
            
            if dist > 0:
                # Check if close enough to eat
                if dist <= self.eating_range:
                    # Eat the target
                    if self.eating_cooldown == 0:
                        self.eat(self.target)
                        self.eating_cooldown = 30  # Eat once per second (at 60 FPS)
                else:
                    # Move toward target
                    dx /= dist
                    dy /= dist
                    self.x += dx * self.speed
                    self.y += dy * self.speed
    
    def eat(self, victim: Entity):
        """Eat a victim, reducing their health and increasing zombie's health."""
        if victim.alive:
            victim.take_damage(EATING_DAMAGE)
            self.heal(EATING_HEALTH_GAIN)


class Simulation:
    """Main simulation class."""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Zombie Survival Simulation")
        self.clock = pygame.time.Clock()
        self.running = True
        self.show_ranges = True
        
        # Create entities
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.zombies: List[Zombie] = []
        self.animals: List[Animal] = []
        
        # Spawn initial zombies
        for _ in range(5):
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 50)
            self.zombies.append(Zombie(x, y))
        
        # Spawn initial animals
        for _ in range(8):
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 50)
            self.animals.append(Animal(x, y))
    
    def handle_input(self):
        """Handle user input."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r:
                    # Toggle range display
                    self.show_ranges = not self.show_ranges
        
        # Handle movement
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += 1
        
        self.player.move(dx, dy)
    
    def update(self):
        """Update all entities."""
        # Update animals
        for animal in self.animals:
            animal.update()
        
        # Update zombies
        for zombie in self.zombies:
            zombie.update(self.player, self.animals)
    
    def draw(self):
        """Draw everything."""
        self.screen.fill(BLACK)
        
        # Draw player with ranges
        self.player.draw(self.screen, self.show_ranges)
        
        # Draw animals
        for animal in self.animals:
            animal.draw(self.screen)
        
        # Draw zombies
        for zombie in self.zombies:
            zombie.draw(self.screen)
        
        # Draw UI
        self.draw_ui()
        
        pygame.display.flip()
    
    def draw_ui(self):
        """Draw UI elements."""
        font = pygame.font.Font(None, 24)
        
        # Player health
        health_text = font.render(f"Player Health: {self.player.health}/{self.player.max_health}", 
                                 True, WHITE)
        self.screen.blit(health_text, (10, 10))
        
        # Alive counts
        alive_zombies = sum(1 for z in self.zombies if z.alive)
        alive_animals = sum(1 for a in self.animals if a.alive)
        
        count_text = font.render(f"Zombies: {alive_zombies} | Animals: {alive_animals}", 
                                True, WHITE)
        self.screen.blit(count_text, (10, 35))
        
        # Instructions
        if self.show_ranges:
            info_text = font.render("Press R to hide ranges | WASD/Arrows to move | ESC to quit", 
                                   True, GRAY)
        else:
            info_text = font.render("Press R to show ranges | WASD/Arrows to move | ESC to quit", 
                                   True, GRAY)
        self.screen.blit(info_text, (10, SCREEN_HEIGHT - 30))
        
        # Game over
        if not self.player.alive:
            game_over_text = font.render("GAME OVER - You were eaten!", True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(game_over_text, text_rect)
    
    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()


if __name__ == "__main__":
    sim = Simulation()
    sim.run()
