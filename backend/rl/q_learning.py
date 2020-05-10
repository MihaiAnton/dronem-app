"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   02.05.2020 19:02
"""
import json
import random
from typing import Dict
from typing import Optional

import numpy as np

from environments.env_interpretation.state_utils import get_state_from_observation
from environments.envs import DronemEnv
from utils.websocket_utils import send_to_websocket


class QLearning:
    """
    Class for q-learning algorithm
    """

    def __init__(self,
                 env: DronemEnv,
                 path_to_save: Optional[str] = None,
                 episodes: int = 55_000,
                 epsilon: float = 1,
                 epsilon_decay: float = 0.99989,
                 min_epsilon: float = 0.0005,
                 discount: float = 0.9,
                 lr: float = 0.1,
                 stats_every: int = 50,
                 q_table_every: Optional[int] = None):

        self.__env_data = env.get_env_metadata()
        self.__env = env
        self.__num_actions = env.action_space.n
        self.__episodes = episodes
        self.__epsilon = epsilon
        self.__epsilon_decay = epsilon_decay
        self.__min_epsilon = min_epsilon
        self.__discount = discount
        self.__lr = lr
        self.__q_tbl = {}
        self.__stats_every = stats_every
        self.__ep_rewards = []
        self.__stats = {
            'ep': [], 'min': [], 'max': [], 'avg': []
        }
        if q_table_every:
            self.__q_table_every = q_table_every
        else:
            self.__q_table_every = self.__episodes // 5
        if path_to_save:
            self.__path_to_save = path_to_save
        else:
            self.__q_table_every = self.__episodes + 1
            self.__path_to_save = ''

    def __select_action(self, epsilon: float, state: np.array) -> int:
        state = tuple(state)

        if self.__q_tbl.get(state, None) is None:
            self.__q_tbl = self.__add_state_q(state)

        if random.random() < epsilon:
            return np.random.randint(0, self.__num_actions)
        else:
            return int(np.argmax(self.__q_tbl[state]))

    def __add_state_q(self, state: np.array) -> Dict:
        state = tuple(state)
        self.__q_tbl[state] = -1 + np.zeros(self.__num_actions)
        return self.__q_tbl

    def __update_q(self, state: np.array, action: int, reward: float, new_state: np.array) -> Dict:
        state = tuple(state)  # by default np arrays are not hashable
        new_state = tuple(new_state)
        if self.__q_tbl.get(new_state, None) is None:
            self.__q_tbl = self.__add_state_q(new_state)

        max_q_future = np.max(self.__q_tbl[new_state])

        current_q = self.__q_tbl[state][action]

        new_q = (1 - self.__lr) * current_q + self.__lr * (reward + self.__discount * max_q_future)

        self.__q_tbl[state][action] = new_q
        return self.__q_tbl

    @staticmethod
    def __save_table_to_file(payload: json, file_path: str) -> None:
        with open(file_path, 'w+') as f:
            f.write(payload)

    def train(self) -> None:
        for episode in range(self.__episodes + 1):
            episode_reward = 0
            print(f"STARTING EPISODE: {episode}")
            done = False
            state = self.__env.reset()
            while not done:
                action = self.__select_action(self.__epsilon, state)
                new_state, reward, done, _ = self.__env.step(action)

                episode_reward += reward
                if not done:
                    self.__q_tbl = self.__update_q(state, action, reward, new_state)
                else:
                    if get_state_from_observation(new_state).time == self.__env_data['max_steps']:
                        self.__q_tbl[tuple(state)][action] = -1
                    else:
                        self.__q_tbl[tuple(state)][action] = reward
                state = new_state

            self.__ep_rewards.append(episode_reward)
            if not episode % self.__stats_every:
                avg_reward = sum(self.__ep_rewards[-self.__stats_every:]) / self.__stats_every
                min_reward = min(self.__ep_rewards[-self.__stats_every:])
                max_reward = max(self.__ep_rewards[-self.__stats_every:])
                self.__stats['ep'].append(episode)
                self.__stats['avg'].append(avg_reward)
                self.__stats['min'].append(min_reward)
                self.__stats['max'].append(max_reward)
                send_to_websocket(self.__stats, "1")
                print(f"EPISODE: {episode}, avg: {avg_reward}, min: {min_reward}, max: {max_reward}")

            if not episode % self.__q_table_every and episode > 0:
                table = json.dumps({str(k): list(v) for k, v in self.__q_tbl.items()})
                self.__save_table_to_file(table, f"{self.__path_to_save}/Q_table_{episode}.json")

            if self.__epsilon > self.__min_epsilon:
                self.__epsilon *= self.__epsilon_decay
