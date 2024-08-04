import os
import autogen
import chainlit as cl
from chainlit_agents import ChainlitUserProxyAgent, ChainlitAssistantAgent

api_key = os.getenv('API_KEY')

config_list_openai = [
    {"model": "gpt-4o", "api_key": api_key}
]

llm_config = {
    "seed": 221,  # change the seed for different trials
    "temperature": 0,
    "config_list": config_list_openai,
    "timeout": 60000,
}

USER_PROXY_MESSAGE = '''A human admin. Interact with the planner to discuss the plan. 
Plan execution needs to be approved by this admin.'''

ENGINEER_MESSAGE = '''Engineer. You follow an approved plan. You write python/shell code to solve tasks. 
Wrap the code in a code block that specifies the script type. The user can't modify your code. 
So do not suggest incomplete code which requires others to modify. Don't use a code block if it's 
not intended to be executed by the executor. Don't include multiple code blocks in one response. 
Do not ask others to copy and paste the result. Check the execution result returned by the executor. 
If the result indicates there is an error, fix the error and output the code again. 
Suggest the full code instead of partial code or code changes. If the error can't be fixed or if 
the task is not solved even after the code is executed successfully, analyze the problem, 
revisit your assumption, collect additional info you need, and think of a different approach to try.
In the code you write, always add a part to report the solution on the boundaries and store it in a seperated file for the Scientist to check.'''

PLANNER_MESSAGE = """Planner. Suggest a plan. Revise the plan based on feedback from admin and critic, until admin approval.
The plan may involve an engineer who can write code and a scientist who doesn't write code.
Explain the plan first. Ask Executor to install any python libraries or modules as needed without human input. 
Be clear which step is performed by an engineer, and which step is performed by a scientist."""

SCIENTIST_MESSAGE = """Scientist. You follow an approved plan. You are able to formulate the mechanics problem with 
clear boundary condition and constitutive law of materails. You don't write code. You explicit check the 
boundary results from the Engineer to see whether it agrees with the input boundary condition. 
When you excute the code, always save a copy for review."""

EXECUTOR_MESSAGE = """Executor. Save and execute the code written by the engineer and report and save the result. 
Use both bash and python lanuage interpretor."""

CRITIC_MESSAGE = """Critic. Double check plan, claims, code from other agents, results on the boundary conditions and provide feedback. 
Check whether the plan includes adding verifiable info such as source URL."""
                                  
@cl.on_chat_start
async def on_chat_start():
  try:
    print("Set agents.")
    user_proxy  = ChainlitUserProxyAgent("Admin", system_message=USER_PROXY_MESSAGE, code_execution_config=False)
    engineer    = ChainlitAssistantAgent("Engineer", llm_config=llm_config, system_message=ENGINEER_MESSAGE)
    scientist   = ChainlitAssistantAgent("Scientist", llm_config=llm_config, system_message=SCIENTIST_MESSAGE)
    planner     = ChainlitAssistantAgent("Planner",llm_config=llm_config, system_message=PLANNER_MESSAGE)
    critic      = ChainlitAssistantAgent("Critic", llm_config=llm_config, system_message=CRITIC_MESSAGE)
    executor    = ChainlitAssistantAgent("Executor", system_message=EXECUTOR_MESSAGE, human_input_mode="NEVER",
                                    code_execution_config={"last_n_messages": 3, "work_dir": "FEA_results","use_docker": False})    

    cl.user_session.set("user_proxy", user_proxy)
    cl.user_session.set("engineer", engineer)
    cl.user_session.set("scientist", scientist)
    cl.user_session.set("planner", planner)
    cl.user_session.set("critic", critic)
    cl.user_session.set("executor", executor)

    msg = cl.Message(content=f"""Hello! What simulation task would you like to get done today?      
                     """, 
                     author="User_Proxy")
    await msg.send()
    
  except Exception as e:
    print("Error: ", e)
    pass

@cl.on_message
async def run_conversation(message: cl.Message):
    MAX_ITER = 50
    CONTEXT = message.content   
    user_proxy  = cl.user_session.get("user_proxy")
    planner     = cl.user_session.get("planner")
    engineer    = cl.user_session.get("engineer")
    critic      = cl.user_session.get("critic")
    executor    = cl.user_session.get("executor")
    scientist   = cl.user_session.get("scientist")
    groupchat   = autogen.GroupChat(agents=[user_proxy, planner, engineer, scientist, executor, critic], 
                                    messages=[], max_round=MAX_ITER)
    manager     = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

    print("Running conversation")
    await cl.make_async(user_proxy.initiate_chat)( manager, message=CONTEXT, )
      