async def criar_produto(produtoschema: ProdutoSchema, usuario: Usuario = Depends(verificar_token), session: Session = Depends(pegar_sessao)):
    # if not usuario.admin:
    #     raise HTTPException(403, 'Você não tem permissão para criar categoria.')
    
    # categoria = session.query(CategoriaProduto).filter(CategoriaProduto.id == produtoschema.idcategoria).first()
    # if not categoria:
    #     raise HTTPException(404, 'Categoria não existe.')
    pedido = session.query(Produto).filter(Produto.id == 0).first()
    session.delete(pedido)
    session.commit()
    
    # produto = Produto(produtoschema.nome, produtoschema.idcategoria)
    # session.add(produto)
    # session.commit()
    # return {
    #     'mensagem': 'Produto criado.'
    #}