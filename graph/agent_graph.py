import networkx as nx

from agent.base_agent import BaseAgent
import logging

class AgentGraph:

    def __init__(self, agents=None, max_steps=25):
        self.is_busy = False
        self.graph = nx.DiGraph()
        self._processing_agent = None
        self.max_steps = max_steps
        self.log = logging.Logger("AgentGraph")
        self.add_agents(agents)

    def add_agent(self, agent: BaseAgent):
        self.graph.add_node(agent)

    def add_agents(self, agents):
        if not agents:
            return

        for agent in agents:
            self.add_agent(agent)

    def add_transition(self, from_agent: BaseAgent, to_agent: BaseAgent, pass_output=True):
        self.graph.add_edge(from_agent, to_agent, pass_output=pass_output)

    def process(self, start_agent: BaseAgent, input_message:str = None):
        assert start_agent in self.graph, "start agent is not in this graph!"

        self.is_busy = True
        self._processing_agent = start_agent

        if input_message:
            self._processing_agent.tell(input_message)

        # Main processing loop
        for step in range(self.max_steps):
            agent_response = self._processing_agent.listen()

            # TODO Tag handling, etc

            # If no, outgoing edges, complete
            if self.graph.out_degree(self._processing_agent) == 0:
                self.is_busy = False
                return

            # TODO For now just transition if there is one
            next_agent: BaseAgent = next(self.graph.successors(self._processing_agent))
            transition = self.graph.edges[(self._processing_agent, next_agent)]
            if transition["pass_output"]:
                next_agent.tell(agent_response)

            self._processing_agent = next_agent

        # The function should return before exceeding the step limit
        self.log.error("Graph processing exceeeded maximum steps!")





