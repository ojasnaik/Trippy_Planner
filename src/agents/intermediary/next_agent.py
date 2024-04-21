from uagents import Agent, Context, Protocol
from messages import UAgentResponse, UAgentResponseType, KeyValue
from uagents.setup import fund_agent_if_low
from utils.llm import get_llm
# from utils.llm_gemini import get_llm
import asyncio
import os


INTERMEDIARY_SEED = os.getenv("INTERMEDIARY_SEED", "intermediary really secret phrase :)")

agent = Agent(
    name="next_agent",
    seed=INTERMEDIARY_SEED
)
iternary_agent = "agent1q2gam6vqryy7zk34n6crf4tpg7ld72deg6hzcvu4jd2ej34aqpayynmz788"

fund_agent_if_low(agent.wallet.address())

llm = get_llm()
next_agent_protocol = Protocol("Intermediary")

agents = {
    "top_destination_agent": "agent1qd2jvf7r3k25x03pcu8920xf7geeeuw3cheqymqejhjj4zcluq8xj9lfld2",
    "iternary_agent": "agent1q2gam6vqryy7zk34n6crf4tpg7ld72deg6hzcvu4jd2ej34aqpayynmz788",
    "client_agent": "agent1qd99csvyam42gpts65h3ghk95uqm5hwumvaqvf3mq43qesngj2ufkq0w4wy",
    "top_activities_agent": "agent1qvdrwyl2svkfsg248xwwp386gxn0qnpp7q7hppv9yqn9vke9a7lkvu8t6cq",
    "hotels_agent": "agent1qw38uyxt0cwsg0ctzzdpgh290986kkaq8xht44w98xnde8z9xxsjwl3lkgu",
    "dining_agent": "agent1qgy3fp93tnr96djxf9rcnz3w22eu4sp4pwu3qx7q8awu959nehy96lv830h",
    "flights_agent": "agent1q2sd7qx74e05s6zhzuvduk9d04g5cka5rew84n0u5v8ml2j0vv3v2plpjs3"
}

@next_agent_protocol.on_message(model=UAgentResponse, replies=UAgentResponse)
async def get_next_agent(ctx: Context, sender: str, msg: UAgentResponse):
    ctx.logger.info(f"Received message from {sender}, session: {ctx.session}")
    
    user_input = input("\nSo what's on your mind (next)? Need any suggestions on which city to visit? Want to know about flights? Need to know about hotels? Curious about activities or attractions? If you are satisified by the current itenary then enter 'yes', else lets continue chatting \n")
    
    print("User input: ", user_input)
    if(user_input == 'yes'):
        await ctx.send(iternary_agent, 
                UAgentResponse(
                # options=list(map(lambda x: KeyValue(key=x, value=x), result)),
                message=msg.message,
                type=UAgentResponseType.FINAL_OPTIONS
            ))
        return

    final_message = msg.message + "\n" + user_input

    prompt = f"""You have 6 AI agents working for you to suggest the user a travel itinerary. Each serving a given purpose. The following are the names of the 6 AI Agents with their functionality: 
    * top_destination_agent - suggests user which place to visit
    * top_activities_agent  - suggests users what tourist fun activities user could DO while visiting the place
    * top_attractions_agent - suggests users what are the tourist attractions the user could go to while visiting the place
    * flights_agent - suggests users flights that they can take from their current location to their destination
    * hotels_agent - suggests the user the hotels in which they can live while staying at the city at which they plan to visit
    * dining_agent - suggests the user the places where he or she could go to grab some food in the place they are planning on visiting based on their preferences 
    /n
    Here is the conversation that you have had with the user till now: {final_message}
    Your job is to call the correct AI Agent that would best serve the user. Tell me which AI Agent should be called from the above mentioned 6 AI Agents (top_destination_agent, top_activities_agent, top_attractions_agent, flights_agent, hotels_agent, dining_agent).
    Remember you have to very strictly return your reponse in a single word. This single word must be the name of one of the 6 AI Agents best suited to serve the user now.
    """
    try:
        print("Before llm.complete next_agent")
        response = await llm.complete("", prompt, "Response:", max_tokens=4096, stop=["END"])
        print("Before ctx.send")
        result = response.strip()
        # result = result.split("\n")
        print(result)
        agent_name = result
        print("Agent id: ", agents[agent_name])
        await ctx.send(
            agents[agent_name],
            UAgentResponse(
                # options=list(map(lambda x: KeyValue(key=x, value=x), result)),
                message=final_message,
                type=UAgentResponseType.FINAL_OPTIONS
            )
        )

    # except openai.InvalidRequestError as e:
    #     print("Invalid request:", e)
    # except openai.Error as e:
    #     print("OpenAI API error:", e)
    except Exception as exc:
        ctx.logger.warn(f"olem iter {exc}")
        await ctx.send(sender, UAgentResponse(message=str(exc), type=UAgentResponseType.ERROR))

agent.include(next_agent_protocol)
