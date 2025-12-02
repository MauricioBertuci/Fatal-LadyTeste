import importlib
import sys
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Inclui raiz do projeto no PYTHONPATH
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from app.database import Base

# Garante que todos os models estejam registrados no metadata
for module_path in [
    "app.models.categoria_model",
    "app.models.fabricante_model",
    "app.models.produto_model",
    "app.models.usuario_model",
    "app.models.pedido_model",
    "app.models.enderecos_model",
    "app.models.carrinho_model",
    "app.models.favorito_model",
    "app.models.pagamento_model",
]:
    importlib.import_module(module_path)


@pytest.fixture(scope="session")
def test_engine():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture()
def db_session(test_engine):
    TestingSessionLocal = sessionmaker(bind=test_engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()