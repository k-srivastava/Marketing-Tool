"""
AI wrapper for the Google Gemini client and related utilities.
"""

import os
from typing import Literal, Type, Optional

import dotenv
from PIL import Image
from google import genai
from google.genai.types import GenerateContentConfig, HttpOptions
from pydantic import BaseModel

# All supported models by the application.
SUPPORTED_MODEL: type[str] = Literal['gemini-2.5-flash', 'gemini-2.5-flash-image', 'gemini-2.5-pro']


class AIClient:
    """
    Wrapper over the Google Gemini client. Contains methods for generating text and parsed responses.
    """

    def __init__(self, system_instruction: str, model_name: SUPPORTED_MODEL = 'gemini-2.5-pro'):
        """
        Creates and validates a new client instance.

        :param system_instruction: System instruction to be supplied to the model.
        :type system_instruction: str
        :param model_name: Name of the Gemini model to use.
        :type model_name: SUPPORTED_MODEL

        :raises EnvironmentError: If GOOGLE_API_KEY is not found in the .env file.
        """
        dotenv.load_dotenv()

        google_api_key = os.getenv('GOOGLE_API_KEY')
        if google_api_key is None:
            raise EnvironmentError('GOOGLE_API_KEY not found in .env file. Please issue a key and add it.')

        self.system_instruction = system_instruction
        self.model_name = model_name
        self._google_client = genai.Client(api_key=google_api_key, http_options=HttpOptions(timeout=30000))

    async def generate_text_response(self, prompt: str) -> str:
        """
        Generate a plain text response from the given prompt.

        :param prompt: Prompt to the AI model.
        :type prompt: str
        :return: Generated response.
        :rtype: str

        :raises ValueError: If the response is not a text response, or is None.
        """
        response = await self._google_client.aio.models.generate_content(
            model=self.model_name, contents=prompt,
            config=GenerateContentConfig(system_instruction=self.system_instruction)
        )

        if response.parsed is not None:
            raise ValueError('Response is not a text response.')

        if response.text is None:
            raise ValueError('Response is empty.')

        return response.text

    async def generate_parsed_response[T: BaseModel](
            self, prompt: str, schema: Type[T], image: Optional[Image.Image] = None
    ) -> T:
        """
        Generate a parsed response from the given prompt and optional image using Pydantic models and validation.
        The type variable T must be a Pydantic BaseModel used to parse the response.

        :param prompt: Prompt to the AI model.
        :type prompt: str
        :param schema: Pydantic model to use for parsing the response.
        :type schema: Type[T]
        :param image: Optional image to be included in the prompt.
        :type image: Optional[Image.Image]
        :return: Parsed response as the Pydantic model instance.
        :rtype: T

        :raises ValueError: If the response is not a parsed response, or is None.
        """
        if image is None:
            contents = [prompt]
        else:
            contents = [prompt, image]

        response = await self._google_client.aio.models.generate_content(
            model=self.model_name,
            contents=contents,
            config=GenerateContentConfig(
                system_instruction=self.system_instruction, response_mime_type='application/json',
                response_schema=schema
            )
        )

        if response.parsed is None:
            raise ValueError('Response is empty.')

        return response.parsed

    async def generate_image_response(self, prompt: str, image: Optional[Image.Image]) -> tuple[str, Image.Image]:
        """
        Asynchronously generates a text and image response based on the given prompt and optional input image.
        This method uses a specific model ("gemini-2.5-flash-image") to generate content.
        If the specified model is not used or no image is generated in the response, appropriate errors
        will be raised.

        :param prompt: The input textual prompt to guide the content generation process.
        :type prompt: str
        :param image: An optional input image to refine or complement the content generation.
        :type image: Optional[Image.Image]
        :return: A tuple containing the generated text and the generated image.
        :rtype: tuple[str, Image.Image]

        :raises ValueError: If the model is not "gemini-2.5-flash-image" or if no image is generated in the response.
        """
        if self.model_name != 'gemini-2.5-flash-image':
            raise ValueError('Image generation is only supported for the gemini-2.5-flash-image model.')

        if image is None:
            contents = [prompt]
        else:
            contents = [prompt, image]

        response = await self._google_client.aio.models.generate_content(
            model=self.model_name,
            contents=contents,
            config=GenerateContentConfig(system_instruction=self.system_instruction)
        )

        text = ''
        image: Optional[Image.Image] = None

        for part in response.parts:
            if part.text:
                text += f'{part.text}\n'

            elif response_image := part.as_image():
                image = response_image

        if image is None:
            raise ValueError('Response image is empty.')

        return text, image
