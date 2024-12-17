from autogen import ConversableAgent, UserProxyAgent
from autogen.agentchat.contrib.multimodal_conversable_agent import (
    MultimodalConversableAgent,
)

from agentic3d._constants import LLM_CONFIG, NUM_VERSIONS


class AgentBuilder:
    """
    A class used to build and manage different types of agents.
    Methods
    -------
    __init__(generator_system_message: str, feedback_system_message: str)
        Initializes the AgentBuilder with the specified system messages for the generator
        and feedback agents.
    build_user_designer_agent()
        Builds and returns a UserProxyAgent configured as a designer agent.
    build_openscad_generator_agent(system_message: str)
        Builds and returns a ConversableAgent configured as an OpenSCAD generator agent
        with the provided system message.
    build_feedback_agent(system_message: str)
        Builds and returns a MultimodalConversableAgent configured as a feedback agent
        with the provided system message.
    print_agents()
        Prints the names of all the agents managed by the AgentBuilder.
    """

    def __init__(
        self,
        generator_system_message: str,
        feedback_system_message: str,
        prompt_improver_system_message: str,
        commander_system_message: str,
        coder_system_message: str,
        critic_system_message: str,
    ):
        """
        Initializes the agent system with the provided system messages for the generator and feedback agents.
        Args:
            generator_system_message (str): The system message to be used by the OpenSCAD generator agent.
            feedback_system_message (str): The system message to be used by the feedback agent.
        """

        self.all_agents = [
            self.build_designer_agent(),
            self.build_openscad_generator_agent(generator_system_message),
            self.build_feedback_agent(feedback_system_message),
            self.build_prompt_improver_agent(prompt_improver_system_message),
        ]

        self.all_agents_dict = {
            "user_designer_agent": self.all_agents[0],
            "openscad_generator_agent": self.all_agents[1],
            "feedback_agent": self.all_agents[2],
            "prompt_improver_agent": self.all_agents[3],
        }
        # self.all_new_agents = [
        #     self.build_commander_agent(commander_system_message),
        #     self.build_prompt_improver_agent(prompt_improver_system_message),
        #     self.build_coder_agent(coder_system_message),
        #     self.build_critic_agent(critic_system_message),
        # ]

    def build_designer_agent(self) -> UserProxyAgent:
        """
        Builds and returns a UserProxyAgent named as a designer.
        This is essentially the user who has a description they want to build using OpenSCAD.
        Returns:
            UserProxyAgent: The configured designer agent.
        """
        designerAgent = UserProxyAgent(
            name="designer",
            human_input_mode="NEVER",
            llm_config=LLM_CONFIG,
            code_execution_config=False,
            is_termination_msg=lambda x: x.get("content", "")
            and x.get("content", "").rstrip().endswith("TERMINATE"),
            max_consecutive_auto_reply=1,
        )
        return designerAgent

    def build_openscad_generator_agent(self, system_message: str) -> ConversableAgent:
        """
        Builds and returns a ConversableAgent with the role of an OpenSCAD code generator.
        This agent is responsible for generating OpenSCAD code based on the initial
        description as defined in the provided system message.
        Args:
            system_message (str): The system message to be used by the OpenSCAD generator agent.
        Returns:
            ConversableAgent: The configured OpenSCAD generator agent.
        """
        openSCAD_generatorAgent = ConversableAgent(
            name="openscad_generator",
            llm_config=LLM_CONFIG,
            system_message=system_message,
        )
        return openSCAD_generatorAgent

    def build_feedback_agent(self, system_message: str) -> MultimodalConversableAgent:
        """
        Builds and returns a MultimodalConversableAgent with the role of a feedback agent.
        This agent is responsible for providing feedback based on the image and initial
        description as defined in the provided system message.
        Args:
            system_message (str): The system message to be used by the feedback agent.
        Returns:
            MultimodalConversableAgent: The configured feedback agent.
        """
        feedbackAgent = MultimodalConversableAgent(
            name="feedback",
            llm_config=LLM_CONFIG,
            system_message=system_message,
            is_termination_msg=lambda msg: msg.get("content") is not None
            and "TERMINATE_MATCH" in msg["content"],
            human_input_mode="NEVER",
        )
        return feedbackAgent

    def build_prompt_improver_agent(self, system_message: str) -> ConversableAgent:
        promptImproverAgent = ConversableAgent(
            name="prompt_improver",
            system_message=system_message,
            llm_config=LLM_CONFIG,
            is_termination_msg=lambda msg: msg.get("content") is not None
            and "TERMINATE_MATCH" in msg["content"],
            human_input_mode="NEVER",
            max_consecutive_auto_reply=1,
        )
        return promptImproverAgent

    # def build_commander_agent(self, system_message: str) -> AssistantAgent:
    #     commanderAgent = AssistantAgent(
    #         name="commander",
    #         llm_config=LLM_CONFIG,
    #         system_message=system_message,
    #         human_input_mode="NEVER",
    #         max_consecutive_auto_reply=10,
    #     )
    #     return commanderAgent

    # def build_coder_agent(self, system_message: str) -> AssistantAgent:
    #     coderAgent = AssistantAgent(
    #         name="Coder",
    #         system_message=system_message,
    #         llm_config=LLM_CONFIG,
    #     )
    #     return coderAgent

    # def build_critic_agent(self, system_message: str) -> MultimodalConversableAgent:
    #     criticAgent = MultimodalConversableAgent(
    #         name="Critics",
    #         system_message=system_message,
    #         llm_config=LLM_CONFIG,
    #         human_input_mode="NEVER",
    #         max_consecutive_auto_reply=NUM_VERSIONS,
    #     )
    #     return criticAgent

    # def get_all_new_agents(self) -> list:
    #     return self.all_new_agents

    def get_all_agents(self) -> list:
        return self.all_agents

    def get_all_agents_dict(self) -> list:
        return self.all_agents_dict

    def print_agents(self) -> None:
        """
        Prints the names of all the agents managed by the AgentBuilder.
        """
        for agent in self.all_agents:
            print(agent.name)