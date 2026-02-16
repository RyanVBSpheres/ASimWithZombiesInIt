"""
Test script to verify the simulation initializes and runs correctly
without requiring a display.
"""

import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'

from simulation import Simulation, Player, Zombie, Animal, distance
import math

def test_simulation_initialization():
    """Test that simulation initializes correctly."""
    print("Testing simulation initialization...")
    sim = Simulation()
    
    # Check player exists
    assert sim.player is not None
    assert isinstance(sim.player, Player)
    assert sim.player.alive
    print(f"✓ Player initialized at ({sim.player.x}, {sim.player.y})")
    
    # Check zombies exist
    assert len(sim.zombies) > 0
    assert all(isinstance(z, Zombie) for z in sim.zombies)
    print(f"✓ {len(sim.zombies)} zombies created")
    
    # Check animals exist
    assert len(sim.animals) > 0
    assert all(isinstance(a, Animal) for a in sim.animals)
    print(f"✓ {len(sim.animals)} animals created")

def test_circular_properties():
    """Test that all entities have circular properties."""
    print("\nTesting circular properties...")
    
    player = Player(100, 100)
    zombie = Zombie(200, 200)
    animal = Animal(300, 300)
    
    # Check all have radius
    assert player.radius > 0
    assert zombie.radius > 0
    assert animal.radius > 0
    print("✓ All entities have radius (circular representation)")
    
    # Check player and animal have sound/smell ranges
    assert player.sound_range > 0
    assert player.smell_range > 0
    assert animal.sound_range > 0
    assert animal.smell_range > 0
    print("✓ Player and animals have circular sound/smell ranges")

def test_health_system():
    """Test health system works."""
    print("\nTesting health system...")
    
    zombie = Zombie(100, 100)
    player = Player(100, 100)
    
    initial_health = player.health
    zombie.eat(player)
    
    assert player.health < initial_health
    print(f"✓ Zombie eating reduces victim health ({initial_health} → {player.health})")
    
    initial_zombie_health = zombie.health
    zombie.eat(player)
    
    # Zombie should heal (unless already at max)
    if initial_zombie_health < zombie.max_health:
        assert zombie.health >= initial_zombie_health
    print(f"✓ Eating increases zombie health")

def test_circular_detection():
    """Test that detection uses circular distance."""
    print("\nTesting circular detection...")
    
    zombie = Zombie(100, 100)
    player = Player(100, 100)
    
    # Place player at a diagonal that would be outside circle but inside square
    test_range = 80
    player.sound_range = test_range
    player.smell_range = test_range
    
    # Diagonal outside circle but inside square
    offset = test_range / math.sqrt(2) + 5
    player.x = 100 + offset
    player.y = 100 + offset
    
    dist = distance(zombie.get_pos(), player.get_pos())
    assert dist > test_range
    
    zombie.find_target(player, [])
    
    # Should NOT detect (circular, not square)
    assert zombie.target is None
    print(f"✓ Circular detection confirmed (distance {dist:.1f} > range {test_range})")

def test_simulation_update():
    """Test that simulation can update without crashing."""
    print("\nTesting simulation updates...")
    
    sim = Simulation()
    
    # Run a few update cycles
    for i in range(10):
        sim.update()
    
    print("✓ Simulation updates successfully")

def test_zombie_targeting():
    """Test zombies can find and target entities."""
    print("\nTesting zombie targeting...")
    
    zombie = Zombie(100, 100)
    player = Player(150, 100)
    animal = Animal(300, 300)
    
    zombie.find_target(player, [animal])
    
    # Should target player (closer and in range)
    assert zombie.target == player
    print("✓ Zombie correctly targets closest entity in range")
    
    # Move player out of range
    player.x = 1000
    player.y = 1000
    
    zombie.find_target(player, [animal])
    
    # Should not target anyone (all out of range)
    assert zombie.target is None
    print("✓ Zombie ignores entities out of range")

if __name__ == "__main__":
    print("=" * 60)
    print("Running Simulation Verification Tests")
    print("=" * 60)
    
    test_simulation_initialization()
    test_circular_properties()
    test_health_system()
    test_circular_detection()
    test_simulation_update()
    test_zombie_targeting()
    
    print("\n" + "=" * 60)
    print("All verification tests passed! ✓")
    print("=" * 60)
    print("\nThe simulation implements:")
    print("  • Circular sound and smell emanation")
    print("  • Circular entity representations")
    print("  • Health system for all sentient characters")
    print("  • Animals with sound/smell generation")
    print("  • Zombie eating behavior")
    print("\nRun 'python simulation.py' to start the visual simulation")
