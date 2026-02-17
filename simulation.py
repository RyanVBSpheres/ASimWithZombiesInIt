#!/usr/bin/env python3
"""
A Simulation with Zombies in It - Graphical Interface

A top-down zombie survival simulation with:
- Wandering zombies and creatures
- Controllable player
- Sound and smell emissions
- Trailing smells and sounds that fade with distance
"""

import pygame
import random
import math
from dataclasses import dataclass
from typing import List, Tuple

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (200, 0, 200)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)

# Game settings
PLAYER_SPEED = 3.0
ZOMBIE_SPEED = 1.5
CREATURE_SPEED = 2.0
SMELL_DECAY_RATE = 0.995
SOUND_DECAY_RATE = 0.92
SMELL_EMISSION_INTERVAL = 5  # frames
SOUND_THRESHOLD_DISTANCE = 30  # minimum distance moved to create sound


@dataclass
class Position:
    """Represents a 2D position"""
    x: float
    y: float
    
    def distance_to(self, other: 'Position') -> float:
        """Calculate distance to another position"""
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
    
    def copy(self) -> 'Position':
        """Create a copy of this position"""
        return Position(self.x, self.y)


class Smell:
    """Represents a smell in the environment that decays over time"""
    
    def __init__(self, x: float, y: float, intensity: float, color: Tuple[int, int, int]):
        self.position = Position(x, y)
        self.intensity = intensity
        self.color = color
    
    def update(self):
        """Decay the smell over time"""
        self.intensity *= SMELL_DECAY_RATE
    
    def is_alive(self) -> bool:
        """Check if smell is still significant"""
        return self.intensity > 0.1
    
    def draw(self, screen: pygame.Surface):
        """Draw the smell as a circle with transparency based on intensity"""
        if self.intensity > 0.1:
            radius = int(5 + self.intensity * 10)
            alpha = int(min(255, self.intensity * 50))
            color = (*self.color, alpha)
            
            # Create a surface for the smell
            smell_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(smell_surface, color, (radius, radius), radius)
            screen.blit(smell_surface, (int(self.position.x - radius), int(self.position.y - radius)))


class Sound:
    """Represents a sound that emanates from a position and fades with distance and time"""
    
    def __init__(self, x: float, y: float, intensity: float):
        self.position = Position(x, y)
        self.intensity = intensity
        self.initial_intensity = intensity
    
    def update(self):
        """Decay the sound over time"""
        self.intensity *= SOUND_DECAY_RATE
    
    def is_alive(self) -> bool:
        """Check if sound is still audible"""
        return self.intensity > 0.5
    
    def draw(self, screen: pygame.Surface):
        """Draw the sound as expanding rings"""
        if self.intensity > 0.5:
            # Calculate radius based on how much the sound has decayed
            decay_factor = self.intensity / self.initial_intensity
            max_radius = 50
            radius = int(max_radius * (1 - decay_factor))
            
            if radius > 0:
                alpha = int(min(255, self.intensity * 15))
                color = (*YELLOW, alpha)
                
                # Create a surface for the sound wave
                sound_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(sound_surface, color, (radius, radius), radius, 2)
                screen.blit(sound_surface, (int(self.position.x - radius), int(self.position.y - radius)))


class Entity:
    """Base class for all moving entities"""
    
    def __init__(self, x: float, y: float, speed: float, color: Tuple[int, int, int], smell_color: Tuple[int, int, int]):
        self.position = Position(x, y)
        self.last_position = self.position.copy()
        self.speed = speed
        self.color = color
        self.smell_color = smell_color
        self.size = 10
        self.frame_count = 0
        self.total_distance_moved = 0.0
    
    def move(self, dx: float, dy: float):
        """Move the entity by a delta amount"""
        self.last_position = self.position.copy()
        self.position.x += dx
        self.position.y += dy
        
        # Keep within bounds
        self.position.x = max(self.size, min(WINDOW_WIDTH - self.size, self.position.x))
        self.position.y = max(self.size, min(WINDOW_HEIGHT - self.size, self.position.y))
        
        # Track distance moved
        self.total_distance_moved += math.sqrt(dx * dx + dy * dy)
    
    def emit_smell(self) -> Smell:
        """Emit a smell at current position"""
        return Smell(self.position.x, self.position.y, 10.0, self.smell_color)
    
    def emit_sound(self) -> Sound:
        """Emit a sound at current position"""
        return Sound(self.position.x, self.position.y, 20.0)
    
    def should_emit_smell(self) -> bool:
        """Determine if entity should emit smell this frame"""
        return self.frame_count % SMELL_EMISSION_INTERVAL == 0
    
    def should_emit_sound(self) -> bool:
        """Determine if entity should emit sound based on movement"""
        if self.total_distance_moved >= SOUND_THRESHOLD_DISTANCE:
            self.total_distance_moved = 0
            return True
        return False
    
    def update(self):
        """Update entity state"""
        self.frame_count += 1
    
    def draw(self, screen: pygame.Surface):
        """Draw the entity"""
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), self.size)


