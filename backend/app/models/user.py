"""
Módulo de modelo de usuário.
Define a classe User que representa um usuário do sistema.
"""

class User:
    """
    Classe que representa um usuário do sistema.
    
    Attributes:
        id: Identificador único do usuário
        name: Nome do usuário
        email: Email do usuário
        user_type: Tipo do usuário ('locador' ou 'locatario')
    """
    
    def __init__(self, id, name, email, user_type):
        """
        Inicializa um novo usuário.
        
        Args:
            id: Identificador único do usuário
            name: Nome do usuário
            email: Email do usuário
            user_type: Tipo do usuário ('locador' ou 'locatario')
        """
        self.id = id
        self.name = name
        self.email = email
        self.user_type = user_type  # 'locador' ou 'locatario'

    def to_dict(self):
        """
        Converte o objeto User para um dicionário.
        
        Returns:
            dict: Dicionário contendo os dados do usuário
        """
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "user_type": self.user_type
        }

    @staticmethod
    def from_dict(data):
        """
        Cria um objeto User a partir de um dicionário.
        
        Args:
            data: Dicionário contendo os dados do usuário
            
        Returns:
            User: Objeto User criado a partir dos dados
        """
        return User(
            id=data["id"],
            name=data["name"],
            email=data["email"],
            user_type=data["user_type"]
        )
