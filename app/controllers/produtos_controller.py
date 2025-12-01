from app.database import *
from sqlalchemy import Date
from fastapi import Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session, joinedload
from app.auth import verificar_token
from app.models.usuario_model import UsuarioDB
from app.models.produto_model import ProdutoDB
from app.models.categoria_model import CategoriaDB
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import joinedload

import os
import unicodedata
from collections import defaultdict

templates = Jinja2Templates(directory="app/views/templates")

# imagens por categoria

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_PRODUCTS_DIR = os.path.join(
    BASE_DIR,
    "views",
    "static",
    "uploads",
    "img",
    "catalogo",
    "products",
)

IMAGES_URL_PREFIX = "/static/uploads/img/catalogo/products"

# mapeia categoria normalizada -> pasta de imagens
CATEGORY_FOLDER_BY_KEY = {
    "tenis": "tenis",
    "sandalia": "sandalia",
    "rasteirinha": "rasteira",
    "sapatilha": "sapatilha",
    "salto alto": "scarpins",
    "scarpins": "scarpins",
    "bota": "botas",
    "botas": "botas",
}


def _normalize_categoria_nome(nome: str) -> str:
    """
    remove acentos, converte para minúsculo e tira espaços extras
    """
    if not nome:
        return ""
    normalized = unicodedata.normalize("NFD", nome)
    normalized = "".join(
        ch for ch in normalized
        if unicodedata.category(ch) != "Mn"
    )
    return normalized.lower().strip()


def _load_category_images() -> dict[str, list[str]]:
    """
    lê as pastas de produtos dentro de STATIC_PRODUCTS_DIR e monta
    uma lista de URLs de imagem para cada pasta.
    """
    imagens_por_pasta: dict[str, list[str]] = {}

    if not os.path.isdir(STATIC_PRODUCTS_DIR):
        return imagens_por_pasta

    for pasta in set(CATEGORY_FOLDER_BY_KEY.values()):
        dir_categoria = os.path.join(STATIC_PRODUCTS_DIR, pasta)
        if not os.path.isdir(dir_categoria):
            continue

        arquivos = [
            f
            for f in os.listdir(dir_categoria)
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".gif"))
            and not f.startswith(".")
        ]

        arquivos.sort()

        imagens_por_pasta[pasta] = [
            f"{IMAGES_URL_PREFIX}/{pasta}/{nome_arquivo}"
            for nome_arquivo in arquivos
        ]

    return imagens_por_pasta


CATEGORY_IMAGES = _load_category_images()


def get_images_for_category(nome_categoria: str) -> list[str]:
    """
    usa o nome da categoria do banco para achar a pasta e retornar
    a lista de URLs daquelas imagens.
    """
    key = _normalize_categoria_nome(nome_categoria)
    pasta = CATEGORY_FOLDER_BY_KEY.get(key)
    if not pasta:
        return []
    return CATEGORY_IMAGES.get(pasta, [])


# funções

# def listar_produto(request: Request, db: Session):
#     token = request.cookies.get("token")

#     if token:
#         payload = verificar_token(token)
#         if payload:
#             email = payload.get("sub")
#             usuario = db.query(UsuarioDB).filter_by(email=email).first()
#         else:
#             usuario = None  # token inválido
#     else:
#         usuario = None  # nenhum token no cookie

#     produtos = db.query(ProdutoDB).all()

#     return templates.TemplateResponse(
#         "catalogo.html",
#         {"request": request, "usuario": usuario, "produtos": produtos}
#     )

def produtos_por_categoria(request: Request, db: Session):
    token = request.cookies.get("token")
    usuario = None

    if token:
        payload = verificar_token(token)
        if payload:
            email = payload.get("sub")
            usuario = db.query(UsuarioDB).filter_by(email=email).first()

    produtos = (
        db.query(ProdutoDB)
        .options(joinedload(ProdutoDB.categoria))
        .order_by(ProdutoDB.id_produto)  # ordenação estável
        .all()
    )

    # aplica a mesma regra de imagem para todos os produtos
    for produto in produtos:
        atribuir_imagem_para_produto(produto)

    # monta lista de categorias se o template precisar
    categorias_map: dict[int, CategoriaDB] = {}
    for produto in produtos:
        if produto.categoria:
            categorias_map[produto.categoria.id] = produto.categoria

    categorias = list(categorias_map.values())

    return templates.TemplateResponse(
        "catalogo.html",
        {
            "request": request,
            "usuario": usuario,
            "produtos": produtos,
            "categorias": categorias,
        },
    )


def get_produto(request: Request, id_produto: int, db: Session):
    token = request.cookies.get("token")
    if not token:
        return RedirectResponse(url="/login", status_code=303)

    payload = verificar_token(token)
    if not payload:
        return RedirectResponse(url="/login", status_code=303)

    email = payload.get("sub")

    produto = (
        db.query(ProdutoDB)
        .options(joinedload(ProdutoDB.categoria))
        .filter(ProdutoDB.id_produto == id_produto)
        .first()
    )

    # aplica a MESMA função de imagem
    if produto:
        atribuir_imagem_para_produto(produto)

    usuario = db.query(UsuarioDB).filter_by(email=email).first()

    return templates.TemplateResponse(
        "produto.html",
        {
            "request": request,
            "produto": produto,
            "usuario": usuario,
        },
    )



def atribuir_imagem_para_produto(produto: ProdutoDB) -> None:
    """
    define produto.caminhoimagem de forma determinística com base na categoria
    e no id do produto. a mesma regra vale para /produtos e /produto.
    """
    # se já tem imagem no banco, não mexe
    if produto.caminhoimagem:
        return

    # se não tem categoria, não tem como associar
    if not produto.categoria:
        return

    imagens_categoria = get_images_for_category(produto.categoria.nome)
    if not imagens_categoria:
        return

    total_imagens = len(imagens_categoria)

    # usa o id do produto para gerar um índice estável
    pid = getattr(produto, "id_produto", None)
    if not pid:
        # fallback paranoico
        produto.caminhoimagem = imagens_categoria[0]
        return

    # se id começar em 1, (pid - 1) deixa o primeiro produto da categoria na primeira imagem
    idx = (pid - 1) % total_imagens
    produto.caminhoimagem = imagens_categoria[idx]