class Player(Entity):
    """Player entity controlled by keyboard"""
    
    def __init__(self, x: float, y: float):
        super().__init__(x, y, PLAYER_SPEED, BLUE, CYAN)
        self.size = 12
    
    def handle_input(self, keys) -> Tuple[float, float]:
        """Handle keyboard input and return movement delta"""
        dx, dy = 0, 0
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += self.speed
        
        # Normalize diagonal movement
        if dx != 0 and dy != 0:
            factor = self.speed / math.sqrt(2)
            dx = factor if dx > 0 else -factor
            dy = factor if dy > 0 else -factor
        
        return dx, dy


class Zombie(Entity):
    """Zombie entity that wanders around"""
    
    def __init__(self, x: float, y: float):
        super().__init__(x, y, ZOMBIE_SPEED, RED, PURPLE)
        self.direction_change_timer = 0
        self.current_direction = random.uniform(0, 2 * math.pi)
        self.size = 10
    
    def wander(self) -> Tuple[float, float]:
        """Generate wandering movement"""
        self.direction_change_timer -= 1
        
        # Change direction periodically
        if self.direction_change_timer <= 0:
            self.direction_change_timer = random.randint(60, 180)
            self.current_direction = random.uniform(0, 2 * math.pi)
        
        dx = math.cos(self.current_direction) * self.speed
        dy = math.sin(self.current_direction) * self.speed
        
        return dx, dy


class Creature(Entity):
    """Other wandering creatures"""
    
    def __init__(self, x: float, y: float):
        super().__init__(x, y, CREATURE_SPEED, GREEN, ORANGE)
        self.direction_change_timer = 0
        self.current_direction = random.uniform(0, 2 * math.pi)
        self.size = 8
    
    def wander(self) -> Tuple[float, float]:
        """Generate wandering movement"""
        self.direction_change_timer -= 1
        
        # Change direction periodically (more frequently than zombies)
        if self.direction_change_timer <= 0:
            self.direction_change_timer = random.randint(30, 120)
            self.current_direction = random.uniform(0, 2 * math.pi)
        
        dx = math.cos(self.current_direction) * self.speed
        dy = math.sin(self.current_direction) * self.speed
        
        return dx, dy


class Game:
    """Main game class"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("A Sim with Zombies in It")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Initialize entities
        self.player = Player(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self.zombies: List[Zombie] = []
        self.creatures: List[Creature] = []
        
        # Initialize environmental effects
        self.smells: List[Smell] = []
        self.sounds: List[Sound] = []
        
        # Spawn zombies
        for _ in range(8):
            x = random.randint(50, WINDOW_WIDTH - 50)
            y = random.randint(50, WINDOW_HEIGHT - 50)
            self.zombies.append(Zombie(x, y))
        
        # Spawn creatures
        for _ in range(12):
            x = random.randint(50, WINDOW_WIDTH - 50)
            y = random.randint(50, WINDOW_HEIGHT - 50)
            self.creatures.append(Creature(x, y))
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def update(self):
        """Update game state"""
        # Handle player input
        keys = pygame.key.get_pressed()
        dx, dy = self.player.handle_input(keys)
        self.player.move(dx, dy)
        self.player.update()
        
        # Emit player smell and sound
        if self.player.should_emit_smell():
            self.smells.append(self.player.emit_smell())
        if self.player.should_emit_sound():
            self.sounds.append(self.player.emit_sound())
        
        # Update zombies
        for zombie in self.zombies:
            dx, dy = zombie.wander()
            zombie.move(dx, dy)
            zombie.update()
            
            # Emit zombie smell and sound
            if zombie.should_emit_smell():
                self.smells.append(zombie.emit_smell())
            if zombie.should_emit_sound():
                self.sounds.append(zombie.emit_sound())
        
        # Update creatures
        for creature in self.creatures:
            dx, dy = creature.wander()
            creature.move(dx, dy)
            creature.update()
            
            # Emit creature smell and sound
            if creature.should_emit_smell():
                self.smells.append(creature.emit_smell())
            if creature.should_emit_sound():
                self.sounds.append(creature.emit_sound())
        
        # Update and clean up smells
        for smell in self.smells:
            smell.update()
        self.smells = [smell for smell in self.smells if smell.is_alive()]
        
        # Update and clean up sounds
        for sound in self.sounds:
            sound.update()
        self.sounds = [sound for sound in self.sounds if sound.is_alive()]
    
    def draw(self):
        """Draw everything"""
        # Clear screen
        self.screen.fill(BLACK)
        
        # Draw smells (in background)
        for smell in self.smells:
            smell.draw(self.screen)
        
        # Draw sounds
        for sound in self.sounds:
            sound.draw(self.screen)
        
        # Draw entities
        for zombie in self.zombies:
            zombie.draw(self.screen)
        
        for creature in self.creatures:
            creature.draw(self.screen)
        
        self.player.draw(self.screen)
        
        # Draw UI
        font = pygame.font.Font(None, 24)
        text = font.render(f"Zombies: {len(self.zombies)} | Creatures: {len(self.creatures)} | Smells: {len(self.smells)} | Sounds: {len(self.sounds)}", True, WHITE)
        self.screen.blit(text, (10, 10))
        
        controls_text = font.render("Controls: Arrow Keys or WASD to move | ESC to quit", True, WHITE)
        self.screen.blit(controls_text, (10, WINDOW_HEIGHT - 30))
        
        # Update display
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()


def main():
    """Entry point"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
