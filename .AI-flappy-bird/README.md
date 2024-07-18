展示短片: https://www.youtube.com/watch?v=Z1VQu9UOKmY

#steps to take!
1.recreate flappy bird with python
2.code an simple AI algorithm
3.train said algorithm and tune while doing fine adjustments
4.hopefully having a working AI at the end :O

update: success!


Features:
    red bird (cuter than yellow)
    nightsky background(has a breathing effect as a bonus)
    cute flapping sound effect
    uses a very simple neural network!

in depth:
# Flappy Bird AI with NEAT

This project implements an AI to learn how to play Flappy Bird using the NEAT (NeuroEvolution of Augmenting Topologies) algorithm. The AI evolves through generations to optimize its gameplay strategies, gradually improving its ability to navigate through pipes.

## Project Structure

- **main.py**: main.py, self explanatory
- **classes.py**: This file contains all the classes used!
- **assets/**: This directory contains all images and sounds used in the game.
- **NEAT-config.txt**: NEAT algorithm's configuration settings.

## How It Works

### NEAT Algorithm

The NEAT algorithm is used to evolve a population of neural networks. The neural networks control the bird's actions in the game, learning when to jump to avoid pipes and stay within the screen boundaries.

### Game Mechanics

- **Bird**: The bird can jump and fall, controlled by the neural network's output. It earns fitness points by staying alive and passing through pipes.
- **Pipes**: Pipes move towards the bird from the right side of the screen. The bird must avoid colliding with these pipes.
- **Ground**: The ground moves continuously to simulate forward motion. The bird must avoid hitting the ground.

### NEAT Setup

The NEAT setup initializes the population and runs the main game loop for a specified number of generations. Each bird (neural network) in the population plays the game, and its performance is evaluated based on its score and how long it survives.

### Fitness Evaluation

Birds are rewarded for:
- Staying alive (small fitness increment).
- Passing through pipes (big fitness increment).
Birds are penalized for:
- Colliding with pipes.
- Hitting the ground or flying out of bounds.

## Running the Project

1. Ensure you have Python and Pygame installed.
2. Clone the repository and navigate to the project directory.
3. Run the `main.py` script to start the training process.

```bash
python main.py
