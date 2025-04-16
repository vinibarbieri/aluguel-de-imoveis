"""
Script de inicialização da aplicação Flask.
Este arquivo é responsável por iniciar o servidor de desenvolvimento.
"""
from app import create_app

# Cria a aplicação Flask usando a função factory
app = create_app()

if __name__ == '__main__':
    # Inicia o servidor de desenvolvimento com modo debug ativado
    # O modo debug permite:
    # - Recarregamento automático do código
    # - Mensagens de erro detalhadas
    # - Debugger interativo
    app.run(debug=True)
