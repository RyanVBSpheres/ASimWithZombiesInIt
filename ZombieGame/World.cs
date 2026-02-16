using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;
using System;
using System.Collections.Generic;

namespace ZombieGame;

/// <summary>
/// Represents an environmental object in the apocalypse world
/// </summary>
public class WorldObject
{
    public Vector2 Position { get; set; }
    public Vector2 Size { get; set; }
    public Color Color { get; set; }
    public string Type { get; set; }

    public WorldObject(Vector2 position, Vector2 size, Color color, string type)
    {
        Position = position;
        Size = size;
        Color = color;
        Type = type;
    }

    public void Draw(SpriteBatch spriteBatch, Texture2D pixel)
    {
        Rectangle rect = new Rectangle(
            (int)(Position.X - Size.X / 2),
            (int)(Position.Y - Size.Y / 2),
            (int)Size.X,
            (int)Size.Y
        );
        spriteBatch.Draw(pixel, rect, Color);
    }
}

/// <summary>
/// Manages the game world with various environmental objects
/// </summary>
public class World
{
    private List<WorldObject> objects;
    private Random random;

    public World(int width, int height, Random random)
    {
        this.random = random;
        objects = new List<WorldObject>();
        GenerateWorld(width, height);
    }

    private void GenerateWorld(int width, int height)
    {
        // Add some trees (nature elements)
        for (int i = 0; i < 15; i++)
        {
            Vector2 pos = new Vector2(
                random.Next(50, width - 50),
                random.Next(50, height - 50)
            );
            Vector2 size = new Vector2(
                random.Next(20, 40),
                random.Next(30, 50)
            );
            objects.Add(new WorldObject(pos, size, new Color(34, 139, 34), "Tree"));
        }

        // Add some rocks
        for (int i = 0; i < 10; i++)
        {
            Vector2 pos = new Vector2(
                random.Next(50, width - 50),
                random.Next(50, height - 50)
            );
            Vector2 size = new Vector2(
                random.Next(15, 30),
                random.Next(15, 30)
            );
            objects.Add(new WorldObject(pos, size, Color.Gray, "Rock"));
        }

        // Add ruined buildings
        for (int i = 0; i < 5; i++)
        {
            Vector2 pos = new Vector2(
                random.Next(100, width - 100),
                random.Next(100, height - 100)
            );
            Vector2 size = new Vector2(
                random.Next(60, 120),
                random.Next(60, 100)
            );
            objects.Add(new WorldObject(pos, size, new Color(139, 69, 19), "Ruin"));
        }

        // Add abandoned cars
        for (int i = 0; i < 8; i++)
        {
            Vector2 pos = new Vector2(
                random.Next(50, width - 50),
                random.Next(50, height - 50)
            );
            Vector2 size = new Vector2(
                random.Next(40, 50),
                random.Next(25, 35)
            );
            objects.Add(new WorldObject(pos, size, new Color(105, 105, 105), "Car"));
        }
    }

    public void Draw(SpriteBatch spriteBatch, Texture2D pixel)
    {
        foreach (var obj in objects)
        {
            obj.Draw(spriteBatch, pixel);
        }
    }
}
