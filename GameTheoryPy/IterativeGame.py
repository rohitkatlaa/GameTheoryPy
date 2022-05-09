import random
import numpy as np
from typing import Callable, Dict, List, Tuple


class SimpleIterativeGame:

  def __init__(self, player_list: List, actions_list: List, payoff_function: Dict[Tuple, List[float]], belief_values: Dict[str, np.array], initial_choices_prob: Dict[str, List[float]], belief_update_value: float, iter_count: int):
    self.player_list = player_list
    self.actions_list = actions_list
    self.payoff_function = payoff_function
    self.belief_values = belief_values
    self.belief_update_value = belief_update_value
    self.initial_choices_prob = initial_choices_prob
    self.iter_count = iter_count
    SimpleIterativeGame.validate(self.player_list, self.actions_list, self.payoff_function, self.belief_values, self.initial_choices_prob)

  @staticmethod
  def validate(player_list: List, actions_list: List, payoff_function: Dict[Tuple, List[float]], belief_values: Dict[str, np.array], initial_choices_prob: Dict[str, List[float]]):
    n = len(player_list)
    a = len(actions_list)
    assert len(payoff_function) == a**n
    for strategy in payoff_function.keys():
      for action in strategy:
        assert action in actions_list
      assert len(strategy) == n
      assert len(payoff_function[strategy]) == n
    assert len(belief_values) == n
    for key in belief_values.keys():
      assert key in player_list
      assert belief_values[key].shape == (n-1, a)    
    if initial_choices_prob:
      for key in initial_choices_prob.keys():
        assert key in player_list
        assert len(initial_choices_prob[key]) == a

  def get_expected_payoff_dict(self):
    n = len(self.player_list)
    a = len(self.actions_list)
    expected_payoff_dict = {}
    for player in self.player_list:
      expected_payoff_dict[player] = [0]*a
    for scenario in self.payoff_function.keys():
      for player_index in range(len(self.player_list)):
        prob = 1
        scenario_view = scenario[:player_index]+scenario[player_index+1:]
        player_action_index = self.actions_list.index(scenario[player_index])
        player = self.player_list[player_index]

        for other_player_index in range(len(scenario_view)):
          other_player_action_index = self.actions_list.index(scenario_view[other_player_index])
          prob *= self.belief_values[player][other_player_index][other_player_action_index]

        expected_payoff_dict[player][player_action_index] += prob*self.payoff_function[scenario][player_index]
    
    return expected_payoff_dict

  def get_strategy(self, initial=False):
    n = len(self.player_list)
    a = len(self.actions_list)
    strategy = ()
    if initial and self.initial_choices_prob:
      for player_index in range(len(self.player_list)):
        action = random.choices(self.actions_list, weights=self.initial_choices_prob[self.player_list[player_index]], k=1)[0]
        strategy += (action, )
    else:
      expected_payoff_dict = self.get_expected_payoff_dict()
      for player in self.player_list:
        expected_payoff = expected_payoff_dict[player]
        max_payoff = max(expected_payoff)
        best_actions = [self.actions_list[i] for i, j in enumerate(expected_payoff) if j==max_payoff]
        action = random.choice(best_actions)
        strategy += (action, )

    return strategy

  @staticmethod
  def update_beliefs(scenario, player_list, actions_list, belief_values, belief_update_value):
    new_belief_values = {}
    belief_dec_value = belief_update_value/(len(actions_list)-1)
    for player in belief_values.keys():
      player_index = player_list.index(player)
      beliefs = belief_values[player].copy()
      scenario_view = scenario[:player_index]+scenario[player_index+1:]

      for other_player_index in range(len(scenario_view)):
        other_player_action_index = actions_list.index(scenario_view[other_player_index])
        # Decrease the belief of all other actions and increase the belief of the action that the agent took.
        beliefs[other_player_index] = list(map(lambda x: max(x-belief_dec_value, 0), beliefs[other_player_index]))
        beliefs[other_player_index][other_player_action_index] += belief_dec_value + belief_update_value
        beliefs[other_player_index][other_player_action_index] = min(beliefs[other_player_index][other_player_action_index], 1)

      new_belief_values[player] = beliefs    
    return new_belief_values

  def print_game(self, iter, iter_strategy):
    iter_payoff = self.payoff_function[iter_strategy]
    print("-"*100)
    print("Iteration {}:".format(iter))
    print("Actions of players: {}".format(iter_strategy))
    print("Payoffs of players: {}".format(iter_payoff))
    print("Beliefs of players: {}".format(self.belief_values))
    print("-"*100)

  def play_game(self):
    for iter in range(self.iter_count):
      iter_strategy = self.get_strategy(iter==0)
      self.belief_values = SimpleIterativeGame.update_beliefs(iter_strategy, self.player_list, self.actions_list, self.belief_values, self.belief_update_value)
      self.print_game(iter, iter_strategy)


class IterativeGame:

  def __init__(self, player_list: List, actions_list: List, payoff_function: Dict[Tuple, List[float]], strategy_function: Dict[str, Callable], iter_count: int):
    IterativeGame.validate(player_list, actions_list, payoff_function, strategy_function)
    self.player_list = player_list
    self.actions_list = actions_list
    self.payoff_function = payoff_function
    self.strategy_function = strategy_function
    self.iter_count = iter_count

  @staticmethod
  def validate(player_list: List, actions_list: List, payoff_function: Dict[Tuple, List[float]], strategy_function: Dict[str, Callable]):
    n = len(player_list)
    a = len(actions_list)
    assert len(payoff_function) == a**n
    for payoff in payoff_function.keys():
      for action in payoff:
        assert action in actions_list
      assert len(payoff) == n
      assert len(payoff_function[payoff]) == n
    assert len(strategy_function) == n
    for strategy in strategy_function.keys():
      assert strategy in player_list

  def print_iter(self, iter, game_action, players_total_payoff):
    iter_payoff = self.payoff_function[game_action]
    print("-"*100)
    print("Iteration {}:".format(iter))
    print("Actions of players: {}".format(game_action))
    print("Payoffs of players: {}".format(iter_payoff))
    print("Total playoff of players: {}".format(players_total_payoff))
    print("-"*100)
  
  def play_game(self):
    history = {}
    players_payoff = {}
    players_total_payoff = []
    for player in self.player_list:
      history[player] = []
      players_payoff[player] = []
      players_total_payoff.append(0)

    for iter in range(self.iter_count):
      game_action = ()
      for player in self.player_list:
        action = self.strategy_function[player](player, self.player_list, history)
        game_action += (action, )

      for player_num in range(len(self.player_list)):
        history[self.player_list[player_num]].append(game_action[player_num])
        players_payoff[self.player_list[player_num]].append(self.payoff_function[game_action][player_num])
        players_total_payoff[player_num] += self.payoff_function[game_action][player_num]
      
      self.print_iter(iter, game_action, players_total_payoff)

    