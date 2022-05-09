from typing import Callable, Dict, List, Tuple
import random


class Agent:

  def __init__(self, player_id: int, strategy_name: str, strategy: Callable):
    self.strategy_name = strategy_name
    self.strategy = strategy
    self.player_id = player_id
    self.payoff_history = []

  def update_game(self, payoff):
    self.payoff_history.append(payoff)

  def get_avg_payoff(self):
    return sum(self.payoff_history)/len(self.payoff_history)
  

class AgentSet:

  def __init__(self, agent_distribution: Dict[str, int], strategy_function: Dict[str, Callable]):
    self.agent_set = {}
    self.agent_count = 0
    self.strategy_function = strategy_function
    for strategy_name in agent_distribution.keys():
      self.agent_set[strategy_name] = []
      for _ in range(agent_distribution[strategy_name]):
        self.agent_set[strategy_name].append(Agent(self.agent_count, strategy_name, self.strategy_function[strategy_name]))
        self.agent_count += 1

  def fetch_agent_list(self):
    agent_list = []
    for lst in self.agent_set.values():
      agent_list.extend(lst)
    random.shuffle(agent_list)
    return agent_list

  def get_total_strategy_payoff(self):
    total_strategy_payoff = {}
    for strategy in self.agent_set.keys():
      agent_list = self.agent_set[strategy]
      total_payoff = sum([agent.get_avg_payoff() for agent in agent_list])
      total_strategy_payoff[strategy] = total_payoff
    
    return total_strategy_payoff

  def get_agent_distribution(self, avg_strategy_payoff):
    total_payoff = sum(avg_strategy_payoff.values())
    agent_distribution = {}
    strategy_list = list(self.strategy_function.keys())
    curr_sum = 0
    for i in range(len(strategy_list)-1):
      val = round((avg_strategy_payoff[strategy_list[i]]/total_payoff)*self.agent_count)
      agent_distribution[strategy_list[i]] = val
      curr_sum += val
      
    agent_distribution[strategy_list[-1]] = self.agent_count - curr_sum

    assert sum(agent_distribution.values()) == self.agent_count

    return agent_distribution

  def update_generation(self):
    avg_strategy_payoff = self.get_total_strategy_payoff()

    agent_distribution = self.get_agent_distribution(avg_strategy_payoff)

    self.agent_set = {}
    self.agent_count = 0
    for strategy_name in agent_distribution.keys():
      self.agent_set[strategy_name] = []
      for _ in range(agent_distribution[strategy_name]):
        self.agent_set[strategy_name].append(Agent(self.agent_count, strategy_name, self.strategy_function[strategy_name]))
        self.agent_count += 1


  def print_generation_data(self, curr_gen, match_ups_count):
    total_strategy_payoff = self.get_total_strategy_payoff()
    print("-"*100)
    print("Generation {}:".format(curr_gen))
    for strategy in self.agent_set.keys():
      print("{} has {} number of agents with total payoff : {}".format(strategy, len(self.agent_set[strategy]), total_strategy_payoff[strategy]))
    for match_up in match_ups_count.keys():
      print("Number of matches with {} : {}".format(match_up, sum(match_ups_count[match_up])))
    print("-"*100)


class EvolutionaryGame:
  
  def __init__(self, generations_count: int, game_count: int, iter_count: int, strategy_function: Dict[str, Callable], agent_distribution: Dict[str, int], payoff_function: Dict[Tuple, List[float]]):
    self.generations_count = generations_count
    self.game_count = game_count
    self.iter_count = iter_count
    self.strategy_function = strategy_function
    self.payoff_function = payoff_function
    self.agent_distribution = agent_distribution
    EvolutionaryGame.validate(strategy_function, agent_distribution, payoff_function)
    self.agent_set = AgentSet(self.agent_distribution, self.strategy_function)

  @staticmethod
  def validate(strategy_function: Dict[str, Callable], agent_distribution: Dict[str, int], payoff_function: Dict[Tuple, List[float]]):
    for key in payoff_function.keys():
      assert len(key) == 2
      assert len(payoff_function[key]) == 2
    strategies = set(strategy_function.keys())
    assert strategies == set(agent_distribution.keys())
    assert sum(agent_distribution.values()) % 2 == 0

  @staticmethod
  def match_pairs(agent_list: List[Agent]):
    def pop_random(lst: List[Agent]):
      idx = random.randrange(0, len(lst))
      return lst.pop(idx)

    lst = agent_list.copy()
    pairs = []
    while lst:
      rand1 = pop_random(lst)
      rand2 = pop_random(lst)
      pair = (rand1, rand2)
      pairs.append(pair)

    return pairs

  @staticmethod
  def play_game(iter_count, agent1: Agent, agent2: Agent, payoff_function: Dict[Tuple, List[float]]):
    player_list = [agent1, agent2]
    player_list_id = [agent1.player_id, agent2.player_id]
    history = {}
    players_payoff = {}
    players_total_payoff = []
    for player in player_list:
      history[player.player_id] = []
      players_payoff[player.player_id] = []
      players_total_payoff.append(0)

    for _ in range(iter_count):
      game_action = ()
      for player in player_list:
        action = player.strategy(player.player_id, player_list_id, history)
        game_action += (action, )

      for player_num in range(len(player_list)):
        history[player_list_id[player_num]].append(game_action[player_num])
        players_payoff[player_list_id[player_num]].append(payoff_function[game_action][player_num])
        players_total_payoff[player_num] += payoff_function[game_action][player_num]
    
    return players_total_payoff

  @staticmethod
  def create_match_count(strategy_list):
    match_ups_count = {}
    for i in range(len(strategy_list)):
      for j in range(len(strategy_list)):
        match_ups_count[(strategy_list[i], strategy_list[j])] = []

    return match_ups_count

  def simulate(self):
    for curr_gen in range(self.generations_count):
      match_ups_count = EvolutionaryGame.create_match_count(list(self.strategy_function.keys()))
      for curr_game in range(self.game_count):
        
        for pair in match_ups_count.keys():
          match_ups_count[pair].append(0)

        game_pairs = EvolutionaryGame.match_pairs(self.agent_set.fetch_agent_list())
  
        for pair in game_pairs:
          strategy_pair = (pair[0].strategy_name, pair[1].strategy_name)
          match_ups_count[strategy_pair][curr_game] += 1
          payoff_list = EvolutionaryGame.play_game(self.iter_count, pair[0], pair[1], self.payoff_function)
          pair[0].update_game(payoff_list[0])
          pair[1].update_game(payoff_list[1])

      self.agent_set.print_generation_data(curr_gen, match_ups_count)
      self.agent_set.update_generation()