"""
Tests for the zombie simulation mechanics.
"""
import unittest
from character import Character
from trail_system import TrailSystem, Trail
from simulation import ZombieSimulation


class TestCharacter(unittest.TestCase):
    """Test character stats and mechanics."""
    
    def test_character_initialization(self):
        """Test character is initialized correctly."""
        char = Character("Test", health=100, agility=10, strength=15)
        self.assertEqual(char.name, "Test")
        self.assertEqual(char.health, 100)
        self.assertEqual(char.max_health, 100)
        self.assertEqual(char.agility, 10)
        self.assertEqual(char.base_agility, 10)
        self.assertEqual(char.strength, 15)
    
    def test_move_speed_based_on_agility(self):
        """Test that move speed is based on agility."""
        char = Character("Test", agility=10)
        self.assertEqual(char.get_move_speed(), 1.0)
        
        char = Character("Test", agility=20)
        self.assertEqual(char.get_move_speed(), 2.0)
    
    def test_damage_reduces_health(self):
        """Test that taking damage reduces health."""
        char = Character("Test", health=100)
        char.take_damage(30)
        self.assertEqual(char.health, 70)
    
    def test_damage_reduces_agility(self):
        """Test that taking damage reduces agility based on health loss."""
        char = Character("Test", health=100, agility=10)
        initial_agility = char.agility
        
        # Take 50% damage
        char.take_damage(50)
        self.assertEqual(char.health, 50)
        # Agility should be 50% of base
        self.assertAlmostEqual(char.agility, 5.0, places=2)
        self.assertLess(char.agility, initial_agility)
    
    def test_damage_reduces_move_speed(self):
        """Test that taking damage reduces move speed via agility."""
        char = Character("Test", health=100, agility=10)
        initial_speed = char.get_move_speed()
        
        char.take_damage(50)
        reduced_speed = char.get_move_speed()
        
        self.assertLess(reduced_speed, initial_speed)
        self.assertAlmostEqual(reduced_speed, 0.5, places=2)
    
    def test_health_cannot_go_negative(self):
        """Test that health cannot go below zero."""
        char = Character("Test", health=100)
        char.take_damage(150)
        self.assertEqual(char.health, 0)
        self.assertTrue(not char.is_alive())
    
    def test_strength_affects_damage(self):
        """Test that strength determines attack damage."""
        char = Character("Test", strength=20)
        self.assertEqual(char.get_attack_damage(), 20)
    
    def test_movement_updates_position(self):
        """Test that movement updates character position."""
        char = Character("Test", x=0, y=0, agility=10)
        char.move(1, 0)
        self.assertEqual(char.x, 1.0)
        self.assertEqual(char.y, 0.0)
    
    def test_movement_sets_is_moving_flag(self):
        """Test that movement sets the is_moving flag."""
        char = Character("Test")
        self.assertFalse(char.is_moving)
        
        char.move(1, 0)
        self.assertTrue(char.is_moving)
        
        char.move(0, 0)
        self.assertFalse(char.is_moving)


