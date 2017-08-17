from Agent import Agent
from Environment import Environment
from GraphicUtility import GraphicUtility

if __name__ == "__main__":
    env = Environment()
    agent = Agent(env)
    util = GraphicUtility('Policy Iteration', agent)
    util.main_loop()
