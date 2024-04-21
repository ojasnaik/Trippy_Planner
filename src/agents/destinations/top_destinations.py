from uagents import Agent, Context, Protocol
from messages import UAgentResponse, UAgentResponseType, KeyValue
from uagents.setup import fund_agent_if_low
from utils.llm import get_llm
# from utils.llm_gemini import get_llm
import asyncio
import os


TOP_DESTINATIONS_SEED = os.getenv("TOP_DESTINATIONS_SEED", "top_destinations really secret phrase :)")

agent = Agent(
    name="top_destinations",
    seed=TOP_DESTINATIONS_SEED
)

intermediary_agent =  "agent1q0wf3xa58qfn8eayxcn7xhlxl8qhpjnkfdtwpru987afat9wrkxrstxs9q8"

fund_agent_if_low(agent.wallet.address())

llm = get_llm()
top_destinations_protocol = Protocol("TopDestinations")

@top_destinations_protocol.on_message(model=UAgentResponse, replies=UAgentResponse)
async def get_top_destinations(ctx: Context, sender: str, msg: UAgentResponse):
    ctx.logger.info(f"Received message from {sender}, session: {ctx.session}")
    prompt = f"""You are an expert AI agent in suggesting which destination the user should go to. User input may or may not be provided. Without user input, suggest popular destinations. With user input, tailor your suggestion accordingly. Provide a brief description for the destination explaining why it is recommended. Example response based on user preferences: {msg.message}
"""
    try:
        print("Before llm.comlete")
        print("Prompt: ", prompt)
        response = await llm.complete("", prompt, "Response:", max_tokens=4096, stop=["END"])
        print("Before ctx.send")
        result = response.strip()
        ctx.logger.info(result)
        #TODO: send as json to UI
        final_result = msg.message + "\n" + result
        # result = result.split("\n")
        # results = list(map(lambda x: KeyValue(key=x, value=x), result))
        # iternary_request = Iternary(destinations="Aspen, Colorado, USA. Aspen is a beautiful mountain town known for its serene mountains and cool temperatures. It offers a range of outdoor activities such as hiking, skiing, and snowboarding. While it can be moderately expensive, you can find meals around $10 USD at local eateries.")
        # print(results)
        # await ctx.send(
        #     sender,
        #     UAgentResponse(
        #         message= result,
        #         type=UAgentResponseType.FINAL_OPTIONS
        #     )
        # )

        await ctx.send(intermediary_agent, UAgentResponse(
                message= final_result,
                type=UAgentResponseType.FINAL_OPTIONS
            ))

    # except openai.InvalidRequestError as e:
    #     print("Invalid request:", e)
    # except openai.Error as e:
    #     print("OpenAI API error:", e)
    except Exception as exc:
        ctx.logger.warn(f"olem ole ole {exc}")
        await ctx.send(sender, UAgentResponse(message=str(exc), type=UAgentResponseType.ERROR))

agent.include(top_destinations_protocol)
