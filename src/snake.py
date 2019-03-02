from util import get_config
from pathfind import find_path
import json

config = get_config()

"""
This function decides on priorities and makes a decision about what to do
"""
def choose_move(data):
    # Initialize board with 0 weights
    # Positive weights are more desirable; negative less
    weights = [[0 for x in range(data['board']['width'])] for y in range(data['board']['height'])]
    snakes = data['board']['snakes']
    
    # Weight snake bodies as very underisable suntanning spots
    weights = weight_snakes(weights, snakes)

    for row in weights:
        print(row)

    direction = find_path(data['board'], weights)
    return direction

"""
Negatively weight the snakes so we don't step on their tail
"""
def weight_snakes(weights, snakes):
    for snake in snakes:
        for coord in snake['body'][:-1]:
            weights[coord['x']][coord['y']] += -100
    return weights

"""
Sample Data:
{
  "game": {
    "id": "game-id-string"
  },
  "turn": 4,
  "board": {
    "height": 15,
    "width": 15,
    "food": [
      {
        "x": 1,
        "y": 3
      }
    ],
    "snakes": [
      {
        "id": "snake-id-string",
        "name": "Sneky Snek",
        "health": 90,
        "body": [
          {
            "x": 1,
            "y": 3
          }
        ]
      }
    ]
  },
  "you": {
    "id": "snake-id-string",
    "name": "Sneky Snek",
    "health": 90,
    "body": [
      {
        "x": 1,
        "y": 3
      }
    ]
  }
}
"""