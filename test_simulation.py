"""
Tests for the Zombie Survival Simulation

Tests verify:
- Circular distance calculations
- Health system
- Eating behavior
- Entity representation
"""

import unittest
import math
from simulation import (
    distance, Player, Zombie, Animal, Entity,
    PLAYER_MAX_HEALTH, ZOMBIE_MAX_HEALTH, ANIMAL_MAX_HEALTH,
    EATING_DAMAGE, EATING_HEALTH_GAIN
)


class TestCircularDistance(unittest.TestCase):
    """Test that distance calculations are circular (Euclidean)."""
    
    def test_distance_calculation(self):
        """Test distance function uses Euclidean (circular) distance."""
        # Test basic distance
        self.assertEqual(distance((0, 0), (3, 4)), 5.0)
        self.assertEqual(distance((0, 0), (0, 0)), 0.0)
        
        # Test symmetry
        self.assertEqual(distance((1, 2), (4, 6)), distance((4, 6), (1, 2)))
        
        # Test diagonal distance (should be sqrt(2) * side, not 2*side as in square)
        dist = distance((0, 0), (1, 1))
        self.assertAlmostEqual(dist, math.sqrt(2), places=5)
        # If it were square distance, it would be 2
        self.assertNotEqual(dist, 2.0)


class TestEntityHealth(unittest.TestCase):
    """Test health system for all entities."""
    
    def test_player_health(self):
        """Test player has health system."""
        player = Player(100, 100)
        self.assertEqual(player.health, PLAYER_MAX_HEALTH)
        self.assertEqual(player.max_health, PLAYER_MAX_HEALTH)
        self.assertTrue(player.alive)
    
    def test_zombie_health(self):
        """Test zombie has health system."""
        zombie = Zombie(100, 100)
        self.assertEqual(zombie.health, ZOMBIE_MAX_HEALTH)
        self.assertEqual(zombie.max_health, ZOMBIE_MAX_HEALTH)
        self.assertTrue(zombie.alive)
    
    def test_animal_health(self):
        """Test animal has health system."""
        animal = Animal(100, 100)
        self.assertEqual(animal.health, ANIMAL_MAX_HEALTH)
        self.assertEqual(animal.max_health, ANIMAL_MAX_HEALTH)
        self.assertTrue(animal.alive)
    
    def test_take_damage(self):
        """Test entities can take damage."""
        entity = Entity(100, 100, 10, (255, 0, 0), 100)
        entity.take_damage(30)
        self.assertEqual(entity.health, 70)
        self.assertTrue(entity.alive)
    
    def test_death(self):
        """Test entities die when health reaches 0."""
        entity = Entity(100, 100, 10, (255, 0, 0), 100)
        entity.take_damage(100)
        self.assertEqual(entity.health, 0)
        self.assertFalse(entity.alive)
    
    def test_overkill_damage(self):
        """Test damage doesn't go below 0."""
        entity = Entity(100, 100, 10, (255, 0, 0), 100)
        entity.take_damage(150)
        self.assertEqual(entity.health, 0)
        self.assertFalse(entity.alive)
    
    def test_heal(self):
        """Test entities can heal."""
        entity = Entity(100, 100, 10, (255, 0, 0), 100)
        entity.take_damage(50)
        entity.heal(20)
        self.assertEqual(entity.health, 70)
    
    def test_heal_cap(self):
        """Test healing doesn't exceed max health."""
        entity = Entity(100, 100, 10, (255, 0, 0), 100)
        entity.take_damage(20)
        entity.heal(50)
        self.assertEqual(entity.health, 100)


class TestZombieEating(unittest.TestCase):
    """Test zombie eating behavior."""
    
    def test_zombie_eats_player(self):
        """Test zombie can eat player."""
        zombie = Zombie(100, 100)
        player = Player(100, 100)
        
        initial_player_health = player.health
        initial_zombie_health = zombie.health
        
        zombie.eat(player)
        
        self.assertEqual(player.health, initial_player_health - EATING_DAMAGE)
        self.assertEqual(zombie.health, min(initial_zombie_health + EATING_HEALTH_GAIN, 
                                           zombie.max_health))
    
    def test_zombie_eats_animal(self):
        """Test zombie can eat animal."""
        zombie = Zombie(100, 100)
        animal = Animal(100, 100)
        
        initial_animal_health = animal.health
        initial_zombie_health = zombie.health
        
        zombie.eat(animal)
        
        self.assertEqual(animal.health, initial_animal_health - EATING_DAMAGE)
        self.assertEqual(zombie.health, min(initial_zombie_health + EATING_HEALTH_GAIN, 
                                           zombie.max_health))
    
    def test_eating_kills_victim(self):
        """Test that eating enough times kills the victim."""
        zombie = Zombie(100, 100)
        animal = Animal(100, 100)
        
        # Eat until dead
        while animal.alive:
            zombie.eat(animal)
        
        self.assertEqual(animal.health, 0)
        self.assertFalse(animal.alive)
    
    def test_zombie_health_gain_capped(self):
        """Test zombie health gain is capped at max health."""
        zombie = Zombie(100, 100)
        # Zombie already at max health
        self.assertEqual(zombie.health, zombie.max_health)
        
        player = Player(100, 100)
        zombie.eat(player)
        
        # Zombie health should still be at max
        self.assertEqual(zombie.health, zombie.max_health)


