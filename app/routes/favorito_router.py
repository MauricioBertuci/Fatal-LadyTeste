from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from app.database import get_db
from app.controllers.favorito_controller import *
from fastapi.responses import RedirectResponse
from app.auth import verificar_token 

router = APIRouter(prefix="/favoritos")
templates = Jinja2Templates(directory="app/views/templates")

@router.get("/")
def list_favorites(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("token")
    if not token:
        return RedirectResponse(url="/login", status_code=303)
        
    payload = verificar_token(token)
    if not payload:
        return RedirectResponse(url="/login", status_code=303)
    id_usuario = payload.get("id")

    favoritos = listar_favoritos(id_usuario, db)

    return templates.TemplateResponse(
        "favoritos.html",
        {
            "request": request,
            "favoritos": favoritos,
        },
    )

@router.post("/adicionar/{id_produto}")
def add_favorite(id_produto: int, request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("token")
    payload = verificar_token(token)
    id_usuario = payload.get("id")

    return adicionar_favorito(id_usuario, id_produto, db)

@router.delete("/deletar/{id_produto}")
def delete_favorite(id_produto: int, request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("token")
    payload = verificar_token(token)
    id_usuario = payload.get("id")

    return remover_favorito(id_usuario, id_produto, db)
