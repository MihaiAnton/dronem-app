"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   22.03.2020 00:21
"""

import pytest
from django.contrib.auth import get_user_model
from faker import Faker

from environments.env_interpretation import MeetingEnv
from environments.envs.DronemEnv import DronemEnv

User = get_user_model()
faker = Faker()


@pytest.fixture
def env4_robots() -> DronemEnv:
    """
    Returns the environment, alongside its pair mapping
    :return:
    """
    return DronemEnv(
        num_robots=4,
        max_memory=15,
        init_memory=10,
        meetings=[
            MeetingEnv(r1=1, r2=2, first_time=4),
            MeetingEnv(r1=2, r2=3, first_time=2),
            MeetingEnv(r1=0, r2=1, first_time=2),
            MeetingEnv(r1=0, r2=2, first_time=4)
        ],
        cycles=[
            [2],
            [1, 2],
            [3, 5, 4, 2],
            [6, 5]
        ]
    )


@pytest.fixture
def env3_robots() -> DronemEnv:
    """
    Returns the environment, alongside its robot pair mapping
    :return:
    """
    return DronemEnv(
        num_robots=3,
        init_memory=15,
        max_memory=55,
        meetings=[
            MeetingEnv(r1=1, r2=2, first_time=5),
            MeetingEnv(r1=0, r2=1, first_time=1)
        ],
        cycles=[
            [2],
            [1, 2, 3],
            [4, 3]
        ]
    )


@pytest.fixture
def env3_robots_modified() -> DronemEnv:
    """
        Returns the environment, alongside its robot pair mapping
        :return:
        """
    return DronemEnv(
        num_robots=3,
        init_memory=1,
        max_memory=2,
        meetings=[
            MeetingEnv(r1=1, r2=2, first_time=2),
            MeetingEnv(r1=0, r2=1, first_time=1)
        ],
        cycles=[
            [2],
            [2, 3, 1],
            [4, 3]
        ]
    )


@pytest.fixture
def user() -> User:
    return User.objects.create(
        username=faker.user_name(),
        email=faker.email(),
        password='test123test123test123'
    )
