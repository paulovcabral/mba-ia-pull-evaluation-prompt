"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()


def pull_prompts_from_langsmith():
    """Faz pull dos prompts do LangSmith Hub."""
    prompt_id = "leonanluppi/bug_to_user_story_v1"
    print(f"Fazendo pull do prompt {prompt_id}...")
    try:
        prompt = hub.pull(prompt_id)
        # Salva o prompt localmente em YAML
        output_path = "prompts/bug_to_user_story_v1.yml"
        
        # Converte para dicionário usando serialização nativa
        prompt_dict = prompt.dict()
        
        if save_yaml(prompt_dict, output_path):
            print(f"✅ Prompt salvo com sucesso em {output_path}")
            return True
        else:
            print("❌ Falha ao salvar o prompt.")
            return False
    except Exception as e:
        print(f"❌ Erro ao fazer pull do prompt: {e}")
        return False


def main():
    """Função principal"""
    print_section_header("Pull de Prompts do LangSmith")
    
    if not check_env_vars(["LANGCHAIN_API_KEY"]):
        return 1
        
    success = pull_prompts_from_langsmith()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
