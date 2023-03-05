from random import randint
from numpy import ndarray, unique
from numpy.random import random_integers
from typing import Literal, Tuple


class FoodWorld:
    size = 16
    food = 24
    food_energy = 10
    max_energy = size * 2
    state_names = ("empty", "agent", "food", "wall")
    observation_names = [
        "energy",
        "up",
        "down",
        "left",
        "right",
    ]
    action_names = ["up", "down", "left", "right"]

    def __init__(self):
        self.grid = ndarray((self.size, self.size), dtype=int)
        self.grid.fill(self.state_names.index("empty"))

        agent_x = randint(0, self.size - 1)
        agent_y = randint(0, self.size - 1)
        self.grid[agent_x, agent_y] = self.state_names.index("agent")

        self.agent_energy = int(self.max_energy / 2)

        self.spawn_food()

    def move(self, action):
        x, y = self.get_agent_position()
        new_x, new_y = x, y

        if action == "up":
            if y > 0:
                new_y -= 1
            else:
                new_y = y
        elif action == "down":
            if y < self.size - 1:
                new_y += 1
            else:
                new_y = y
        elif action == "left":
            if x > 0:
                new_x -= 1
            else:
                new_x = x
        elif action == "right":
            if x < self.size - 1:
                new_x += 1
            else:
                new_x = x

        if self.grid[new_x, new_y] == self.state_names.index("food"):
            self.agent_energy += self.food_energy

        self.agent_energy -= 1  # cost of moving
        self.grid[x, y] = self.state_names.index("empty")
        self.grid[new_x, new_y] = self.state_names.index("agent")

        if self.agent_energy >= self.max_energy:
            self.agent_energy = self.max_energy - 1
        elif self.agent_energy < 0:
            self.agent_energy = 0

        self.spawn_food()

    def get_agent_position(self):
        for x in range(self.size):
            for y in range(self.size):
                if self.grid[x, y] == self.state_names.index("agent"):
                    return x, y
        raise Exception("Agent not found")

    def get_agent_observation(self):
        x, y = self.get_agent_position()
        wall_index = self.state_names.index("wall")
        return (
            self.agent_energy,
            self.grid[x, y - 1] if y > 0 else wall_index,
            self.grid[x, y + 1] if y < self.size - 1 else wall_index,
            self.grid[x - 1, y] if x > 0 else wall_index,
            self.grid[x + 1, y] if x < self.size - 1 else wall_index,
        )

    def spawn_food(self):
        state_counts = dict(zip(*unique(self.grid, return_counts=True)))
        current_food = state_counts.get(self.state_names.index("food"), 0)

        for _i in range(self.food - current_food):
            for _j in range(self.size):
                x = randint(0, self.size - 1)
                y = randint(0, self.size - 1)
                if self.grid[x, y] == self.state_names.index("empty"):
                    self.grid[x, y] = self.state_names.index("food")
                    break

    def print(self):
        # print(self.grid)
        for y in range(self.size):
            for x in range(self.size):
                if self.grid[x, y] == self.state_names.index("empty"):
                    print("⬜️", end="")
                elif self.grid[x, y] == self.state_names.index("agent"):
                    print("🟦", end="")
                elif self.grid[x, y] == self.state_names.index("food"):
                    print("🟥", end="")

            print()
        print("energy:", self.agent_energy)
