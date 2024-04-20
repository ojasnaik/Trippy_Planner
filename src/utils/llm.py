import openai
import time
from typing import List
import os

class OpenAILLM:
  def __init__(self,
      completion_model: str = "text-davinci-003",
      embedding_model: str = "text-embedding-ada-002"
    ):
    self.completion_model = completion_model
    self.embedding_model = embedding_model
    self.usage_counter = None

  async def embedding(self, text: str) -> str:
    text = text.replace("\n", " ")
    emb = await openai.Embedding.acreate(input=[text], model=self.embedding_model)
    if self.usage_counter:
        await self.usage_counter.add_embedding_usage(emb["usage"])
    return emb["data"][0]["embedding"]

  async def complete(
    self,
    header: str,
    prompt: str,
    complete: str,
    max_tokens: int = 100,
    temperature: float = 0.5,
    stop: List[str] = None,
  ) -> str:
    print(self.completion_model)
    # try:
    #   if self.completion_model != "gpt-4" and self.completion_model.find("gpt-3.5") == -1:
    #       #Call GPT-3 DaVinci model
    #       print("Hello")
    #       # response = await openai.Completion.acreate(
    #       try:
    #          response = await openai.Completion.create(
    #           engine=self.completion_model,
    #           prompt=header+prompt+complete,
    #           temperature=temperature,
    #           max_tokens=max_tokens,
    #           top_p=1,
    #           frequency_penalty=0,
    #           presence_penalty=0,
    #           stop=stop
    #       )
    #       except openai.APIError as e:
    #           print(f"API Error occurred: {e}")
    #       except openai.OpenAIError as e:
    #           print(f"An error occurred with OpenAI: {e}")
    #       except Exception as e:
    #           print(f"An unexpected error occurred: {e}")

    #       if self.usage_counter:
    #         await self.usage_counter.add_completion_usage(response.usage)
    #       return response.choices[0].text.strip()
    #   else:
    #       #Call GPT-4/gpt-3.5 chat model
    #       messages=[{"role": "system", "content": header}, {"role": "user", "content": prompt}, {"role": "assistant", "content": complete}]
    #       response = await openai.ChatCompletion.acreate(
    #           model=self.completion_model,
    #           messages = messages,
    #           temperature=temperature,
    #           max_tokens=max_tokens,
    #           n=1,
    #           stop=stop,
    #       )
    #       if self.usage_counter:
    #         await self.usage_counter.add_completion_usage(response.usage)
    #       return response.choices[0].message.content.strip()
    # except openai.InvalidRequestError as err:
    #   print("openai_call InvalidRequestError: ", err)
    #   print("\n\n§§§§§§§§§§§§§§§§§§§§§§§§§§§§PROMPT§§§§§§§§§§§§§§§§§§§§§§§§§§§§")
    #   print(prompt)
    #   print("§§§§§§§§§§§§§§§§§§§§§§§§§§§§\n\n")
    #   raise err
    # except Exception as err:
    #     print("openai_call Exception: ", err)
    #     print("Retry...")
    #     time.sleep(2)
    #     return await self.complete(header, prompt, complete, temperature, max_tokens, stop)


    try:
      messages=[{"role": "system", "content": header}, {"role": "user", "content": prompt}, {"role": "assistant", "content": complete}]
      response = await openai.ChatCompletion.acreate(
          model=self.completion_model,
          messages = messages,
          temperature=temperature,
          max_tokens=max_tokens,
          n=1,
          stop=stop,
      )
    except openai.APIError as e:
      print(f"API Error occurred: {e}")
    except openai.OpenAIError as e:
      print(f"An error occurred with OpenAI: {e}")
    except Exception as e:
      print(f"An unexpected error occurred: {e}")
    return response.choices[0].message.content.strip()


def get_llm():
    # return OpenAILLM(completion_model="text-davinci-003")
    return OpenAILLM(completion_model="gpt-3.5-turbo")
