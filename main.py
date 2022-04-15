from SimpleGame import SimpleGame
from IterativeGame import IterativeGame
import numpy as np

def test1():
  """Prisoners' dilemma - a simple game"""
  agents = ["A", "B"]
  actions = [0, 1]
  payoff_function = {
    (0, 0): [6,6],
    (0, 1): [0,10],
    (1, 0): [10,0],
    (1, 1): [1,1]
  }


  game = SimpleGame(agents, actions, payoff_function)
  assert game.calculate_nash_states() == [(1, 1)]

def test2():
  """A simple game with three actions."""
  agents = ["A", "B"]
  actions = [0, 1, 2]
  payoff_function = {
    (0,0): [2,1],
    (0,1): [1,2],
    (0,2): [0,1],
    (1,0): [1,2],
    (1,1): [1,0],
    (1,2): [0,0],
    (2,0): [0,1],
    (2,1): [0,0],
    (2,2): [2,1]
  }


  game = SimpleGame(agents, actions, payoff_function)
  assert game.calculate_nash_states() == [(0, 1), (2, 2)]

def test3():
  """A simple game with three agents."""
  # https://economics.stackexchange.com/questions/34297/pure-nash-equilibria-3-players-game
  
  agents = ["A", "B", "C"]
  actions = [0, 1]
  payoff_function = {
    (0,0,0): [70,70,70],
    (0,1,0): [10,10,23],
    (1,0,0): [60,0,0],
    (1,1,0): [60,65,10],
    (0,0,1): [70,70,60],
    (0,1,1): [10,20,0],
    (1,0,1): [80,50,30],
    (1,1,1): [60,55,5],
  }

  game = SimpleGame(agents, actions, payoff_function)
  assert game.calculate_nash_states() == [(0, 0, 0), (1, 1, 0)]


def test4():
  """Prisoners' dilemma with neutral trust."""
  agents = ["A", "B"]
  actions = [0, 1]
  payoff_function = {
    (0, 0): [6,6],
    (0, 1): [0,10],
    (1, 0): [10,0],
    (1, 1): [1,1]
  }
  belief_values = {
    "A": np.array([[0.5, 0.5]]),
    "B": np.array([[0.5, 0.5]])
  }
  initial_choices_prob = {
    "A": [1, 0],
    "B": [1, 0]
  }
  belief_update_value = 0.1
  iter_count = 10

  game = IterativeGame(agents, actions, payoff_function, belief_values, initial_choices_prob, belief_update_value, iter_count)
  game.play_game()


def test5():
  """Prisoners' dilemma with high trust."""
  agents = ["A", "B"]
  actions = [0, 1]
  payoff_function = {
    (0, 0): [6,6],
    (0, 1): [0,10],
    (1, 0): [10,0],
    (1, 1): [1,1]
  }
  belief_values = {
    "A": np.array([[0.8, 0.2]]),
    "B": np.array([[0.8, 0.2]])
  }
  belief_update_value = 0.1
  iter_count = 10

  game = IterativeGame(agents, actions, payoff_function, belief_values, None, belief_update_value, iter_count)
  game.play_game()


def test6():
  """ Stag Hare Hunt with neutral trust"""
  agents = ["A", "B"]
  actions = [0, 1]
  payoff_function = {
    (0, 0): [3,3],
    (0, 1): [0,2],
    (1, 0): [2,0],
    (1, 1): [2,2]
  }
  belief_values = {
    "A": np.array([[0.5, 0.5]]),
    "B": np.array([[0.5, 0.5]])
  }

  belief_update_value = 0.1
  iter_count = 10

  game = IterativeGame(agents, actions, payoff_function, belief_values, None, belief_update_value, iter_count)
  game.play_game()


def test7():
  """ Stag Hare Hunt with high trust"""
  agents = ["A", "B"]
  actions = [0, 1]
  payoff_function = {
    (0, 0): [3,3],
    (0, 1): [0,2],
    (1, 0): [2,0],
    (1, 1): [2,2]
  }
  belief_values = {
    "A": np.array([[0.8, 0.2]]),
    "B": np.array([[0.8, 0.2]])
  }

  belief_update_value = 0.1
  iter_count = 10

  game = IterativeGame(agents, actions, payoff_function, belief_values, None, belief_update_value, iter_count)
  game.play_game()


if __name__ == "__main__":
  test1()
  test2()
  test3()
  test4()
  test5()
  test6()
  test7()