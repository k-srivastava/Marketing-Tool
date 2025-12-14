from io import BytesIO
from pathlib import Path

from PIL import Image
from fastapi import FastAPI, UploadFile, File, Form, Response, HTTPException

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


@app.post('/generate')
async def generate_final_poster(
        name: str = Form(...),
        tagline: str = Form(...),
        brand_name: str = Form(...),
        font: str = Form(...),
        primary_color: str = Form(...),
        secondary_color: str = Form(...),
        hero_feature: str = Form(...),
        size: str = Form(...),
        raw_poster: UploadFile = File(...),
        comments: str = Form(''),
        use_ai: bool = Form(False)
) -> Response:
    try:
        uploaded_bytes = await raw_poster.read()
        img = Image.open(BytesIO(uploaded_bytes))
        img.load()
    except Exception:
        raise HTTPException(status_code=400, detail='Invalid image uploaded')

    if use_ai:
        message = (
            f'Product Name: "{name}", Tagline: "{tagline}", Brand Name: "{brand_name}", Font: "{font}", '
            f'Primary Color (Hex): "{primary_color}", Secondary Color (Hex): "{secondary_color}", '
            f'Hero Feature (Must be included): "{hero_feature}", Size: "{size}", Comments: "{comments}"'
        )

        prompt = repository.load_prompt('image-generation')
        client = AIClient(prompt.to_system_instruction(), model_name='gemini-2.5-flash-image')

        _text, generated_image = await client.generate_image_response(message, img)
        generated_image.save('assets/images/generated.png')

        with open('assets/images/generated.png', 'rb') as f:
            out = f.read()

        return Response(out, media_type='image/png', headers={'Cache-Control': 'no-store'})

    with open('assets/images/generated.png', 'rb') as f:
        out = f.read()

    return Response(out, media_type='image/png', headers={'Cache-Control': 'no-store'})
