from uagents import Agent, Context, Protocol
from messages import TopDestinations, UAgentResponse, UAgentResponseType, KeyValue
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

fund_agent_if_low(agent.wallet.address())

llm = get_llm()
top_destinations_protocol = Protocol("TopDestinations")

@top_destinations_protocol.on_message(model=TopDestinations, replies=UAgentResponse)
async def get_top_destinations(ctx: Context, sender: str, msg: TopDestinations):
    ctx.logger.info(f"Received message from {sender}, session: {ctx.session}")
    prompt = f"""You are an expert AI in suggesting travel, holiday destination based on some user input.
User input might not be provided, in which case suggest popular destinations. 
If user input is present, then suggest destinations based on user input.
The response should be a list of destinations, each destination should have information about why it is a good destination. 
After listing all the suggestions say END. Every destination should be separated by a new line.

Example:
User input: I want to go to a place with good weather and beaches.
Response:
1. Goa, India. Goa is a popular destination for tourists. It has good weather and beaches.
2. Malé, Maldives. Maldives is a popular destination for tourists. It has good weather and beaches.
END

User preferences: {msg.preferences}
"""
    try:
        print("Before llm.comlete")
        response = await llm.complete("", prompt, "Response:", max_tokens=500, stop=["END"])
        print("Before ctx.send")
        result = response.strip()
        result = result.split("\n")
        results = list(map(lambda x: KeyValue(key=x, value=x), result))
        # iternary_request = Iternary(destinations="Aspen, Colorado, USA. Aspen is a beautiful mountain town known for its serene mountains and cool temperatures. It offers a range of outdoor activities such as hiking, skiing, and snowboarding. While it can be moderately expensive, you can find meals around $10 USD at local eateries.")
        print(results)
        await ctx.send(
            sender,
            UAgentResponse(
                options= results,
                type=UAgentResponseType.FINAL_OPTIONS
            )
        )

        await ctx.send("agent1q2gam6vqryy7zk34n6crf4tpg7ld72deg6hzcvu4jd2ej34aqpayynmz788", UAgentResponse(
                options= results,
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
