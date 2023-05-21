from agent.mock_agent import MockAgent
from graph.agent_graph import AgentGraph


def test_state_flow_simple():
    """
    Test that a simple, directed graph consisting of 2 agents completes as expected
    """
    # Create initial objects
    final_output = "final_output"
    graph = AgentGraph()
    agents = MockAgent(), MockAgent(response_func=lambda _: final_output)

    # Add the agents to the graph
    for agent in agents:
        graph.add_agent(agent)

    # Add state transitions
    for i in range(len(agents) - 1):
        graph.add_transition(agents[i], agents[i + 1], pass_output=False)

    # Trigger the first agent
    graph.process(agents[0])
    assert not graph.is_busy, "Graph should not be in a 'busy' state now"

    # Check the output of the final agent
    assert agents[-1].last_response == final_output


def test_transition_pass_output():
    """
    Test output passing between agents
    """
    # Create initial objects
    final_output = "final_output"
    agents = MockAgent(), MockAgent()
    graph = AgentGraph(agents)

    # Add state transitions
    for i in range(len(agents) - 1):
        graph.add_transition(agents[i], agents[i + 1])

    # Trigger the first agent
    graph.process(agents[0], final_output)

    # Check the output of the final agent
    assert agents[-1].last_response == final_output


def test_transition_pass_transformed_output():
    """
    Test output passing between agents with some transformations applied
    """
    # Create initial objects
    test_input = "Input"
    trans_func = lambda input: input + "_Output"
    agents = [MockAgent(response_func=trans_func) for _ in range(3)]
    graph = AgentGraph(agents)

    # Add state transitions
    for i in range(len(agents) - 1):
        graph.add_transition(agents[i], agents[i + 1])

    # Trigger the first agent
    graph.process(agents[0], test_input)

    # Check the output of the final agent
    assert agents[-1].last_response == test_input + "_Output" * 3


def test_simple_tags():
    """
    Test output passing between agents with some transformations applied
    """
    # Create initial objects
    test_input = "Input"
    trans_func = lambda input: input + "_Output"
    agents = [MockAgent(response_func=trans_func) for _ in range(3)]
    graph = AgentGraph(agents)

    # Add state transitions
    for i in range(len(agents) - 1):
        graph.add_transition(agents[i], agents[i + 1])

    # Trigger the first agent
    graph.process(agents[0], test_input)

    # Check the output of the final agent
    assert agents[-1].last_response == test_input + "_Output" * 3