from app import ultils


def test_validar_cpf_valido_e_invalido():
    cpf_valido = "529.982.247-25"
    cpf_invalido = "123.456.789-00"

    assert ultils.validar_cpf(cpf_valido) is True
    assert ultils.validar_cpf(cpf_invalido) is False


def test_validar_cpf_string_curta():
    assert ultils.validar_cpf("123") is False