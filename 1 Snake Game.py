#Snake_Game_by_RAZ
import tkinter as tk
import random

# Initialize the main window
root = tk.Tk()
root.title("Snake Game (RAZ)")

# Game configuration
GAME_WIDTH = 500
GAME_HEIGHT = 500
CELL_SIZE = 20
SNAKE_COLORS = ["#6B8E23", "#FF6347", "#4682B4", "#FFD700", "#8A2BE2"]  # List of colors for the snake
FOOD_COLORS = ["red", "blue", "yellow", "green", "purple", "orange"]  # List of random food colors
BG_COLOR = "black"

# Initialize game variables
snake = [(100, 100), (80, 100), (60, 100)]  # Initial snake position
snake_direction = "Right"
food_position = (200, 200)
score = 0
speed = 70  # Initial speed in milliseconds
current_snake_color = SNAKE_COLORS[0]  # Start with the first color
current_food_color = random.choice(FOOD_COLORS)  # Start with a random food color

# Create canvas
canvas = tk.Canvas(root, width=GAME_WIDTH, height=GAME_HEIGHT, bg=BG_COLOR)
canvas.pack()

# Draw the snake
def draw_snake():
    canvas.delete("snake")
    for segment in snake:
        x, y = segment
        canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE, fill=current_snake_color, outline="black", tags="snake")

# Draw the food with a random color
def draw_food():
    global current_food_color
    canvas.delete("food")
    x, y = food_position
    current_food_color = random.choice(FOOD_COLORS)  # Select a random color for the food
    canvas.create_oval(x, y, x + CELL_SIZE, y + CELL_SIZE, fill=current_food_color, tags="food")

# Move the snake
def move_snake():
    global snake, food_position, score, speed, current_snake_color

    # Calculate new head position
    head_x, head_y = snake[0]
    if snake_direction == "Up":
        head_y -= CELL_SIZE
    elif snake_direction == "Down":
        head_y += CELL_SIZE
    elif snake_direction == "Left":
        head_x -= CELL_SIZE
    elif snake_direction == "Right":
        head_x += CELL_SIZE

    # Wrap around the screen
    head_x %= GAME_WIDTH
    head_y %= GAME_HEIGHT

    new_head = (head_x, head_y)

    # Check if the snake collides with itself
    if new_head in snake:
        game_over()
        return

    # Check if the snake eats the food
    if new_head == food_position:
        snake.insert(0, new_head)
        score += 1
        food_position = generate_food()
        # Change the snake's color
        current_snake_color = random.choice(SNAKE_COLORS)
        # Increase speed as the score increases
        if speed > 50:
            speed -= 2
    else:
        snake.insert(0, new_head)
        snake.pop()

    # Redraw the snake and food
    draw_snake()
    draw_food()

    # Schedule the next move
    root.after(speed, move_snake)

# Change the direction of the snake
def change_direction(new_direction):
    global snake_direction
    # Prevent the snake from reversing
    if (
        (new_direction == "Up" and snake_direction != "Down") or
        (new_direction == "Down" and snake_direction != "Up") or
        (new_direction == "Left" and snake_direction != "Right") or
        (new_direction == "Right" and snake_direction != "Left")
    ):
        snake_direction = new_direction

# Generate a new food position
def generate_food():
    while True:
        x = random.randint(0, (GAME_WIDTH // CELL_SIZE) - 1) * CELL_SIZE
        y = random.randint(0, (GAME_HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
        if (x, y) not in snake:
            return (x, y)

# End the game
def game_over():
    canvas.delete("all")
    canvas.create_text(
        GAME_WIDTH // 2, GAME_HEIGHT // 2 - 40,
        text=f"Game Over! Score: {score}",
        fill="white",
        font=("Arial", 24)
    )

    # Create Restart Button
    restart_button = tk.Button(root, text="Restart", font=("Arial", 14), command=restart_game_button)
    restart_button.place(x=GAME_WIDTH // 2 - 60, y=GAME_HEIGHT // 2)

    # Create Exit Button
    exit_button = tk.Button(root, text="Exit", font=("Arial", 14), command=root.destroy)
    exit_button.place(x=GAME_WIDTH // 2 - 60, y=GAME_HEIGHT // 2 + 40)

# Restart the game using the button
def restart_game_button():
    global snake, snake_direction, food_position, score, speed, current_snake_color
    # Reset all game variables
    snake = [(100, 100), (80, 100), (60, 100)]
    snake_direction = "Right"
    food_position = generate_food()
    score = 0
    speed = 70
    current_snake_color = SNAKE_COLORS[0]  # Reset to the first color

    # Destroy all buttons
    for widget in root.winfo_children():
        if isinstance(widget, tk.Button):
            widget.destroy()

    # Clear the canvas and redraw everything
    canvas.delete("all")
    draw_snake()
    draw_food()
    move_snake()

# Bind keyboard events
root.bind("<Up>", lambda event: change_direction("Up"))
root.bind("<Down>", lambda event: change_direction("Down"))
root.bind("<Left>", lambda event: change_direction("Left"))
root.bind("<Right>", lambda event: change_direction("Right"))

# Start the game
draw_snake()
draw_food()
move_snake()

# Run the application
root.mainloop()