from agent.mock_agent import MockAgent
from graph.agent_graph import AgentGraph


def test_state_flow_simple():
    """
    Test that a simple, directed graph consisting of 3 agents completes as expected
    """
    # Create initial objects
    scratchpad_name = "output"
    final_output = "final_output"
    graph = AgentGraph()
    agents = MockAgent(), MockAgent(), MockAgent(response_func=lambda _: final_output)

    # Add the agents to the graph
    for agent in agents:
        graph.add_agent(agent)

    # Add state transitions
    for i in range(len(agents)-1):
        graph.add_transition(agents[i], agents[i+1])

    # Trigger the first agent
    graph.process(agents[0])
    assert not graph.is_busy, "Graph should not be in a 'busy' state now"

    # Check the output of the final agent
    assert agents[-1].last_response == final_output