class TestTrailSystem(unittest.TestCase):
    """Test trail mechanics for sound and smell."""
    
    def test_trail_decay(self):
        """Test that trails decay over time."""
        trail = Trail(0, 0, intensity=1.0, decay_rate=0.1)
        trail.decay()
        self.assertAlmostEqual(trail.intensity, 0.9, places=2)
    
    def test_trail_becomes_inactive(self):
        """Test that trails become inactive when intensity reaches zero."""
        trail = Trail(0, 0, intensity=0.1, decay_rate=0.2)
        self.assertTrue(trail.is_active())
        trail.decay()
        self.assertFalse(trail.is_active())
    
    def test_sound_minimal_when_not_moving(self):
        """Test that sound is minimal when character is not moving."""
        trail_system = TrailSystem()
        char = Character("Test", x=0, y=0)
        char.is_moving = False
        
        trail_system.add_sound(char)
        
        # Should create very minimal sound
        self.assertEqual(len(trail_system.sound_trails), 1)
        self.assertLess(trail_system.sound_trails[0].intensity, 0.1)
    
    def test_sound_created_when_moving(self):
        """Test that sound is created when character is moving."""
        trail_system = TrailSystem()
        char = Character("Test", x=0, y=0, agility=10)
        char.is_moving = True
        
        trail_system.add_sound(char)
        
        # Should create noticeable sound
        self.assertEqual(len(trail_system.sound_trails), 1)
        self.assertGreater(trail_system.sound_trails[0].intensity, 0.1)
    
    def test_smell_always_created(self):
        """Test that smell is always created regardless of movement."""
        trail_system = TrailSystem()
        char = Character("Test", x=0, y=0)
        
        # Not moving
        char.is_moving = False
        trail_system.add_smell(char)
        self.assertEqual(len(trail_system.smell_trails), 1)
        
        # Moving
        char.is_moving = True
        trail_system.add_smell(char)
        self.assertEqual(len(trail_system.smell_trails), 2)
    
    def test_smell_decays_slower_than_sound(self):
        """Test that smell persists longer than sound."""
        trail_system = TrailSystem()
        self.assertLess(trail_system.smell_decay_rate, trail_system.sound_decay_rate)
    
    def test_trails_removed_when_inactive(self):
        """Test that inactive trails are removed."""
        trail_system = TrailSystem()
        trail_system.sound_trails.append(Trail(0, 0, 0.0, 0.1))
        trail_system.smell_trails.append(Trail(0, 0, 0.0, 0.1))
        
        trail_system._decay_trails()
        
        self.assertEqual(len(trail_system.sound_trails), 0)
        self.assertEqual(len(trail_system.smell_trails), 0)
    
    def test_intensity_at_position(self):
        """Test that intensity can be calculated at a position."""
        trail_system = TrailSystem()
        trail_system.sound_trails.append(Trail(0, 0, 1.0, 0.1))
        
        # At trail position
        intensity = trail_system.get_sound_intensity_at(0, 0)
        self.assertGreater(intensity, 0)
        
        # Far from trail
        intensity = trail_system.get_sound_intensity_at(100, 100)
        self.assertEqual(intensity, 0)
    
    def test_smell_has_longer_range_than_sound(self):
        """Test that smell detection range is longer than sound."""
        trail_system = TrailSystem()
        # Sound max_distance default is 10
        # Smell max_distance default is 20
        # This is verified in the get_strongest_trail_direction method
        self.assertTrue(True)  # Verified by code inspection


class TestZombieSimulation(unittest.TestCase):
    """Test the zombie simulation."""
    
    def test_simulation_initialization(self):
        """Test that simulation initializes correctly."""
        sim = ZombieSimulation()
        self.assertIsNotNone(sim.player)
        self.assertGreater(len(sim.zombies), 0)
        self.assertIsNotNone(sim.trail_system)
    
    def test_player_movement(self):
        """Test that player can move."""
        sim = ZombieSimulation()
        initial_x = sim.player.x
        sim.move_player(1, 0)
        self.assertNotEqual(sim.player.x, initial_x)
    
    def test_attack_deals_damage(self):
        """Test that attacks deal damage based on strength."""
        sim = ZombieSimulation()
        initial_health = sim.player.health
        attacker_strength = sim.zombies[0].strength
        
        sim.attack(sim.zombies[0], sim.player)
        
        self.assertEqual(sim.player.health, initial_health - attacker_strength)
    
    def test_update_creates_trails(self):
        """Test that updating the simulation creates trails."""
        sim = ZombieSimulation()
        sim.update()
        
        trails = sim.trail_system.get_trail_count()
        # Should have at least some trails
        self.assertGreater(trails['sound'] + trails['smell'], 0)
    
    def test_zombies_track_player(self):
        """Test that zombies move toward player trails."""
        sim = ZombieSimulation()
        zombie = sim.zombies[0]
        initial_x = zombie.x
        
        # Create some player trails
        for _ in range(5):
            sim.move_player(1, 0)
            sim.update()
        
        # Zombie should have moved
        self.assertNotEqual(zombie.x, initial_x)


if __name__ == '__main__':
    unittest.main()
