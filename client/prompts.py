"""
Prompt and repositories for storing and loading prompts from the file system.
"""
from abc import ABC
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, ValidationError


class Prompt[T](BaseModel):
    """
    Encapsulates prompt-related information and functionalities.

    :ivar id: Unique identifier for the prompt.
    :type id: str
    :ivar content: The textual content of the prompt.
    :type content: str
    :ivar examples: A dictionary mapping example keys to their corresponding values of type T.
    :type examples: dict[str, T]
    """
    id: str
    content: str
    examples: dict[str, T] = {}


class PromptRepository(ABC):
    """
    General abstract base for storing and loading prompts.
    """
    parent_directory: Path
    file_extension: str

    def save_prompt(self, prompt: Prompt):
        """
        Save a prompt to the repository.

        :param prompt: Prompt to save.
        :type prompt: Prompt
        """

    def load_prompt(self, prompt_id: str) -> Optional[Prompt]:
        """
        Attempt to load a prompt from the repository.

        :param prompt_id: ID of the prompt to load.
        :type prompt_id: str
        :return: The loaded prompt, or None if not found.
        :rtype: Optional[Prompt]
        """

    def remove_prompt(self, prompt_id: str):
        """
        Attempt to remove a prompt from the repository.

        :param prompt_id: ID of the prompt to remove.
        :type prompt_id: str
        :raises FileNotFoundError: If the prompt is not found.
        """


class JSONRepository(PromptRepository):
    """
    JSON file repository for storing prompts.
    """

    def __init__(self, parent_directory: Path):
        """
        Create a new JSON repository. Creates a new directory in the file system if it does not exist.

        :param parent_directory: Parent directory for the repository.
        :type parent_directory: Path
        """
        self.parent_directory = parent_directory
        self.file_extension = '.json'

        self.parent_directory.mkdir(parents=True, exist_ok=True)

    def save_prompt(self, prompt: Prompt):
        full_path = (self.parent_directory / prompt.id).with_suffix(self.file_extension)
        full_path.write_text(prompt.model_dump_json(indent=2), encoding='utf-8')

    def load_prompt(self, prompt_id: str) -> Optional[Prompt]:
        for path in self.parent_directory.glob(f'*{prompt_id}*', case_sensitive=False):
            try:
                return Prompt.model_validate_json(path.read_text(encoding='utf-8'))

            except ValidationError:
                return None

        return None

    def remove_prompt(self, prompt_id: str):
        if not (self.parent_directory / prompt_id).with_suffix(self.file_extension).exists():
            raise FileNotFoundError(f'Prompt {prompt_id} not found.')

        (self.parent_directory / prompt_id).with_suffix(self.file_extension).unlink()