class TestCircularAttractionRange(unittest.TestCase):
    """Test that sound and smell ranges are circular."""
    
    def test_player_has_circular_ranges(self):
        """Test player has sound and smell range attributes."""
        player = Player(100, 100)
        self.assertGreater(player.sound_range, 0)
        self.assertGreater(player.smell_range, 0)
    
    def test_animal_has_circular_ranges(self):
        """Test animal has sound and smell range attributes."""
        animal = Animal(100, 100)
        self.assertGreater(animal.sound_range, 0)
        self.assertGreater(animal.smell_range, 0)
    
    def test_zombie_detects_in_sound_range(self):
        """Test zombie detects entities within sound range using circular distance."""
        zombie = Zombie(100, 100)
        player = Player(100, 100)
        
        # Place player within sound range
        player.x = 100 + player.sound_range - 10
        player.y = 100
        
        zombie.find_target(player, [])
        
        # Zombie should detect player
        self.assertEqual(zombie.target, player)
    
    def test_zombie_detects_in_smell_range(self):
        """Test zombie detects entities within smell range using circular distance."""
        zombie = Zombie(100, 100)
        player = Player(100, 100)
        
        # Place player within smell range but outside previous position
        player.x = 100 + player.smell_range - 10
        player.y = 100
        
        zombie.find_target(player, [])
        
        # Zombie should detect player
        self.assertEqual(zombie.target, player)
    
    def test_zombie_ignores_out_of_range(self):
        """Test zombie doesn't detect entities outside both ranges."""
        zombie = Zombie(100, 100)
        player = Player(100, 100)
        
        # Place player far away (outside both ranges)
        player.x = 100 + player.sound_range + 100
        player.y = 100 + player.sound_range + 100
        
        zombie.find_target(player, [])
        
        # Zombie should not detect player
        self.assertIsNone(zombie.target)
    
    def test_circular_vs_square_detection(self):
        """Test that detection is circular, not square."""
        zombie = Zombie(100, 100)
        player = Player(100, 100)
        animal = Animal(100, 100)
        
        # Use a test range that we can control
        test_range = 80
        
        # Place player at diagonal distance
        # For a circle of radius R, diagonal corners of square would be at sqrt(2)*R
        # So we place player at diagonal just outside circle but inside square
        offset = test_range / math.sqrt(2) + 5
        player.x = 100 + offset
        player.y = 100 + offset
        
        # Temporarily set both ranges to test_range for this test
        original_sound_range = player.sound_range
        original_smell_range = player.smell_range
        player.sound_range = test_range
        player.smell_range = test_range
        
        dist = distance(zombie.get_pos(), player.get_pos())
        
        # Distance should be outside test range (circular)
        self.assertGreater(dist, test_range)
        
        # But would be inside square range
        self.assertLess(abs(player.x - zombie.x), test_range)
        self.assertLess(abs(player.y - zombie.y), test_range)
        
        zombie.find_target(player, [])
        
        # Zombie should NOT detect (circular detection)
        # If detection were square-based, zombie would detect player
        self.assertIsNone(zombie.target)
        
        # Restore original ranges
        player.sound_range = original_sound_range
        player.smell_range = original_smell_range


class TestEntityCircles(unittest.TestCase):
    """Test that entities are represented as circles."""
    
    def test_player_has_radius(self):
        """Test player has circular radius."""
        player = Player(100, 100)
        self.assertGreater(player.radius, 0)
    
    def test_zombie_has_radius(self):
        """Test zombie has circular radius."""
        zombie = Zombie(100, 100)
        self.assertGreater(zombie.radius, 0)
    
    def test_animal_has_radius(self):
        """Test animal has circular radius."""
        animal = Animal(100, 100)
        self.assertGreater(animal.radius, 0)


if __name__ == '__main__':
    unittest.main()
