from random import randint
from typing import Optional

from killer_world.agent import KillerWorldAgent


class KillerWorld:
    size = 32
    killer_min = 4
    killer_max = size * 2
    agent_min = 3
    agent_max = size
    agents: list[Optional["KillerWorldAgent"]] = []
    state_names = ("empty", "agent", "killer")
    observation_names = ["up", "down", "right"]
    action_names = ["up", "down", "right"]

    def __init__(self):
        self.grid: list[list[Optional[int]]] = []
        for x in range(self.size):
            self.grid.append([])
            for y in range(self.size):
                self.grid[x].append(None)

        for _i in range(self.agent_min):
            agent = KillerWorldAgent(len(self.agents), self.size, self.action_names)
            self.agents.append(agent)
            self.place(agent.id, x=0)

        for _i in range(self.killer_min):
            self.place(-1, x=self.size - 1)

    def step(self):
        for agent in self.agents:
            if agent is None:
                continue
            action = agent.step(self)
            self.move_agent(agent, action)
        self.move_killers()

    def move_agent(self, agent: "KillerWorldAgent", action: str):
        x, y = self.get_position(agent.id)
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
        elif action == "right":
            new_x += 1

        if new_x >= self.size - 1:
            new_x = 0
            self.reproduce_agent(agent)

        if self.grid[new_x][new_y] == -1:
            self.kill_agent(agent)
        elif self.grid[new_x][new_y] is not None:
            new_x = x
            new_y = y

        self.grid[x][y] = None
        self.grid[new_x][new_y] = agent.id

    def kill_agent(self, agent: "KillerWorldAgent"):
        self.agents[agent.id] = None

        x, y = self.get_position(agent.id)
        self.grid[x][y] = -1

        new_agent = KillerWorldAgent(len(self.agents), self.size, self.action_names)
        self.agents.append(new_agent)
        self.place(new_agent.id, x=0)

    def reproduce_agent(self, agent: "KillerWorldAgent"):
        x, y = self.get_position(agent.id)
        self.grid[x][y] = None
        self.place(agent.id, x=0)

        new_agent = agent.reproduce(self, len(self.agents))
        self.agents.append(new_agent)
        self.place(new_agent.id, x=0)

    def get_position(
        self,
        id: int,
    ):
        for x in range(self.size):
            for y in range(self.size):
                if self.grid[x][y] == id:
                    return x, y
        raise Exception(f"ID not found id:{id}")

    def place(self, id: int, x: Optional[int] = None, y: Optional[int] = None):
        new_y = randint(0, self.size - 1) if y is None else y
        new_x = randint(0, self.size - 1) if x is None else x

        for _i in range(self.size):
            if self.grid[new_x][new_y] is None:
                self.grid[new_x][new_y] = id
                return

            if x is None:
                new_x = randint(0, self.size - 1)
            if y is None:
                new_y = randint(0, self.size - 1)

        raise Exception(f"Cannot place id:{id} at {x}, {y}")

    def move_killers(self):
        agent_count = len([agent for agent in self.agents if agent is not None])
        proportion = (agent_count - self.agent_min) / (self.agent_max - self.agent_min)
        needed_killers = int(self.killer_max * proportion)

        current_killers = 0
        for x in range(self.size):
            for y in range(self.size):
                if self.grid[x][y] != -1:
                    continue

                self.grid[x][y] = None
                if x == 0:
                    continue

                new_x, new_y = x - 1, y

                id = self.grid[new_x][new_y]
                if id is not None and id != -1 and self.agents[id] is not None:
                    self.kill_agent(self.agents[id])  # type: ignore

                self.grid[new_x][new_y] = -1
                current_killers += 1

        for _i in range(needed_killers - current_killers):
            self.place(-1, x=self.size - 1)

    def __repr__(self):
        board = ""
        for y in range(self.size):
            for x in range(self.size):
                if self.grid[x][y] is None:
                    board += "⬜️"
                elif self.grid[x][y] == -1:
                    board += "🟥"
                else:
                    board += "🟦"

            board += "\n"
        return board
