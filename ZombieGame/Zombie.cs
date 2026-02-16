using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;
using System;
using System.Collections.Generic;

namespace ZombieGame;

/// <summary>
/// Represents a zombie entity with AI that is attracted to sounds and smells
/// </summary>
public class Zombie
{
    public Vector2 Position { get; set; }
    public Vector2 Velocity { get; set; }
    public float Speed { get; set; } = 30f;
    public float Size { get; set; } = 16f;
    public Color Color { get; set; } = Color.DarkGreen;
    
    private Vector2 wanderDirection;
    private float wanderTimer;
    private Random random;

    public Zombie(Vector2 position, Random random)
    {
        Position = position;
        this.random = random;
        wanderDirection = new Vector2(
            (float)(random.NextDouble() * 2 - 1),
            (float)(random.NextDouble() * 2 - 1)
        );
        if (wanderDirection.Length() > 0)
            wanderDirection.Normalize();
        wanderTimer = (float)random.NextDouble() * 3f;
    }

    public void Update(float deltaTime, List<Stimulus> stimuli)
    {
        // Find the strongest stimulus affecting this zombie
        Vector2 attractionForce = Vector2.Zero;
        float totalIntensity = 0f;

        foreach (var stimulus in stimuli)
        {
            float intensity = stimulus.GetIntensityAt(Position);
            if (intensity > 0.01f)
            {
                Vector2 direction = stimulus.Position - Position;
                if (direction.Length() > 0)
                {
                    direction.Normalize();
                    // Sounds are more immediately attractive than smells
                    float multiplier = stimulus.Type == StimulusType.Sound ? 1.5f : 1.0f;
                    attractionForce += direction * intensity * multiplier;
                    totalIntensity += intensity * multiplier;
                }
            }
        }

        Vector2 targetVelocity;
        
        if (totalIntensity > 0.1f)
        {
            // Move towards stimuli
            attractionForce.Normalize();
            targetVelocity = attractionForce * Speed;
        }
        else
        {
            // Wander when no strong stimuli
            wanderTimer -= deltaTime;
            if (wanderTimer <= 0)
            {
                wanderDirection = new Vector2(
                    (float)(random.NextDouble() * 2 - 1),
                    (float)(random.NextDouble() * 2 - 1)
                );
                if (wanderDirection.Length() > 0)
                    wanderDirection.Normalize();
                wanderTimer = (float)random.NextDouble() * 3f + 2f;
            }
            targetVelocity = wanderDirection * Speed * 0.3f;
        }

        // Smooth velocity transition
        Velocity = Vector2.Lerp(Velocity, targetVelocity, 0.1f);
        Position += Velocity * deltaTime;
    }

    public void Draw(SpriteBatch spriteBatch, Texture2D pixel)
    {
        Rectangle rect = new Rectangle(
            (int)(Position.X - Size / 2),
            (int)(Position.Y - Size / 2),
            (int)Size,
            (int)Size
        );
        spriteBatch.Draw(pixel, rect, Color);
    }
}
