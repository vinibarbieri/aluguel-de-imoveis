"""
Módulo de modelo de imóvel.
Define a classe Property que representa um imóvel disponível para aluguel.
"""

from datetime import date

class Property:
    """
    Classe que representa um imóvel disponível para aluguel.
    
    Attributes:
        id: Identificador único do imóvel
        title: Título do imóvel
        description: Descrição do imóvel
        address: Endereço do imóvel
        price_per_day: Preço por dia do aluguel
        available_from: Data de disponibilidade inicial (string em formato ISO)
        available_until: Data de disponibilidade final (string em formato ISO)
        owner_id: ID do proprietário do imóvel
        image_url: URL da imagem do imóvel (opcional)
    """
    
    def __init__(self, id, title, description, address, city, price_per_day,
                 available_from, available_until, owner_id, image_url=None):
        """
        Inicializa um novo imóvel.
        
        Args:
            id: Identificador único do imóvel
            title: Título do imóvel
            description: Descrição do imóvel
            address: Endereço do imóvel
            price_per_day: Preço por dia do aluguel
            available_from: Data de disponibilidade inicial (string em formato ISO)
            available_until: Data de disponibilidade final (string em formato ISO)
            owner_id: ID do proprietário do imóvel
            image_url: URL da imagem do imóvel (opcional)
        """
        self.id = id
        self.title = title
        self.description = description
        self.address = address
        self.city = city
        self.price_per_day = price_per_day
        self.available_from = available_from  # string em formato ISO (ex: "2025-01-01")
        self.available_until = available_until
        self.owner_id = owner_id
        self.image_url = image_url

    def to_dict(self):
        """
        Converte o objeto Property para um dicionário.
        
        Returns:
            dict: Dicionário contendo os dados do imóvel
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "address": self.address,
            "city": self.city,
            "price_per_day": self.price_per_day,
            "available_from": self.available_from,
            "available_until": self.available_until,
            "owner_id": self.owner_id,
            "image_url": self.image_url
        }

    @staticmethod
    def from_dict(data):
        """
        Cria um objeto Property a partir de um dicionário.
        
        Args:
            data: Dicionário contendo os dados do imóvel
            
        Returns:
            Property: Objeto Property criado a partir dos dados
        """
        return Property(
            id=data["id"],
            title=data["title"],
            description=data["description"],
            address=data["address"],
            city=data.get("city", ""),
            price_per_day=data["price_per_day"],
            available_from=data["available_from"],
            available_until=data["available_until"],
            owner_id=data["owner_id"],
            image_url=data.get("image_url")
        )
