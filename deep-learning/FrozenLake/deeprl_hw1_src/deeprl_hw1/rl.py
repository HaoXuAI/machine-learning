# coding: utf-8
from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals
import random

import numpy as np


def evaluate_policy(env, gamma, policy, max_iterations=int(1e3), tol=1e-3):
    """Evaluate the value of a policy.

    See page 87 (pg 105 pdf) of the Sutton and Barto Second Edition
    book.

    http://webdocs.cs.ualberta.ca/~sutton/book/bookdraft2016sep.pdf

    Parameters
    ----------
    env: gym.core.Environment
      The environment to compute value iteration for. Must have nS,
      nA, and P as attributes.
    gamma: float
      Discount factor, must be in range [0, 1)
    policy: np.array
      The policy to evaluate. Maps states to actions.
    max_iterations: int
      The maximum number of iterations to run before stopping.
    tol: float
      Determines when value function has converged.

    Returns
    -------
    np.ndarray, int
      The value for the given policy and the number of iterations till
      the value function converged.
    """

    steps = 0
    Value = np.zeros(env.nS)

    while steps < max_iterations:
        delta = 0
        for s in range(0, env.nS):
            v = Value[s]
            new_value = 0
            action = policy[s]
            transition_table_row = env.P[s][action]
            for p, next_state, reward, is_terminal in transition_table_row:
                new_value += p * (reward + gamma * Value[next_state])
            Value[s] = new_value
            delta = max(delta, abs(v - Value[s]))

        if delta < tol:
            return Value, steps
        steps += 1

    return Value, steps


def value_function_to_policy(env, gamma, value_function):
    """Output action numbers for each state in value_function.

    Parameters
    ----------
    env: gym.core.Environment
      Environment to compute policy for. Must have nS, nA, and P as
      attributes.
    gamma: float
      Discount factor. Number in range [0, 1)
    value_function: np.ndarray
      Value of each state.

    Returns
    -------
    np.ndarray
      An array of integers. Each integer is the optimal action to take
      in that state according to the environment dynamics and the
      given value function.
    """
    policy = np.zeros(env.nS, dtype=int)
    actions_value = np.zeros(4)
    for s in range(env.nS):
        for a in range(0, 4):
            new_value = 0
            transition_table_row = env.P[s][a]
            for p, next_state, reward, is_terminal in transition_table_row:
                new_value += (p * (reward + gamma * value_function[next_state]))
            actions_value[a] = new_value

        policy[s] = np.argmax(actions_value)
    # action_names= {0 : 'L', 1 : 'D', 2 : 'R', 3 : 'U' }
    # print_policy(np.array(policy), action_names)

    return policy


def improve_policy(env, gamma, value_func, policy):
    """Given a policy and value function improve the policy.

    See page 87 (pg 105 pdf) of the Sutton and Barto Second Edition
    book.

    http://webdocs.cs.ualberta.ca/~sutton/book/bookdraft2016sep.pdf

        Parameters
    ----------
    env: gym.core.Environment
      The environment to compute value iteration for. Must have nS,
      nA, and P as attributes.
    gamma: float
      Discount factor, must be in range [0, 1)
    value_func: np.ndarray
      Value function for the given policy.
    policy: dict or np.array
      The policy to improve. Maps states to actions.

    Returns
    -------
    bool, np.ndarray
      Returns true if policy changed. Also returns the new policy.
    """

    policy_stable = True
    for s in range(0, env.nS):
        old_action = policy[s]
        new_action = value_function_to_policy(env, gamma, value_func)[s]
        if not old_action == new_action:
            policy_stable = False
        policy[s] = new_action

    return policy_stable, policy


def policy_iteration(env, gamma, max_iterations=int(1e3), tol=1e-3):
    """Runs policy iteration.

    See page 87 (pg 105 pdf) of the Sutton and Barto Second Edition
    book.

    http://webdocs.cs.ualberta.ca/~sutton/book/bookdraft2016sep.pdf

    You should use the improve_policy and evaluate_policy methods to
    implement this method.

    Parameters
    ----------
    env: gym.core.Environment
      The environment to compute value iteration for. Must have nS,
      nA, and P as attributes.
    gamma: float
      Discount factor, must be in range [0, 1)
    max_iterations: int
      The maximum number of iterations to run before stopping.
    tol: float
      Determines when value function has converged.

    Returns
    -------
    (np.ndarray, np.ndarray, int, int)
       Returns optimal policy, value function, number of policy
       improvement iterations, and number of value iterations.
    """
    policy = np.zeros(env.nS, dtype=int)
    value_func = np.zeros(env.nS)
    value_steps = 0
    improve_steps = 0
    policy_stable = False

    while not policy_stable:
        value_func, steps = evaluate_policy(env, gamma, policy, max_iterations, tol)
        value_steps += steps
        policy_stable, policy = improve_policy(env, gamma, value_func, policy)
        improve_steps += 1
    return policy, value_func, improve_steps, value_steps


def max_value(env, gamma, value_function, state):
    """Output value for each state in value_function.

    Parameters
    ----------
    env: gym.core.Environment
      Environment to compute policy for. Must have nS, nA, and P as
      attributes.
    gamma: float
      Discount factor. Number in range [0, 1)
    value_function: np.ndarray
      Value of each state.

    Returns
    -------
    np.ndarray
      An array of integers. Each integer is the optimal action value
      in that state according to the environment dynamics and the
      given value function.
    """

    actions_value = np.zeros(4)

    for a in range(0, 4):
        new_value = 0
        transition_table_row = env.P[state][a]
        for p, next_state, reward, is_terminal in transition_table_row:
            new_value += (p * (reward + gamma * value_function[next_state]))
        actions_value[a] = new_value

    return max(actions_value)


def value_iteration(env, gamma, max_iterations=int(1e3), tol=1e-3):
    """Runs value iteration for a given gamma and environment.

    See page 90 (pg 108 pdf) of the Sutton and Barto Second Edition
    book.

    http://webdocs.cs.ualberta.ca/~sutton/book/bookdraft2016sep.pdf

    Parameters
    ----------
    env: gym.core.Environment
      The environment to compute value iteration for. Must have nS,
      nA, and P as attributes.
    gamma: float
      Discount factor, must be in range [0, 1)
    max_iterations: int
      The maximum number of iterations to run before stopping.
    tol: float
      Determines when value function has converged.

    Returns
    -------
    np.ndarray, iteration
      The value function and the number of iterations it took to converge.
    """

    value_func = np.zeros(env.nS, dtype=float)
    num_steps = 0

    for num_steps in range(max_iterations):
        delta = 0
        for s in range(env.nS):
            v = value_func[s]
            value_func[s] = max_value(env, gamma, value_func, s)
            delta = max(delta, abs(v - value_func[s]))

        if delta < tol:
            break

        num_steps += 1
    return value_func, num_steps


def print_policy(policy, action_names):
    """Print the policy in human-readable format.

    Parameters
    ----------
    policy: np.ndarray
      Array of state to action number mappings
    action_names: dict
      Mapping of action numbers to characters representing the action.
    """
    str_policy = policy.astype('str')
    for action_num, action_name in action_names.items():
        np.place(str_policy, policy == action_num, action_name)

    print(str_policy)
