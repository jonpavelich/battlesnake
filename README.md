# BattleSnake
A [BattleSnake](https://battlesnake.io) AI written during the 2019 contest.

## Team
Jon Pavelich ([GitLab](https://gitlab.com/jonpavelich), [GitHub](https://github.com/jonpavelich))  
Tyler Harnadek ([GitLab](https://gitlab.com/tharnadek), [GitHub](https://gitlab.com/tharnadek))

## Overview
This snake is based on the [Python 3 Starter Snake](https://github.com/jonpavelich/battlesnake-python3-starter) we also developed during the 2019 contest (the starter snake is available under a more permissive license). It uses Flask and Gunicorn to serve requests, and GitLab CI to deploy to Heroku.

### Strategy
#### Targeting
This snake chooses targets based on its desired length and hunger level; currently it can choose between food and its own tail. When selecting between multiple targets, it currently chooses the closest one computed by Manhattan distance. 

#### Board Weighting 
The board is weighted according to how favourable (positive weighting) or dangerous (negative weighting) the tile is. The weights are initialized to zero. Currently, the area around the heads of snakes who are smaller than us is positively weighted, and the area around the heads of snakes who are the same length or larger than us is negatively weighted, and snake bodies are very negatively weighted. 

#### Pathfinding
Pathfinding is done using A*. The board weighting of each tile is subtracted from G(n) (cost to travel from start to n), which discourages negative weighted tiles (by increasing the cost to reach them) and encourages positive tiles (by decreasing the cost to reach them). The heuristic function simply computes Manhattan distance to guide the search. This finds an path which attempts to pass through positively weighted tiles near our path and avoids negatively weighted tiles.

### Issues
For a list of bugs and improvements which are needed for future contests, see [ISSUES.md](ISSUES.md).

### License
This code is available under the GNU Affero General Public License v3.0. See [LICENSE.md](LICENSE.md).
