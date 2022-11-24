# Snail jumper
**Neuroevolution game assignment.**  
**Fall 2021 - Computer Intelligence.**  

This game has been developed as an assignment for students at Amirkabir University of Technology to apply neuroevolution using a simple game.  
![Snail Jumber](SnailJumper.png)

You can find project's description in Persian in  [this file](/CI_NeuroevolutionGame.pdf).

## How to run

### Requirements

- Python 3.8 or higher
- Pygame 2.0.1 or higher

### Run

- Clone the repository
- Run `python game.py`

## How to play

This game has two modes: **Manual** and **Neuroevolution**.

### Manual

In this mode, you can control the snail using the space bar.

### Neuroevolution

In this mode, the snail is controlled by a neural network.

## Development

- [x] Create a simple game use pygame
- [x] Create a simple neural network
- [x] Create a simple genetic algorithm
- [x] Create a simple neuroevolution algorithm
- [x] Create a simple neuroevolution algorithm with genetic algorithm
## Project structure

- `game.py`: Main file to run the game
  - include all other files
- `nn.py`: Neural network class
    - `NeuralNetwork` class
        - `__init__`: initialize neural network
        - `forward`: feed forward function
        - `batch_normalize`: normalize input
        - `activation`: activation function
          - `sigmoid`: use sigmoid activation function
- `evolution.py`: Evolution class
    - `Evolution` class
        - `__init__`: initialize evolution
        - `next_population_selection`: select next population from current population and wrire to [average.txt](/average.txt) use Q-Tournament
        if you want to use SUS  selection, uncomment line 46 to 62 and comment line 65 to 74
        - `generate_new_population`: generate new population from current population
        - `mutate`: mutate a population
        - `clone_player`: clone a player
- `player.py`: Player class
    - `Player` class
        - `__init__`: initialize player
        - `flip_player_horizontally`: flip player horizontally
        - `update`: update player use neural network or keyboard
        - `animation_state`: animate player
        - `apply_gravity`: apply gravity to player
        - `player_input`: get player input in manual mode
        - `change_gravity`: change gravity 
        - `think`: get output from neural network and change gravity
        - `make_inputs`: make inputs for neural network
        - `batch_normalize`: normalize inputs
- `plot.py`: Plot class
    - plot average score and best score from [average.txt](/average.txt) 
- `average.txt`: save average score and min score from each generation
    - x y z : max score, min score, average score
you can use this file to plot average score and best score

plots of two different runs are:
- [first-run](https://github.com/mohamadch91/SnailJumper/blob/master/Screenshot%202022-01-24%20235711.png)
- [second-run](https://github.com/mohamadch91/SnailJumper/blob/master/Screenshot%202022-01-24%20235741.png)        


## Contributors
[SoroushMehraban](https://github.com/SoroushMehraban)
<br />
[mohamadch91](https://github.com/mohamadch91)

## Orginal Repository
[SoroushMehraban/SnailJumper](https://github.com/SoroushMehraban/SnailJumper)