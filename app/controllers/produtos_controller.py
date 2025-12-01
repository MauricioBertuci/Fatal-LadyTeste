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

import os
import unicodedata
from collections import defaultdict

templates = Jinja2Templates(directory="app/views/templates")

# ===================== CONFIG IMAGENS POR CATEGORIA =====================

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
    "rasteira": "rasteira",
    "sapatilha": "sapatilha",
    "scarpin": "scarpins",
    "scarpins": "scarpins",
    "bota": "botas",
    "botas": "botas",
}


def _normalize_categoria_nome(nome: str) -> str:
    """
    Remove acentos, converte para minúsculo e tira espaços extras.
    Ex.: 'Tênis ' -> 'tenis'
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
    Lê as pastas de produtos dentro de STATIC_PRODUCTS_DIR e monta
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
    Usa o nome da categoria do banco para achar a pasta e retornar
    a lista de URLs daquelas imagens.
    """
    key = _normalize_categoria_nome(nome_categoria)
    pasta = CATEGORY_FOLDER_BY_KEY.get(key)
    if not pasta:
        return []
    return CATEGORY_IMAGES.get(pasta, [])


# ============================ FUNÇÕES ============================

def listar_produto(request: Request, db: Session):
    token = request.cookies.get("token")

    if token:
        payload = verificar_token(token)
        if payload:
            email = payload.get("sub")
            usuario = db.query(UsuarioDB).filter_by(email=email).first()
        else:
            usuario = None  # token inválido
    else:
        usuario = None  # nenhum token no cookie

    produtos = db.query(ProdutoDB).all()

    return templates.TemplateResponse(
        "catalogo.html",
        {"request": request, "usuario": usuario, "produtos": produtos}
    )


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
        .all()
    )

    # Agrupa produtos por categoria para distribuir as imagens
    grupos_por_categoria: dict[int, list[ProdutoDB]] = defaultdict(list)
    for produto in produtos:
        if produto.categoria:
            grupos_por_categoria[produto.categoria.id].append(produto)

    # Para cada categoria, distribui as N imagens entre os produtos usando módulo
    for grupo in grupos_por_categoria.values():
        if not grupo:
            continue

        categoria_nome = grupo[0].categoria.nome if grupo[0].categoria else ""
        imagens_categoria = get_images_for_category(categoria_nome)
        if not imagens_categoria:
            continue

        total_imagens = len(imagens_categoria)

        for idx, produto in enumerate(grupo):
            # só sobrescreve se não tiver caminhoimagem no banco
            if not produto.caminhoimagem:
                produto.caminhoimagem = imagens_categoria[idx % total_imagens]

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
    produto = db.query(ProdutoDB).filter(ProdutoDB.id_produto == id_produto).first()

    # se não tiver imagem no banco, tenta pegar a da categoria
    if produto and not produto.caminhoimagem and produto.categoria:
        imagens_categoria = get_images_for_category(produto.categoria.nome)
        if imagens_categoria:
            produto.caminhoimagem = imagens_categoria[0]

    usuario = db.query(UsuarioDB).filter_by(email=email).first()
    return templates.TemplateResponse(
        "produto.html",
        {
            "request": request,
            "produto": produto,
            "usuario": usuario,
        },
    )
