from itertools import repeat
from random import randint
from typing import TYPE_CHECKING, Optional, Union

import numpy as np
import pymdp
from pymdp.agent import Agent

if TYPE_CHECKING:
    from killer_world.world import KillerWorld


class KillerWorldAgent:
    agent: Agent
    id: int
    world_size: int
    action_names: list[str]

    def __init__(
        self,
        id: int,
        world_size: int,
        action_names: list[str],
        A: Optional[np.ndarray] = None,
        B: Optional[np.ndarray] = None,
        C: Optional[np.ndarray] = None,
    ):
        self.id = id
        self.world_size = world_size
        self.action_names = action_names

        observation_sizes = [
            self.world_size + 1,
            self.world_size + 1,
            self.world_size + 1,
        ]

        # probability of world state, given observation
        A_world_given_observations = (
            A
            if A is not None
            else pymdp.utils.random_A_matrix(
                observation_sizes,
                [self.world_size**2],
            )
        )

        # probability of world state, given action
        B_world_given_actions = (
            B
            if B is not None
            else pymdp.utils.random_B_matrix(
                [self.world_size**2],
                [len(self.action_names)],
            )
        )

        # preferred observation state
        C_observation_preference = (
            C if C is not None else pymdp.utils.obj_array_zeros(observation_sizes)
        )

        self.agent = Agent(
            A=A_world_given_observations,
            B=B_world_given_actions,
            C=C_observation_preference,
        )

    def step(self, world: "KillerWorld") -> str:
        observations = self.get_observation(world)
        self.agent.infer_states(observations)
        self.agent.infer_policies()

        action = self.action_names[int(self.agent.sample_action()[0])]

        self.agent.step_time()

        return action

    def get_observation(self, world: "KillerWorld"):
        x, y = world.get_position(self.id)
        up_distance = 0
        for distance, check_y in enumerate(reversed(range(0, y))):
            if world.grid[x][check_y] == -1:
                up_distance = distance + 1
                break

        down_distance = 0
        for distance, check_y in enumerate(range(y + 1, self.world_size)):
            if world.grid[x][check_y] == -1:
                down_distance = distance + 1
                break

        right_distance = 0
        for distance, check_x in enumerate(range(x + 1, self.world_size)):
            if world.grid[check_x][y] == -1:
                right_distance = distance + 1
                break

        return (up_distance, down_distance, right_distance)

    def reproduce(self, world: "KillerWorld", id: int) -> "KillerWorldAgent":
        C_observation_preference = self.agent.C.copy()
        noise = np.random.normal(0, 0.1, C_observation_preference.shape)
        new_C_observation_preference = C_observation_preference + noise

        return KillerWorldAgent(
            id,
            self.world_size,
            self.action_names,
            A=self.agent.A.copy(),
            B=self.agent.B.copy(),
            C=new_C_observation_preference,
        )
