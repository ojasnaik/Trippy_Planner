import uagents
# from uagents import Bureau
# from uagents import Bureau
 

# from agents.activities.top_activities import agent as top_activities_agent
from agents.destinations.top_destinations import agent as top_destinations_agent
from agents.scheduler.iternary import agent as iternary_agent
# from agents.intermediary.next_agent import agent as intermediary_agent
from agents.activities.top_activities import agent as top_activities_agent
from agents.hotels.hotels import agent as hotels_agent
from agents.dining.top_dining import agent as dining_agent
from agents.flights.flights import agent as flights_agent


if __name__ == "__main__":
    bureau = uagents.Bureau(endpoint="http://127.0.0.1:8000/submit", port=8000)
    # print(f"Adding top activities agent to Bureau: {top_activities_agent.address}")
    # bureau.add(top_activities_agent)
    print(f"Adding top destinations agent to Bureau: {top_destinations_agent.address}")
    bureau.add(top_destinations_agent)

    print(f"Adding iternary agent to Bureau: {iternary_agent.address}")
    bureau.add(iternary_agent)

    print(f"Adding top activities agent to Bureau: {top_activities_agent.address}")
    bureau.add(top_activities_agent)

    # print(f"Adding intermediary agent to Bureau: {intermediary_agent.address}")
    # bureau.add(intermediary_agent)

    print(f"Adding hotels agent to Bureau: {hotels_agent.address}")
    bureau.add(hotels_agent)

    print(f"Adding dining agent to Bureau: {dining_agent.address}")
    bureau.add(dining_agent)

    print(f"Adding flights agent to Bureau: {flights_agent.address}")
    bureau.add(flights_agent)

    
    # print(f"Adding flights agent to Bureau: {flights_agent.address}")
    # bureau.add(flights_agent)
    bureau.run()