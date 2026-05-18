"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header, validate_prompt_structure

load_dotenv()


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt
        prompt_data: Dados do prompt

    Returns:
        True se sucesso, False caso contrário
    """
    try:
        # Extrai os dados do YAML
        system_prompt = prompt_data.get('system_prompt', '')
        # Se não houver user_prompt, usa um padrão com a variável correta
        user_prompt = prompt_data.get('user_prompt', '{bug_report}')
        
        description = prompt_data.get('description', 'Prompt otimizado')
        techniques = prompt_data.get('techniques_applied', [])
        
        # Cria o ChatPromptTemplate com system e user message
        messages = [
            ("system", system_prompt),
            ("user", user_prompt)
        ]
        
        prompt = ChatPromptTemplate.from_messages(messages)
        
        print(f"Fazendo push para '{prompt_name}'...")
        
        # Usa os parâmetros corretos para a nova versão da API do Hub
        hub.push(
            prompt_name,
            prompt,
            new_repo_is_public=True,
            new_repo_description=description,
            tags=techniques
        )
        
        return True
    except Exception as e:
        print(f"❌ Erro ao fazer push: {e}")
        return False


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt (versão simplificada).

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    # Utiliza a função completa já existente no utils.py
    return validate_prompt_structure(prompt_data)


def main():
    """Função principal"""
    print_section_header("Push de Prompts ao LangSmith")
    
    if not check_env_vars(["LANGSMITH_API_KEY", "USERNAME_LANGSMITH_HUB"]):
        return 1
        
    prompt_path = "prompts/bug_to_user_story_v2.yml"
    print(f"Lendo prompt de {prompt_path}...")
    
    prompt_data = load_yaml(prompt_path)
    if not prompt_data:
        print("❌ Falha ao carregar o arquivo YAML.")
        return 1
        
    is_valid, errors = validate_prompt(prompt_data)
    
    if not is_valid:
        print("❌ Prompt inválido. Erros encontrados:")
        for error in errors:
            print(f"   - {error}")
        return 1
        
    print("✅ Prompt válido.")
    
    username = os.environ.get("USERNAME_LANGSMITH_HUB")
    prompt_name = f"{username}/bug_to_user_story_v2"
    
    if push_prompt_to_langsmith(prompt_name, prompt_data):
        print(f"✅ Prompt publicado com sucesso!")
        print(f"🔗 Link: https://smith.langchain.com/hub/{prompt_name}")
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
