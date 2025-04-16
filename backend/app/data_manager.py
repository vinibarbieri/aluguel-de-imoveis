"""
Módulo de gerenciamento de dados.
Este arquivo implementa um sistema simples de persistência de dados usando arquivos JSON.
Fornece funções para:
- Salvar dados
- Carregar dados
- Deletar dados
- Buscar dados por ID ou query
- Gerenciar IDs numéricos
"""

import json
import os
from typing import Dict, List, Any
import uuid

# Diretório onde os arquivos JSON serão armazenados
DATA_DIR = "data"

def ensure_data_dir():
    """
    Garante que o diretório de dados existe.
    Cria o diretório se ele não existir.
    """
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def save_data(collection: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Salva dados em um arquivo JSON.
    
    Args:
        collection: Nome da coleção (nome do arquivo JSON)
        data: Dicionário com os dados a serem salvos
        
    Returns:
        Dict[str, Any]: Dados salvos com ID gerado/atualizado
    """
    ensure_data_dir()
    file_path = os.path.join(DATA_DIR, f"{collection}.json")
    
    # Carrega dados existentes
    existing_data = load_data(collection)
    
    # Gera ID se não existir
    if "id" not in data:
        data["id"] = str(uuid.uuid4())
    
    # Atualiza ou adiciona dados
    existing_data = [item for item in existing_data if item.get("id") != data["id"]]
    existing_data.append(data)
    
    # Salva todos os dados
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=2)
    
    return data

def load_data(collection: str) -> List[Dict[str, Any]]:
    """
    Carrega dados de um arquivo JSON.
    
    Args:
        collection: Nome da coleção (nome do arquivo JSON)
        
    Returns:
        List[Dict[str, Any]]: Lista de dicionários com os dados carregados
    """
    ensure_data_dir()
    file_path = os.path.join(DATA_DIR, f"{collection}.json")
    
    if not os.path.exists(file_path):
        return []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def delete_data(collection: str, _id: str) -> bool:
    """
    Deleta um documento pelo ID.
    
    Args:
        collection: Nome da coleção
        _id: ID do documento a ser deletado
        
    Returns:
        bool: True se o documento foi deletado, False caso contrário
    """
    data = load_data(collection)
    original_length = len(data)
    data = [item for item in data if item.get("id") != _id]
    
    if len(data) < original_length:
        file_path = os.path.join(DATA_DIR, f"{collection}.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    return False

def find_by_id(collection: str, _id: str) -> Dict[str, Any]:
    """
    Encontra um documento pelo ID.
    
    Args:
        collection: Nome da coleção
        _id: ID do documento a ser encontrado
        
    Returns:
        Dict[str, Any]: Documento encontrado ou None se não existir
    """
    data = load_data(collection)
    for item in data:
        if item.get("id") == _id:
            return item
    return None

def find_many(collection: str, query: Dict[str, Any] = None) -> List[Dict[str, Any]]:
    """
    Encontra documentos que correspondem à query.
    
    Args:
        collection: Nome da coleção
        query: Dicionário com os critérios de busca
        
    Returns:
        List[Dict[str, Any]]: Lista de documentos que correspondem à query
    """
    data = load_data(collection)
    if not query:
        return data
    
    result = []
    for item in data:
        matches = all(item.get(k) == v for k, v in query.items())
        if matches:
            result.append(item)
    return result

def get_next_numeric_id(collection: str) -> int:
    """
    Gera o próximo ID numérico para uma coleção.
    
    Args:
        collection: Nome da coleção
        
    Returns:
        int: Próximo ID numérico disponível
    """
    data = load_data(collection)
    if not data:
        return 1
    ids = [int(d["id"]) for d in data if str(d["id"]).isdigit()]
    return max(ids, default=0) + 1
