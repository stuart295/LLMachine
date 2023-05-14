import networkx as nx

from agent.base_agent import BaseAgent
import logging

class AgentGraph:

    def __init__(self, max_steps=25):
        self.is_busy = False
        self.graph = nx.DiGraph()
        self._processing_agent = None
        self.max_steps = max_steps
        self.log = logging.Logger("AgentGraph")

    def add_agent(self, agent: BaseAgent):
        self.graph.add_node(agent)

    def add_transition(self, from_agent: BaseAgent, to_agent: BaseAgent):
        self.graph.add_edge(from_agent, to_agent)

    def process(self, start_agent: BaseAgent):
        assert start_agent in self.graph, "start agent is not in this graph!"

        self.is_busy = True
        self._processing_agent = start_agent

        # Main processing loop
        for step in range(self.max_steps):
            agent_response = self._processing_agent.listen()

            # TODO Tag handling, etc

            # If no, outgoing edges, complete
            if self.graph.out_degree(self._processing_agent) == 0:
                self.is_busy = False
                return

            # TODO For now just transition if there is one
            self._processing_agent = next(self.graph.successors(self._processing_agent))

        # The function should return before exceeding the step limit
        self.log.error("Graph processing exceeeded maximum steps!")





