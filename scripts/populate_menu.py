from app.database.session import SessionLocal
from app.models.categoria_produto_model import CategoriaProduto
from app.models.produto_model import Produto
from app.models.produto_variante_model import ProdutoVariante
from app.models.categoria_addon_model import CategoriaAddon
from app.models.addon_model import Addon

session = SessionLocal()

def popular_menu():

    # -------------------
    # Categorias Produto
    # -------------------

    pizza = CategoriaProduto(nome="Pizza")
    hamburguer = CategoriaProduto(nome="Hambúrguer")
    bebidas = CategoriaProduto(nome="Bebidas")

    session.add_all([pizza, hamburguer, bebidas])
    session.commit()

    # -------------------
    # Produtos
    # -------------------

    pizza_calabresa = Produto(nome="Pizza Calabresa", idcategoria=pizza.id)
    pizza_frango = Produto(nome="Pizza Frango com Catupiry", idcategoria=pizza.id)

    burger_classico = Produto(nome="Hambúrguer Clássico", idcategoria=hamburguer.id)

    coca = Produto(nome="Coca-Cola", idcategoria=bebidas.id)

    session.add_all([
        pizza_calabresa,
        pizza_frango,
        burger_classico,
        coca
    ])
    session.commit()

    # -------------------
    # Variantes de Produto
    # -------------------

    variantes = [

        ProdutoVariante(
            idproduto=pizza_calabresa.id,
            variacao="Pequena",
            preco_variante=35
        ),

        ProdutoVariante(
            idproduto=pizza_calabresa.id,
            variacao="Média",
            preco_variante=45
        ),

        ProdutoVariante(
            idproduto=pizza_calabresa.id,
            variacao="Grande",
            preco_variante=55
        ),

        ProdutoVariante(
            idproduto=pizza_frango.id,
            variacao="Média",
            preco_variante=48
        ),

        ProdutoVariante(
            idproduto=burger_classico.id,
            variacao="Padrão",
            preco_variante=22
        ),

        ProdutoVariante(
            idproduto=coca.id,
            variacao="350ml",
            preco_variante=6
        ),

        ProdutoVariante(
            idproduto=coca.id,
            variacao="1L",
            preco_variante=10
        ),
    ]

    session.add_all(variantes)
    session.commit()

    # -------------------
    # Categorias Addon
    # -------------------

    bordas = CategoriaAddon(nome="Bordas")
    extras = CategoriaAddon(nome="Extras")
    molhos = CategoriaAddon(nome="Molhos")

    session.add_all([bordas, extras, molhos])
    session.commit()

    # -------------------
    # Addons
    # -------------------

    addons = [

        Addon(
            idcategoria=bordas.id,
            nome="Borda Catupiry",
            preco_addon=8
        ),

        Addon(
            idcategoria=bordas.id,
            nome="Borda Cheddar",
            preco_addon=8
        ),

        Addon(
            idcategoria=extras.id,
            nome="Bacon Extra",
            preco_addon=5
        ),

        Addon(
            idcategoria=extras.id,
            nome="Queijo Extra",
            preco_addon=4
        ),

        Addon(
            idcategoria=molhos.id,
            nome="Molho Barbecue",
            preco_addon=2
        ),

        Addon(
            idcategoria=molhos.id,
            nome="Molho Alho",
            preco_addon=2
        ),
    ]

    session.add_all(addons)
    session.commit()

    print("Menu populado com sucesso!")


if __name__ == "__main__":
    popular_menu()
    session.close()
