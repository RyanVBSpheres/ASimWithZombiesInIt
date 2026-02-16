using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;
using Microsoft.Xna.Framework.Input;
using System.Collections.Generic;

namespace ZombieGame;

/// <summary>
/// Represents the player character controlled by WASD
/// </summary>
public class Player
{
    public Vector2 Position { get; set; }
    public Vector2 Velocity { get; set; }
    public float Speed { get; set; } = 100f;
    public float Size { get; set; } = 20f;
    public Color Color { get; set; } = Color.Blue;
    
    private float soundEmissionTimer = 0f;
    private float smellEmissionTimer = 0f;
    
    public Player(Vector2 position)
    {
        Position = position;
    }

    public List<Stimulus> Update(float deltaTime, int screenWidth, int screenHeight)
    {
        var newStimuli = new List<Stimulus>();
        
        // Get keyboard state
        var keyState = Keyboard.GetState();
        
        // WASD movement
        Vector2 movement = Vector2.Zero;
        if (keyState.IsKeyDown(Keys.W)) movement.Y -= 1;
        if (keyState.IsKeyDown(Keys.S)) movement.Y += 1;
        if (keyState.IsKeyDown(Keys.A)) movement.X -= 1;
        if (keyState.IsKeyDown(Keys.D)) movement.X += 1;
        
        if (movement.Length() > 0)
        {
            movement.Normalize();
            Velocity = movement * Speed;
            
            // Moving creates sound
            soundEmissionTimer += deltaTime;
            if (soundEmissionTimer >= 0.5f) // Emit footstep sounds every 0.5 seconds
            {
                newStimuli.Add(new Stimulus(Position, 0.5f, StimulusType.Sound, 2f));
                soundEmissionTimer = 0f;
            }
        }
        else
        {
            Velocity = Vector2.Zero;
            soundEmissionTimer = 0f;
        }
        
        // Player always emits smell
        smellEmissionTimer += deltaTime;
        if (smellEmissionTimer >= 1f)
        {
            newStimuli.Add(new Stimulus(Position, 0.3f, StimulusType.Smell, 10f));
            smellEmissionTimer = 0f;
        }
        
        // Update position
        Position += Velocity * deltaTime;
        
        // Keep player in bounds
        Position = new Vector2(
            MathHelper.Clamp(Position.X, Size/2, screenWidth - Size/2),
            MathHelper.Clamp(Position.Y, Size/2, screenHeight - Size/2)
        );
        
        return newStimuli;
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
