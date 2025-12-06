from abc import ABC
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, ValidationError


class Prompt(BaseModel):
    id: str
    content: str


class PromptRepository(ABC):
    parent_directory: Path
    file_extension: str

    def save_prompt(self, prompt: Prompt):
        pass

    def load_prompt(self, prompt_id: str) -> Optional[Prompt]:
        pass

    def remove_prompt(self, prompt_id: str):
        pass


class JSONRepository(PromptRepository):
    def __init__(self, parent_directory: Path):
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
