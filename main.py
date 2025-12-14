from pathlib import Path

from fastapi import FastAPI

from client.ai import AIClient
from client.models import FontRecommendation, ProductInformation, ColorCurator
from client.prompts import JSONRepository

app = FastAPI()
repository = JSONRepository(Path.cwd() / 'assets' / 'prompts')


@app.get('/info')
async def get_info(description: str, use_ai: bool = False) -> ProductInformation:
    if use_ai:
        prompt = repository.load_prompt('information-extractor')
        client = AIClient(prompt.to_system_instruction(), model_name='gemini-2.5-flash')

        response = await client.generate_parsed_response(description.strip(), ProductInformation)
        return response

    return ProductInformation(
        name='The Eye Concentrate',
        tagline='Reduce the look of dark circles for a brighter, healthier look',
        brand_name='La Mer',
        features=[
            'Removes dark circles and lines',
            'Brightens skin',
            'Smoothens skin',
            'Gives a brighter, healthier look'
        ]
    )


@app.get('/font')
async def get_fonts(description: str, use_ai: bool = False) -> FontRecommendation:
    if use_ai:
        prompt = repository.load_prompt('font-recommender')
        client = AIClient(prompt.to_system_instruction(), model_name='gemini-2.5-flash')

        response = await client.generate_parsed_response(description.strip(), FontRecommendation)
        return response

    return FontRecommendation(
        font_1='MonteCarlo',
        font_1_link='<link href="https://fonts.googleapis.com/css2?family=MonteCarlo&display=swap" rel="stylesheet">',
        font_2='Playfair Display',
        font_2_link='<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400..900;1,400..900&display=swap" rel="stylesheet">',
        font_3='EB Garamond',
        font_3_link='<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400..800;1,400..800&display=swap" rel="stylesheet">',
        font_4='DM Serif Text',
        font_4_link='<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Text:ital@0;1&display=swap" rel="stylesheet">'
    )


@app.get('/color')
async def get_color_scheme(description: str, use_ai: bool = False) -> ColorCurator:
    if use_ai:
        prompt = repository.load_prompt('color-curator')
        client = AIClient(prompt.to_system_instruction(), model_name='gemini-2.5-flash')

        response = await client.generate_parsed_response(description.strip(), ColorCurator)
        return response

    return ColorCurator(
        color_scheme_1=['#0A6159', '#F5F7F2'],
        color_scheme_2=['#1A7F85', '#D9C7A3'],
        color_scheme_3=['#2F5F4A', '#E9DDC7'],
        color_scheme_4=['#0D4C3A', '#DDE3E1']
    )
