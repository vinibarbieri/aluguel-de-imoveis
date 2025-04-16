"""
Módulo de armazenamento em JSON.
Este arquivo implementa um sistema de persistência de dados usando arquivos JSON.
Fornece funções para:
- Carregar e salvar dados em arquivos JSON
- Gerenciar IDs únicos
- Buscar e filtrar dados
- Deletar dados
"""

import json
import os
import uuid

# Diretório base onde os arquivos JSON serão armazenados
BASE_PATH = "data"

def _get_file_path(file_name):
    """
    Retorna o caminho completo do arquivo JSON.
    
    Args:
        file_name: Nome do arquivo (sem extensão)
        
    Returns:
        str: Caminho completo do arquivo
    """
    return os.path.join(BASE_PATH, f"{file_name}.json")

def load_all(file_name):
    """
    Carrega todos os dados de um arquivo JSON.
    
    Args:
        file_name: Nome do arquivo (sem extensão)
        
    Returns:
        list: Lista de dados carregados ou lista vazia se o arquivo não existir
    """
    path = _get_file_path(file_name)
    print("Loading data from:", path)
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_all(file_name, data):
    """
    Salva todos os dados em um arquivo JSON.
    
    Args:
        file_name: Nome do arquivo (sem extensão)
        data: Dados a serem salvos
    """
    path = _get_file_path(file_name)
    os.makedirs(BASE_PATH, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_next_uuid():
    """
    Gera um novo UUID único.
    
    Returns:
        str: UUID gerado
    """
    return str(uuid.uuid4())

def save_data(file_name, new_data):
    """
    Salva ou atualiza dados em um arquivo JSON.
    Se o dado não tiver ID, gera um novo UUID.
    
    Args:
        file_name: Nome do arquivo (sem extensão)
        new_data: Dados a serem salvos/atualizados
        
    Returns:
        dict: Dados salvos com ID
    """
    data = load_all(file_name)

    # Se não tiver id, gera um novo UUID
    if "id" not in new_data:
        new_data["id"] = get_next_uuid()

    # Remove entrada antiga com mesmo ID
    data = [d for d in data if d["id"] != new_data["id"]]
    data.append(new_data)

    save_all(file_name, data)
    return new_data

def find_by_id(file_name, id_value):
    """
    Busca um item pelo ID.
    
    Args:
        file_name: Nome do arquivo (sem extensão)
        id_value: ID do item a ser encontrado
        
    Returns:
        dict: Item encontrado ou None se não existir
    """
    data = load_all(file_name)
    for item in data:
        if str(item.get("id")) == str(id_value):
            return item
    return None

def find_many(file_name, filters=None):
    """
    Busca itens que correspondem aos filtros.
    
    Args:
        file_name: Nome do arquivo (sem extensão)
        filters: Dicionário com critérios de busca
        
    Returns:
        list: Lista de itens que correspondem aos filtros
    """
    data = load_all(file_name)
    if not filters:
        return data

    result = []
    for item in data:
        if all(str(item.get(k)) == str(v) for k, v in filters.items()):
            result.append(item)
    return result

def delete_data(file_name, id_value):
    """
    Deleta um item pelo ID.
    
    Args:
        file_name: Nome do arquivo (sem extensão)
        id_value: ID do item a ser deletado
        
    Returns:
        bool: True se o item foi deletado, False caso contrário
    """
    data = load_all(file_name)
    new_data = [item for item in data if str(item.get("id")) != str(id_value)]
    if len(new_data) < len(data):
        save_all(file_name, new_data)
        return True
    return False
