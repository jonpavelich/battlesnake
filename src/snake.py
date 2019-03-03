from util import get_config
from pathfind import find_path
import json
import random

config = get_config()

"""
This function decides on priorities and makes a decision about what to do
"""
def choose_move(data):
    # Initialize board with 0 weights
    # Positive weights are more desirable; negative less
    weights = [[0 for x in range(data['board']['width'])] for y in range(data['board']['height'])]
    snakes = data['board']['snakes']
    food = data['board']['food']
    head = data['you']['body'][0]
    tail = data['you']['body'][-1]
    length = len(data['you']['body'])
    health = data['you']['health']
    myId = data['you']['id']
    width = data['board']['width']
    height = data['board']['height']
    # Weight snake bodies as very underisable suntanning spots
    weights = weight_snakes(weights, snakes)
    weights = weight_heads(weights, snakes, length, myId, width, height)
    
    weights[head['x']][head['y']] = 0
    
    targets = [tail,]
    # DECIDE WHAT THE SNAKE DOES
    if length < config['desiredLength']:
        targets = food
    elif health < config['desiredHealth']:
        targets = food


    # DEBUG Print Statement
    for row in weights:
        print(row)

   

    direction = find_path(data['board'], weights, head, food)
    
    return direction

"""
Negatively weight the snakes so we don't step on their tail
"""
def weight_snakes(weights, snakes):
    for snake in snakes:
        for coord in snake['body'][:-1]:
            weights[coord['x']][coord['y']] += -10000
    return weights

"""
Negatively weight the area around a snake's head 
Bigger snakes = lower weight
"""
def weight_heads(weights, snakes, length, myId, width, height):
    for snake in snakes:
        if snake['id'] != myId:
            x = snake['body'][0]['x']
            y = snake['body'][0]['y']
            # If it's bigger than or equal to us, try to stay away from it
            # If it's smaller than us, don't do that
            biggerHead = config['weights']['biggerHead']
            smallerHead = config['weights']['smallerHead']
            if len(snake['body']) >= length:
                weight = biggerHead
            else: 
                weight = smallerHead

            print("What the hell")
            print(weight)
            #All surrounding directions seem like a bad place to be
            if weights[x][y+1] != None:
                if is_inbounds(height, width, x, y+1):
                    weights[x][y+1] += weight
            if weights[x][y-1] != None:
                if is_inbounds(height, width, x, y-1):
                    weights[x][y-1] += weight
            if weights[x+1][y] != None:
                if is_inbounds(height, width, x+1, y):
                    weights[x+1][y] += weight
            if weights[x-1][y] != None:
                if is_inbounds(height, width, x-1, y):
                    weights[x-1][y] += weight
    return weights

def is_inbounds(height, width, x, y):
    if x < 0 or x >= width or y < 0 or y >= height:
        return 0
    else: 
        return 1

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