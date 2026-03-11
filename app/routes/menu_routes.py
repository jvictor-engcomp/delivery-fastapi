from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import verificar_token, pegar_sessao

from app.models.usuario_model import Usuario
from app.models.categoria_produto_model import CategoriaProduto
from app.models.produto_model import Produto
from app.models.produto_variante_model import ProdutoVariante

from app.schemas.categoria_produto_schema import CategoriaProdutoSchema
from app.schemas.produto_schema import ProdutoSchema
from app.schemas.produto_variante_schema import ProdutoVarianteSchema

menu_router = APIRouter(prefix="/menu", tags=['menu'], dependencies=[Depends(verificar_token)])

@menu_router.post('/categoria/produto')
async def criar_categoria_produto(categoriaprodutoschema: CategoriaProdutoSchema, usuario: Usuario = Depends(verificar_token), session: Session = Depends(pegar_sessao)):
    if not usuario.admin:
        raise HTTPException(403, 'Você não tem permissão para criar categoria.')
    categoria = CategoriaProduto(categoriaprodutoschema.nome)
    session.add(categoria)
    session.commit()
    return {
        'mensagem': 'Categoria criada.'
    }

@menu_router.delete('/categoria/produto/{idcategoria}')
async def excluir_categoria_produto(idcategoria: int, usuario: Usuario = Depends(verificar_token), session: Session = Depends(pegar_sessao)):
    if not usuario.admin:
        raise HTTPException(403, 'Você não tem permissão para excluir categoria.')
    
    categoria = session.query(CategoriaProduto).filter(CategoriaProduto.id == idcategoria).first()
    if not categoria:
        raise HTTPException(404, 'Categoria não existe.')

    session.delete(categoria)
    session.commit()
    return {
        'mensagem': 'Categoria excluida.'
    }

@menu_router.post('/produto')
async def criar_produto(produtoschema: ProdutoSchema, usuario: Usuario = Depends(verificar_token), session: Session = Depends(pegar_sessao)):
    if not usuario.admin:
        raise HTTPException(403, 'Você não tem permissão para criar categoria.')
    
    categoria = session.query(CategoriaProduto).filter(CategoriaProduto.id == produtoschema.idcategoria).first()
    if not categoria:
        raise HTTPException(404, 'Categoria não existe.')
   
    produto = Produto(produtoschema.nome, produtoschema.idcategoria)
    session.add(produto)
    session.commit()
    return {
         'mensagem': 'Produto criado.'
    }

@menu_router.delete('/produto/{idproduto}')
async def excluir_produto(idproduto: int, usuario: Usuario = Depends(verificar_token), session: Session = Depends(pegar_sessao)):
    if not usuario.admin:
        raise HTTPException(403, 'Você não tem permissão para excluir categoria.')
    
    produto = session.query(Produto).filter(Produto.id == idproduto).first()
    if not produto:
        raise HTTPException(404, 'Produto não existe.')

    session.delete(produto)
    session.commit()
    return {
        'mensagem': 'Produto excluido.'
    }

@menu_router.post('/produto/variante')
async def criar_produto_variante(produtovarianteschema: ProdutoVarianteSchema, usuario: Usuario = Depends(verificar_token), session: Session = Depends(pegar_sessao)):
    if not usuario.admin:
        raise HTTPException(403, 'Você não tem permissão para criar categoria.')
    
    produto = session.query(Produto).filter(Produto.id == produtovarianteschema.idproduto).first()
    if not produto:
        raise HTTPException(404, 'Produto não existe.')
   
    produtovariante = ProdutoVariante(produtovarianteschema.idproduto, produtovarianteschema.variacao, produtovarianteschema.preco_variante)
    session.add(produtovariante)
    session.commit()
    return {
         'mensagem': 'Produto variante criado.'
    }

@menu_router.delete('/produto/variante/{idprodutovariante}')
async def excluir_produto_variante(idprodutovariante: int, usuario: Usuario = Depends(verificar_token), session: Session = Depends(pegar_sessao)):
    if not usuario.admin:
        raise HTTPException(403, 'Você não tem permissão para excluir categoria.')
    
    produtovariante = session.query(ProdutoVariante).filter(ProdutoVariante.id == idprodutovariante).first()
    if not produtovariante:
        raise HTTPException(404, 'Produto variante não existe.')

    session.delete(produtovariante)
    session.commit()
    return {
        'mensagem': 'Produto variante excluido.'
    }
    