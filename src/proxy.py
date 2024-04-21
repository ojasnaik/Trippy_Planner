import json
from fastapi import FastAPI
from messages import UAgentResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware
from uagents.query import query  # Make sure you're correctly importing necessary functions

AGENT_ADDRESS = "agent1q0wf3xa58qfn8eayxcn7xhlxl8qhpjnkfdtwpru987afat9wrkxrstxs9q8"

class TestRequest(BaseModel):  # Changed from Model to BaseModel for Pydantic
    message: str

async def agent_query(req):
    print(req)
    response = await query(destination=AGENT_ADDRESS, message=req, timeout=15.0)  # Ensure the payload is correctly formed
    print(response)
    data = json.loads(response.decode_payload())
    print(data)
    return data["message"]

app = FastAPI()

# Add CORS middleware to allow connections from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def read_root():
    return "Hello from the Agent controller"

@app.post("/submit")
async def make_agent_call(req: UAgentResponse):
    try:
        res = await agent_query(req)
        print(res)
        return {"status": "success", "response": res}  # Modified to return JSON
    except Exception as e:
        return {"status": "error", "error": str(e)}  # Modified to return JSON and include error details

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)  # Specify the port here
