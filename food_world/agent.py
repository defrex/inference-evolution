import numpy as np
import pymdp
from pymdp.agent import Agent

from .world import FoodWorld


def random_agent(world: FoodWorld) -> Agent:
    observation_sizes = [
        world.max_energy,
        len(world.state_names),
        len(world.state_names),
        len(world.state_names),
        len(world.state_names),
    ]

    # probability of world state, given observation
    A_world_given_observations = pymdp.utils.random_A_matrix(
        observation_sizes,
        [world.size**2],
    )

    # probability of world state, given action
    B_world_given_actions = pymdp.utils.random_B_matrix(
        [world.size**2],
        [len(world.action_names)],
    )

    # preferred observation state
    C_observation_preference = pymdp.utils.obj_array_zeros(observation_sizes)

    # prefer higher energy
    C_observation_preference[world.observation_names.index("energy")] = np.arange(
        -world.max_energy / 2, world.max_energy / 2
    )

    return Agent(
        A=A_world_given_observations,
        B=B_world_given_actions,
        C=C_observation_preference,
    )
