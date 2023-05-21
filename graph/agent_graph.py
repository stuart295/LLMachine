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
        self.graph.add_node(agent.id, instance=agent)

    def add_agents(self, agents):
        if not agents:
            return

        for agent in agents:
            self.add_agent(agent)

    def add_transition(self, from_agent: BaseAgent, to_agent: BaseAgent, pass_output=True, tag: str = None):
        self.graph.add_edge(from_agent.id, to_agent.id, pass_output=pass_output, tag=tag)

    def get_agent(self, id: str):
        return self.graph.nodes[id]["instance"]

    def process(self, start_agent: BaseAgent, input_message: str = None):
        assert start_agent.id in self.graph, "start agent is not in this graph!"

        self.is_busy = True
        self._processing_agent = start_agent

        if input_message:
            self._processing_agent.tell(input_message)

        # Main processing loop
        for step in range(self.max_steps):
            agent_response = self._processing_agent.listen()

            # If no, outgoing edges, complete
            if self.graph.out_degree(self._processing_agent.id) == 0:
                self.is_busy = False
                return

            # Use tags to determine transition
            next_agent = self.find_transition(agent_response)

            if not next_agent:
                # No transitions, finish
                self.is_busy = False
                return

            # Handle transition
            transition = self.graph.edges[(self._processing_agent.id, next_agent.id)]
            if transition["pass_output"]:
                next_agent.tell(agent_response)

            self._processing_agent = next_agent

        # The function should return before exceeding the step limit
        self.log.error("Graph processing exceeeded maximum steps!")

    def find_transition(self, agent_response: str) -> BaseAgent:
        """
        Determines the next agent to transition to based on the current agent's response
        """
        # TODO Inefficient approach for initial prototyping. Rewrite.
        next_agent, next_agent_default = None, None
        for (_, successor_id, data) in self.graph.out_edges(self._processing_agent.id, data=True):
            tag = data["tag"]
            if tag is None:
                next_agent_default = self.get_agent(successor_id)
                continue

            if tag in agent_response:
                next_agent = self.get_agent(successor_id)
                break

        return next_agent or next_agent_default
