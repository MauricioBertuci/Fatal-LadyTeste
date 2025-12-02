from datetime import date

from app.models.categoria_model import CategoriaDB
from app.models.produto_model import ProdutoDB
from app.models.usuario_model import UsuarioDB
from app.models.favorito_model import FavoritoDB
from app.models.pedido_model import PedidoDB, ItemPedidoDB


def test_produto_relacionamento_categoria(db_session):
    categoria = CategoriaDB(nome="Tênis", descricao="Calçados esportivos")
    db_session.add(categoria)
    db_session.flush()

    produto = ProdutoDB(
        nome="Tênis Run",
        preco=299.9,
        estoque=10,
        tamanhos=38,
        id_categoria=categoria.id,
        id_fabricante=1,
        caminhoimagem="/img/tenis.png",
    )
    db_session.add(produto)
    db_session.commit()

    produto_db = db_session.query(ProdutoDB).first()
    assert produto_db is not None
    assert produto_db.categoria is not None
    assert produto_db.categoria.nome == "Tênis"


def test_usuario_favoritos_relacionamento(db_session):
    usuario = UsuarioDB(
        nome="Maria",
        email="maria@example.com",
        senha="hash",
        telefone="11999999999",
        cpf="12345678901",
        genero="F",
        data_nascimento=date(1990, 1, 1),
    )
    db_session.add(usuario)
    db_session.flush()

    favorito = FavoritoDB(id_usuario=usuario.id_cliente)
    db_session.add(favorito)
    db_session.commit()

    usuario_db = db_session.query(UsuarioDB).first()
    assert usuario_db.favoritos
    assert usuario_db.favoritos[0].id_usuario == usuario_db.id_cliente


def test_pedido_item_relacionamento(db_session):
    categoria = CategoriaDB(nome="Sandália", descricao="Calçados femininos")
    produto = ProdutoDB(
        nome="Sandália Confort",
        preco=120.0,
        estoque=5,
        tamanhos=37,
        id_categoria=1,
        id_fabricante=1,
        caminhoimagem="/img/sandalia.png",
    )
    db_session.add_all([categoria, produto])
    db_session.flush()

    usuario = UsuarioDB(
        nome="João",
        email="joao@example.com",
        senha="hash",
        telefone="11888888888",
        cpf="10987654321",
        genero="M",
        data_nascimento=date(1985, 5, 5),
    )
    db_session.add(usuario)
    db_session.flush()

    pedido = PedidoDB(id_cliente=usuario.id_cliente, status="novo", valortotal=0, valorfrete=0)
    item = ItemPedidoDB(
        produto_id=produto.id_produto,
        nome_produto=produto.nome,
        preco_unitario=produto.preco,
        quantidade=2,
        tamanho=produto.tamanhos,
    )
    pedido.itens.append(item)
    db_session.add(pedido)
    db_session.commit()

    pedido_db = db_session.query(PedidoDB).first()
    assert pedido_db is not None
    assert pedido_db.itens
    assert pedido_db.itens[0].quantidade == 2
    assert pedido_db.itens[0].pedido_id == pedido_db.id