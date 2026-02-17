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
SMELL_DECAY_RATE = 0.98  # Faster decay for performance
SOUND_DECAY_RATE = 0.85  # Faster decay for performance
SMELL_EMISSION_INTERVAL = 15  # frames - less frequent
SOUND_THRESHOLD_DISTANCE = 50  # minimum distance moved to create sound - less frequent
MAX_SMELLS = 300  # Cap for performance
MAX_SOUNDS = 50   # Cap for performance
ZOMBIE_DETECTION_RANGE = 200  # Range at which zombies detect player
ZOMBIE_SMELL_ATTRACTION = 100  # Range at which zombies follow smells
ZOMBIE_SOUND_ATTRACTION = 150  # Range at which zombies follow sounds
PLAYER_SMELL_ATTRACTION_MULTIPLIER = 1.5  # Zombies prefer player smell
MIN_SMELL_INTENSITY_FOR_ATTRACTION = 2.0  # Minimum intensity to attract zombies


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
        """Draw the smell as a small ring with transparency based on intensity"""
        if self.intensity > 0.1:
            radius = int(3 + self.intensity * 5)  # Smaller radius
            alpha = int(min(150, self.intensity * 30))  # Less opaque
            color = (*self.color, alpha)
            
            # Create a surface for the smell - draw as ring not filled circle
            smell_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(smell_surface, color, (radius, radius), radius, 1)  # Ring with width 1
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
            max_radius = 40  # Smaller max radius
            radius = int(max_radius * (1 - decay_factor))
            
            if radius > 0:
                alpha = int(min(200, self.intensity * 12))  # Less opaque
                color = (*YELLOW, alpha)
                
                # Create a surface for the sound wave
                sound_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(sound_surface, color, (radius, radius), radius, 1)  # Thinner ring
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
        # Health and agility attributes
        self.max_health = 100
        self.health = 100
        self.agility = 1.0  # Multiplier for speed
    
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
        """Draw the entity as a ring instead of filled circle"""
        # Draw ring
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), self.size, 2)
        
        # Draw health indicator (small bar above entity)
        if self.health < self.max_health:
            bar_width = self.size * 2
            bar_height = 3
            health_ratio = self.health / self.max_health
            
            # Background (red)
            pygame.draw.rect(screen, RED, 
                           (int(self.position.x - bar_width // 2), 
                            int(self.position.y - self.size - 8),
                            bar_width, bar_height))
            # Foreground (green)
            pygame.draw.rect(screen, GREEN, 
                           (int(self.position.x - bar_width // 2), 
                            int(self.position.y - self.size - 8),
                            int(bar_width * health_ratio), bar_height))


class Player(Entity):
    """Player entity controlled by keyboard"""
    
    def __init__(self, x: float, y: float):
        super().__init__(x, y, PLAYER_SPEED, BLUE, CYAN)
        self.size = 12
        self.agility = 1.2  # Player is more agile
    
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
    """Zombie entity that wanders around and reacts to stimuli"""
    
    def __init__(self, x: float, y: float):
        super().__init__(x, y, ZOMBIE_SPEED, RED, PURPLE)
        self.direction_change_timer = 0
        self.current_direction = random.uniform(0, 2 * math.pi)
        self.size = 10
        self.agility = 0.8  # Zombies are less agile
    
    def seek_target(self, target_pos: Position) -> Tuple[float, float]:
        """Move towards a target position"""
        dx = target_pos.x - self.position.x
        dy = target_pos.y - self.position.y
        dist = math.sqrt(dx * dx + dy * dy)
        
        if dist > 0:
            # Normalize and scale by speed
            dx = (dx / dist) * self.speed * self.agility
            dy = (dy / dist) * self.speed * self.agility
        
        return dx, dy
    
    def wander(self) -> Tuple[float, float]:
        """Generate wandering movement"""
        self.direction_change_timer -= 1
        
        # Change direction periodically
        if self.direction_change_timer <= 0:
            self.direction_change_timer = random.randint(60, 180)
            self.current_direction = random.uniform(0, 2 * math.pi)
        
        dx = math.cos(self.current_direction) * self.speed * self.agility
        dy = math.sin(self.current_direction) * self.speed * self.agility
        
        return dx, dy
    
    def update_behavior(self, player_pos: Position, smells: List[Smell], sounds: List[Sound]) -> Tuple[float, float]:
        """Update zombie behavior based on stimuli"""
        # Priority 1: Chase player if in detection range
        player_dist = self.position.distance_to(player_pos)
        if player_dist < ZOMBIE_DETECTION_RANGE:
            return self.seek_target(player_pos)
        
        # Priority 2: Follow nearby sounds
        nearest_sound = None
        nearest_sound_dist = ZOMBIE_SOUND_ATTRACTION
        for sound in sounds:
            dist = self.position.distance_to(sound.position)
            if dist < nearest_sound_dist:
                nearest_sound = sound
                nearest_sound_dist = dist
        
        if nearest_sound:
            return self.seek_target(nearest_sound.position)
        
        # Priority 3: Follow nearby smells (prefer player smell - cyan)
        nearest_smell = None
        nearest_smell_dist = ZOMBIE_SMELL_ATTRACTION
        for smell in smells:
            # Zombies are more attracted to player smell (cyan)
            attraction_range = ZOMBIE_SMELL_ATTRACTION * PLAYER_SMELL_ATTRACTION_MULTIPLIER if smell.color == CYAN else ZOMBIE_SMELL_ATTRACTION
            dist = self.position.distance_to(smell.position)
            if dist < attraction_range and smell.intensity > MIN_SMELL_INTENSITY_FOR_ATTRACTION:
                if dist < nearest_smell_dist:
                    nearest_smell = smell
                    nearest_smell_dist = dist
        
        if nearest_smell:
            return self.seek_target(nearest_smell.position)
        
        # Default: Wander
        return self.wander()


class Creature(Entity):
    """Other wandering creatures"""
    
    def __init__(self, x: float, y: float):
        super().__init__(x, y, CREATURE_SPEED, GREEN, ORANGE)
        self.direction_change_timer = 0
        self.current_direction = random.uniform(0, 2 * math.pi)
        self.size = 8
        self.agility = 1.3  # Creatures are more agile
    
    def wander(self) -> Tuple[float, float]:
        """Generate wandering movement"""
        self.direction_change_timer -= 1
        
        # Change direction periodically (more frequently than zombies)
        if self.direction_change_timer <= 0:
            self.direction_change_timer = random.randint(30, 120)
            self.current_direction = random.uniform(0, 2 * math.pi)
        
        dx = math.cos(self.current_direction) * self.speed * self.agility
        dy = math.sin(self.current_direction) * self.speed * self.agility
        
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
        
        # Emit player smell and sound (with cap check)
        if self.player.should_emit_smell() and len(self.smells) < MAX_SMELLS:
            self.smells.append(self.player.emit_smell())
        if self.player.should_emit_sound() and len(self.sounds) < MAX_SOUNDS:
            self.sounds.append(self.player.emit_sound())
        
        # Update zombies with stimulus-based behavior
        for zombie in self.zombies:
            dx, dy = zombie.update_behavior(self.player.position, self.smells, self.sounds)
            zombie.move(dx, dy)
            zombie.update()
            
            # Emit zombie smell and sound (with cap check)
            if zombie.should_emit_smell() and len(self.smells) < MAX_SMELLS:
                self.smells.append(zombie.emit_smell())
            if zombie.should_emit_sound() and len(self.sounds) < MAX_SOUNDS:
                self.sounds.append(zombie.emit_sound())
        
        # Update creatures
        for creature in self.creatures:
            dx, dy = creature.wander()
            creature.move(dx, dy)
            creature.update()
            
            # Emit creature smell and sound (with cap check)
            if creature.should_emit_smell() and len(self.smells) < MAX_SMELLS:
                self.smells.append(creature.emit_smell())
            if creature.should_emit_sound() and len(self.sounds) < MAX_SOUNDS:
                self.sounds.append(creature.emit_sound())
        
        # Update and clean up smells
        for smell in self.smells:
            smell.update()
        self.smells = [smell for smell in self.smells if smell.is_alive()]
        
        # Enforce cap on smells (remove oldest if over cap)
        if len(self.smells) > MAX_SMELLS:
            self.smells = self.smells[-MAX_SMELLS:]
        
        # Update and clean up sounds
        for sound in self.sounds:
            sound.update()
        self.sounds = [sound for sound in self.sounds if sound.is_alive()]
        
        # Enforce cap on sounds (remove oldest if over cap)
        if len(self.sounds) > MAX_SOUNDS:
            self.sounds = self.sounds[-MAX_SOUNDS:]
    
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
        
        # FPS and entity counts
        fps = int(self.clock.get_fps())
        text = font.render(f"FPS: {fps} | Zombies: {len(self.zombies)} | Creatures: {len(self.creatures)} | Smells: {len(self.smells)}/{MAX_SMELLS} | Sounds: {len(self.sounds)}/{MAX_SOUNDS}", True, WHITE)
        self.screen.blit(text, (10, 10))
        
        # Player stats
        player_stats = font.render(f"Player - Health: {int(self.player.health)} | Agility: {self.player.agility:.1f}", True, CYAN)
        self.screen.blit(player_stats, (10, 35))
        
        # Controls
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
