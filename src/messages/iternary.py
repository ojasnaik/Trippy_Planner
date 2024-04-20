from uagents import Model
from pydantic import Field

class Iternary(Model):
  destinations: str = Field(description="The field expresses the top attractions suggested to the user.")
