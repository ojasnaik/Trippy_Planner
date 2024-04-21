from uagents import Agent, Context, Protocol
from messages import UAgentResponse, UAgentResponseType, KeyValue
from uagents.setup import fund_agent_if_low
from utils.llm import get_llm
import asyncio
import os


TOP_FLIGHTS_SEED = os.getenv("TOP_FLIGHTS_SEED", "top_flights really secret phrase :)")

intermediary_agent =  "agent1q0wf3xa58qfn8eayxcn7xhlxl8qhpjnkfdtwpru987afat9wrkxrstxs9q8"

agent = Agent(
    name="top_flights",
    seed=TOP_FLIGHTS_SEED
)

fund_agent_if_low(agent.wallet.address())

llm = get_llm()
top_flights_protocol = Protocol("TopFlights")

# @top_flights_protocol.on_message(model=TopFlights, replies=UAgentResponse)
@top_flights_protocol.on_message(model=UAgentResponse, replies=UAgentResponse)
async def get_top_flights(ctx: Context, sender: str, msg: UAgentResponse):
    ctx.logger.info(f"Received message from {sender}, session: {ctx.session}")
    prompt = f"""You are programmed to find the best flight options for users. If no specifics are given, suggest popular flight routes. When user preferences are provided, search for flights that match their itinerary and budget constraints. Display options in a list format, each separated by a new line, and end with 'END'. User preferences: {msg.message}"""
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

agent.include(top_flights_protocol)