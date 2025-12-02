from app import auth


def test_password_hash_and_verify():
    senha = "SenhaSegura123"
    senha_hash = auth.gerar_hash_senha(senha)

    assert auth.verificar_senha(senha, senha_hash) is True
    assert auth.rehash_password_if_needed(senha, senha_hash) is None


def test_criar_e_verificar_token():
    payload = {"sub": "usuario@example.com", "id": 42}
    token = auth.criar_token(payload, expires_minutes=1)

    decoded = auth.verificar_token(token)
    assert decoded is not None
    assert decoded["sub"] == payload["sub"]
    assert decoded["id"] == payload["id"]
    assert "exp" in decoded

    # Token alterado deve falhar
    token_invalido = token + "invalid"
    assert auth.verificar_token(token_invalido) is None