import pytest

from app.schemas.produto_schema import ProdutoCreate


def test_produto_create_validacao_preco():
    with pytest.raises(ValueError):
        ProdutoCreate(
            nome="Tênis",
            descricao=None,
            preco=0,
            estoque=1,
            tamanhos=38,
            id_categoria=1,
            id_fabricante=1,
        )


def test_produto_create_validacao_estoque():
    with pytest.raises(ValueError):
        ProdutoCreate(
            nome="Tênis",
            descricao=None,
            preco=100,
            estoque=-1,
            tamanhos=38,
            id_categoria=1,
            id_fabricante=1,
        )


def test_produto_create_com_dados_validos():
    produto = ProdutoCreate(
        nome="Tênis",
        descricao="Confortável",
        preco=199.9,
        estoque=5,
        tamanhos=37,
        id_categoria=2,
        id_fabricante=3,
        caminhoimagem="/img/tenis.png",
    )

    assert produto.nome == "Tênis"
    assert produto.preco == 199.9
    assert produto.estoque == 5