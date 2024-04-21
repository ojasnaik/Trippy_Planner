from uagents import Agent, Context, Protocol
from messages import UAgentResponse, UAgentResponseType, KeyValue
from uagents.setup import fund_agent_if_low
from utils.llm import get_llm
# from utils.llm_gemini import get_llm
import asyncio
import os


ITERNARY_SEED = os.getenv("ITERNARY_SEED", "iternary really secret phrase :)")

agent = Agent(
    name="iternary_agent",
    seed=ITERNARY_SEED
)

intermediary_agent =  "agent1q0wf3xa58qfn8eayxcn7xhlxl8qhpjnkfdtwpru987afat9wrkxrstxs9q8"

fund_agent_if_low(agent.wallet.address())

llm = get_llm()
iternary_protocol = Protocol("Iternary")

@iternary_protocol.on_message(model=UAgentResponse, replies=UAgentResponse)
async def get_top_destinations(ctx: Context, sender: str, msg: UAgentResponse):
    ctx.logger.info(f"Received message from {sender}, session: {ctx.session}")
    prompt = f"""You are an expert AI agent in suggesting itinerary based on a given conversation between the user and AI agents. You will summarize the conversation into a single itinerary, tailor the itinerary accordingly and conclude with 'END'. User conversation: {msg.message}
"""
    print(f"All Prompts before iternary: {msg.message}")
    try:
        print("Before llm.comlete")
        response = await llm.complete("", prompt, "Response:", max_tokens=4096, stop=["\n\nEND"])
        print("Before ctx.send")
        result = response.strip()
        # result = result.split("\n")
        await ctx.send(
            "agent1qd99csvyam42gpts65h3ghk95uqm5hwumvaqvf3mq43qesngj2ufkq0w4wy",
            UAgentResponse(
                # options=list(map(lambda x: KeyValue(key=x, value=x), result)),
                message=result,
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
