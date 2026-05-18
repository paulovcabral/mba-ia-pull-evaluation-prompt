"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure

def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

class TestPrompts:
    def test_prompt_has_system_prompt(self):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        prompts = load_prompts("prompts/bug_to_user_story_v2.yml")
        assert "system_prompt" in prompts, "A chave 'system_prompt' deve existir no YAML"
        assert prompts["system_prompt"], "O campo 'system_prompt' não pode ser vazio"

    def test_prompt_has_role_definition(self):
        """Verifica se o prompt define uma persona (ex: "Você é um Product Manager")."""
        prompts = load_prompts("prompts/bug_to_user_story_v2.yml")
        system_prompt = prompts.get("system_prompt", "").lower()
        # Procura por termos como "você é um", "atue como", "seu papel é"
        assert any(term in system_prompt for term in ["você é", "atue como", "sua função é", "seu papel"]), "O prompt deve definir claramente o papel (role) do assistente"

    def test_prompt_mentions_format(self):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        prompts = load_prompts("prompts/bug_to_user_story_v2.yml")
        system_prompt = prompts.get("system_prompt", "").lower()
        assert "markdown" in system_prompt or "user story" in system_prompt, "O prompt deve exigir a saída em formato Markdown ou formato padrão de User Story"

    def test_prompt_has_few_shot_examples(self):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        prompts = load_prompts("prompts/bug_to_user_story_v2.yml")
        system_prompt = prompts.get("system_prompt", "").lower()
        assert "exemplo" in system_prompt or "input:" in system_prompt or "output:" in system_prompt, "O prompt deve conter exemplos de entrada/saída (Few-shot learning)"

    def test_prompt_no_todos(self):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        prompts = load_prompts("prompts/bug_to_user_story_v2.yml")
        system_prompt = prompts.get("system_prompt", "")
        user_prompt = prompts.get("user_prompt", "")
        assert "[TODO]" not in system_prompt and "TODO" not in system_prompt, "Existem tags TODO pendentes no system_prompt"
        assert "[TODO]" not in user_prompt and "TODO" not in user_prompt, "Existem tags TODO pendentes no user_prompt"

    def test_minimum_techniques(self):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        prompts = load_prompts("prompts/bug_to_user_story_v2.yml")
        techniques = prompts.get("techniques_applied", [])
        assert isinstance(techniques, list), "O campo 'techniques_applied' deve ser uma lista"
        assert len(techniques) >= 2, f"O prompt deve aplicar no mínimo 2 técnicas (encontradas {len(techniques)})"

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])