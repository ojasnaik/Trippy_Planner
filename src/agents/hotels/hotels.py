from uagents import Agent, Context, Protocol
from messages import UAgentResponse, UAgentResponseType, KeyValue
from uagents.setup import fund_agent_if_low
from utils.llm import get_llm
import asyncio
import os


TOP_HOTELS_SEED = os.getenv("TOP_HOTELS_SEED", "top_hotels really secret phrase :)")

intermediary_agent =  "agent1q0wf3xa58qfn8eayxcn7xhlxl8qhpjnkfdtwpru987afat9wrkxrstxs9q8"

agent = Agent(
    name="top_hotels",
    seed=TOP_HOTELS_SEED
)

fund_agent_if_low(agent.wallet.address())

llm = get_llm()
top_hotels_protocol = Protocol("TopHotels")

@top_hotels_protocol.on_message(model=UAgentResponse, replies=UAgentResponse)
async def get_top_hotels(ctx: Context, sender: str, msg: UAgentResponse):
    ctx.logger.info(f"Received message from {sender}, session: {ctx.session}")
    prompt = f"""You assist in finding suitable hotels based on user preferences. Suggest popular hotels if no user input is given. With specifics, provide options that match the desired amenities, location, and price range. Each hotel should be listed with a brief description. Separate each suggestion with a new line and conclude with 'END'. User preferences: {msg.message}"""
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

agent.include(top_hotels_protocol)