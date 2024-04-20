from uagents import Agent, Context, Protocol
from messages import UAgentResponse, UAgentResponseType, KeyValue
from uagents.setup import fund_agent_if_low
from utils.llm import get_llm
# from utils.llm_gemini import get_llm
import asyncio
import os


ITERNARY_SEED = os.getenv("ITERNARY_SEED", "iternary really secret phrase :)")

agent = Agent(
    name="iteranry_agent",
    seed=ITERNARY_SEED
)

fund_agent_if_low(agent.wallet.address())

llm = get_llm()
iternary_protocol = Protocol("Iternary")

@iternary_protocol.on_message(model=UAgentResponse, replies=UAgentResponse)
async def get_top_destinations(ctx: Context, sender: str, msg: UAgentResponse):
    ctx.logger.info(f"Received message from {sender}, session: {ctx.session}")
    prompt = f"""You are an expert AI in suggesting an holiday schedule based on some user input of preferred destinations and no of travel days.
User input for dates might not be provided, in which case suggest popular schedule of 3 days. 
If user input for days is present, then suggest a schedule based on user input.
After listing all the suggestions say END. Schedule should be properly formatted.

User preferences: {msg.options}
"""
    try:
        print("Before llm.comlete")
        response = await llm.complete("", prompt, "Response:", max_tokens=500, stop=["END"])
        print("Before ctx.send")
        result = response.strip()
        result = result.split("\n")
        await ctx.send(
            "agent1qd99csvyam42gpts65h3ghk95uqm5hwumvaqvf3mq43qesngj2ufkq0w4wy",
            UAgentResponse(
                options=list(map(lambda x: KeyValue(key=x, value=x), result)),
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

agent.include(iternary_protocol)
