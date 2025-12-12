from pathlib import Path

from fastapi import FastAPI

from client.ai import AIClient
from client.models import FontRecommendation, ProductInformation, ColorCurator
from client.prompts import JSONRepository

app = FastAPI()
repository = JSONRepository(Path.cwd() / 'assets' / 'prompts')


@app.get('/info')
async def get_info(description: str) -> ProductInformation:
    prompt = repository.load_prompt('information-extractor')
    client = AIClient(prompt.to_system_instruction(), model_name='gemini-2.5-flash')

    response = await client.generate_parsed_response(description.strip(), ProductInformation)
    return response


@app.get('/font')
async def get_fonts(description: str) -> FontRecommendation:
    prompt = repository.load_prompt('font-recommender')
    client = AIClient(prompt.to_system_instruction(), model_name='gemini-2.5-flash')

    response = await client.generate_parsed_response(description.strip(), FontRecommendation)
    return response


@app.get('/color')
async def get_color_scheme(description: str) -> ColorCurator:
    prompt = repository.load_prompt('color-curator')
    client = AIClient(prompt.to_system_instruction(), model_name='gemini-2.5-flash')

    response = await client.generate_parsed_response(description.strip(), ColorCurator)
    return response
