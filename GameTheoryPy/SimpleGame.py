from typing import Dict, List, Tuple


class SimpleGame:

  def __init__(self, player_list: List, actions_list: List, payoff_function: Dict[Tuple, List[float]]):
    self.player_list = player_list
    self.actions_list = actions_list
    self.payoff_function = payoff_function
    SimpleGame.validate(self.player_list, self.actions_list, self.payoff_function)


  @staticmethod
  def validate(player_list: List, actions_list: List, payoff_function: Dict[Tuple, List[float]]):
    n = len(player_list)
    a = len(actions_list)
    assert len(payoff_function) == a**n
    for strategy in payoff_function.keys():
      for action in strategy:
        assert action in actions_list
      assert len(strategy) == n
      assert len(payoff_function[strategy]) == n

  def calculate_best_response(self, scenario: List, player_index: int):
    # scenario is the list of actions by other players in order
    # scenario -> list of size n-1, n is the number of players

    strategy = scenario.copy()
    strategy.insert(player_index, 0)
    best_response = [tuple(strategy)]

    # Find the best response for each such scenario by changing my current action
    for k in range(1, len(self.actions_list)):
      strategy = scenario.copy()
      strategy.insert(player_index, k)
      if(self.payoff_function[tuple(strategy)][player_index] == self.payoff_function[best_response[0]][player_index]):
        best_response.append(tuple(strategy))
      elif (self.payoff_function[tuple(strategy)][player_index] > self.payoff_function[best_response[0]][player_index]):
        best_response = [tuple(strategy)]

    return best_response

  def calculate_nash_states(self):
    n = len(self.player_list)
    a = len(self.actions_list)
    best_responses = {}
    strategy_list = list(self.payoff_function.keys())
    strategy_list.sort()

    # For each player
    for i in range(len(self.player_list)):
      best_response_list = []

      # For each scenario -> a^(n-1) possible scenarios for each player
      for j in range(a**(n-1)):
        scenario = list(strategy_list[j][1:])
        best_response_list.extend(self.calculate_best_response(scenario, i))

      best_responses[self.player_list[i]] = best_response_list

    # Find the common set of best_reponses to find the nash equilibrium
    nash_states = set()
    for resp in best_responses.values():
      if len(nash_states) == 0:
        nash_states = set(resp)
      else:
        nash_states &= set(resp)
    return list(nash_states)
