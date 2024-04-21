from uagents import Agent, Context, Protocol
from messages import UAgentResponse, UAgentResponseType, KeyValue
from uagents.setup import fund_agent_if_low
from utils.llm import get_llm
import asyncio
import os


TOP_ACTIVITIES_SEED = os.getenv("TOP_ACTIVITIES_SEED", "top_activities really secret phrase :)")

intermediary_agent =  "agent1q0wf3xa58qfn8eayxcn7xhlxl8qhpjnkfdtwpru987afat9wrkxrstxs9q8"

agent = Agent(
    name="top_activities",
    seed=TOP_ACTIVITIES_SEED
)

fund_agent_if_low(agent.wallet.address())

llm = get_llm()
top_activities_protocol = Protocol("TopActivities")

# @top_activities_protocol.on_message(model=TopActivities, replies=UAgentResponse)
@top_activities_protocol.on_query(model=UAgentResponse, replies=UAgentResponse)
async def get_top_activities(ctx: Context, sender: str, msg: UAgentResponse):
    ctx.logger.info(f"Received message from {sender}, session: {ctx.session}")
    prompt = f"""You specialize in recommending tourist activities based on user preferences. If no specifics are given, suggest popular activities at major destinations. If user input is available, provide tailored activity suggestions. Include a brief description for each activity. List all suggestions with each activity separated by a new line and finish with 'END'. User preferences: {msg.message}. Plaintext answer without any special characters. Concise answer around 50 words"""
    try:
        print("Before llm.comlete (activities)")
        response = await llm.complete("", prompt, "Response:", max_tokens=4096, stop=["\n\nEND"])
        print("Before ctx.send (activities)")
        result = response.strip()

        ctx.logger.info(result)
        #TODO: send as json to UI
        final_result = result
        # result = result.split("\n")
        await ctx.send(
            sender,
            UAgentResponse(
                message=final_result,
                # options=list(map(lambda x: KeyValue(key=x, value=x), result)),
                type=UAgentResponseType.FINAL_OPTIONS
            )
        )
    except Exception as exc:
        ctx.logger.warn(f"{exc}")
        await ctx.send(sender, UAgentResponse(message=str(exc), type=UAgentResponseType.ERROR))

agent.include(top_activities_protocol)