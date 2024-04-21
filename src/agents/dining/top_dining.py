from uagents import Agent, Context, Protocol
from messages import UAgentResponse, UAgentResponseType, KeyValue
from uagents.setup import fund_agent_if_low
from utils.llm import get_llm
import asyncio
import os


TOP_DINING_SEED = os.getenv("TOP_DINING_SEED", "top_dining really secret phrase :)")

intermediary_agent =  "agent1q0wf3xa58qfn8eayxcn7xhlxl8qhpjnkfdtwpru987afat9wrkxrstxs9q8"

agent = Agent(
    name="top_dining",
    seed=TOP_DINING_SEED
)

fund_agent_if_low(agent.wallet.address())

llm = get_llm()
top_dining_protocol = Protocol("TopDining")

@top_dining_protocol.on_message(model=UAgentResponse, replies=UAgentResponse)
async def get_top_dining(ctx: Context, sender: str, msg: UAgentResponse):
    ctx.logger.info(f"Received message from {sender}, session: {ctx.session}")
    prompt = f"""You recommend dining options based on user preferences. In the absence of specific requests, suggest popular dining spots. With user input, provide recommendations that suit their dietary needs and taste. Also consider their budget and the city or destination they are planning on visiting (these details will be provided after "User preferences". Include a brief description for each restaurant. List your suggestions with each separated by a new line and end with 'END'. User preferences: {msg.message}"""
    try:
        print("Before llm.comlete (activities)")
        response = await llm.complete("", prompt, "Response:", max_tokens=4096, stop=["\n\nEND"])
        print("Before ctx.send (activities)")
        result = response.strip()

        ctx.logger.info(result)
        #TODO: send as json to UI
        final_result = msg.message + "\n" + result
        # result = result.split("\n")
        await ctx.send(
            intermediary_agent,
            UAgentResponse(
                message=final_result,
                # options=list(map(lambda x: KeyValue(key=x, value=x), result)),
                type=UAgentResponseType.FINAL_OPTIONS
            )
        )
    except Exception as exc:
        ctx.logger.warn(f"{exc}")
        await ctx.send(sender, UAgentResponse(message=str(exc), type=UAgentResponseType.ERROR))

agent.include(top_dining_protocol)