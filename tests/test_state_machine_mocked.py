from agent.mock_agent import MockAgent
from graph.agent_graph import AgentGraph


def test_state_flow_simple():
    """
    Test that a simple, directed graph consisting of 2 agents completes as expected
    """
    # Create initial objects
    final_output = "final_output"
    graph = AgentGraph()
    agents = MockAgent("0"), MockAgent("1", response_func=lambda _: final_output)

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
    agents = MockAgent("0"), MockAgent("1")
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
    agents = [MockAgent(str(i), response_func=trans_func) for i in range(3)]
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
    test_input = "Go [LEFT]"
    input_agent = MockAgent("input")
    left_agent = MockAgent("left")
    right_agent = MockAgent("right")
    graph = AgentGraph([input_agent, left_agent, right_agent])

    # Add state transitions
    graph.add_transition(input_agent, right_agent)
    graph.add_transition(input_agent, left_agent, tag="[LEFT]")

    # Trigger the first agent
    graph.process(input_agent, test_input)

    # Check the output of the final agent
    assert left_agent.last_response == test_input, "Left agent should have been called"
    assert right_agent.last_response is None, "Right agent should not have been called"


def test_self_transitions(caplog):
    """
    Test graph with transitions to self
    """
    # Create initial objects
    test_input = "0"

    def response_func(input):
        val = int(input)
        if val < 5:
            return str(val + 1)
        return "[DONE]"

    input_agent = MockAgent("input", response_func=response_func)
    output_agent = MockAgent("output")
    graph = AgentGraph([input_agent, output_agent])

    # Add state transitions
    graph.add_transition(input_agent, input_agent)
    graph.add_transition(input_agent, output_agent, tag="[DONE]")

    # Trigger the first agent
    graph.process(input_agent, test_input)

    # Check the output of the final agent
    assert input_agent.input == "5"
    assert input_agent.last_response == "[DONE]"
    assert output_agent.last_response == "[DONE]"

    assert "Graph processing exceeeded maximum steps!" not in caplog.text
