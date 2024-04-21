from messages import UAgentResponse, UAgentResponseType
from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
import os

TOP_DESTINATIONS_CLIENT_SEED = os.getenv("TOP_DESTINATIONS_CLIENT_SEED", "top_destinations_client really secret phrase :)")

top_dest_client = Agent(
    name="top_destinations_client",
    port=8008,
    seed=TOP_DESTINATIONS_CLIENT_SEED,
    endpoint=["http://127.0.0.1:8008/submit"],
)
fund_agent_if_low(top_dest_client.wallet.address())

intermediary_agent =  "agent1q0wf3xa58qfn8eayxcn7xhlxl8qhpjnkfdtwpru987afat9wrkxrstxs9q8"
iternary_agent = "agent1q2gam6vqryy7zk34n6crf4tpg7ld72deg6hzcvu4jd2ej34aqpayynmz788"

print(f"Top dest client address: {top_dest_client.address}")

# # TODO: CALL INTERMEDIATERY AGENT


# top_dest_request = TopDestinations(preferences="new york")

@top_dest_client.on_event("startup")
async def send_message(ctx: Context):

    # user_input = input("So what's on your mind (next)? Need any suggestions on which city to visit? Want to know about flights? Need to know about hotels? Curious about activities or attractions? If you are satisified by the current itenary then enter 'yes', else lets continue chatting")
    # if(user_input == 'yes'):
    #     await ctx.send(iternary_agent, top_dest_request)
    # else:
    await ctx.send(intermediary_agent, UAgentResponse(
                message="",
                # options=list(map(lambda x: KeyValue(key=x, value=x), result)),
                type=UAgentResponseType.FINAL_OPTIONS
            ))

@top_dest_client.on_message(model=UAgentResponse)
async def message_handler(ctx: Context, _: str, msg: UAgentResponse):
    ctx.logger.info(f"\nThis is your final travel plan: {msg.message}")
    

if __name__ == "__main__":
    top_dest_client.run()
