"""
Módulo de serviços de autenticação.
Este arquivo contém funções relacionadas à autenticação e gerenciamento de usuários.
"""

from app.data_manager import find_by_id, save_data

def update_user_info(user_id, name, email):
    """
    Atualiza as informações de um usuário.
    
    Args:
        user_id: ID do usuário a ser atualizado
        name: Novo nome do usuário (opcional)
        email: Novo email do usuário (opcional)
        
    Raises:
        Exception: Se o usuário não for encontrado
    """
    user = find_by_id("users", user_id)

    if not user:
        raise Exception("Usuário não encontrado")

    # Atualiza os campos desejados
    if name:
        user["name"] = name
    if email:
        user["email"] = email

    # Salva de volta usando a lógica do data_manager
    save_data("users", user)
