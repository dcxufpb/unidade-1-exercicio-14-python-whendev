# coding: utf-8

import cupom
import pytest
from datetime import datetime

def verifica_item(mensagem_esperada, Venda, itm, pdt, qnt):
  with pytest.raises(Exception) as excinfo:
    Venda.adicionar_item(itm, pdt, qnt)
  the_exception = excinfo.value
  assert mensagem_esperada == str(the_exception)

  
def verifica_campo_obrigatorio_objeto(mensagem_esperada, Venda):
    with pytest.raises(Exception) as excinfo:
        Venda.imprime_cupom()
    the_exception = excinfo.value
    assert mensagem_esperada == str(the_exception)


# Todas as variaveis preenchidas

DATA_HORA_VENDA = datetime(2020, 11, 25, 10, 30, 40)
CCF = "021784"
COO = "035804"


NOME_LOJA = "Loja 1"
LOGRADOURO = "Log 1"
NUMERO = 10
COMPLEMENTO = "C1"
BAIRRO = "Bai 1"
MUNICIPIO = "Mun 1"
ESTADO = "E1"
CEP = "11111-111"
TELEFONE = "(11) 1111-1111"
OBSERVACAO = "Obs 1"
CNPJ = "11.111.111/1111-11"
INSCRICAO_ESTADUAL = "123456789"

# Dados gerais do teste

produto1 = cupom.Produto(100, "Banana", "cx", 7.45, "ST")
produto2 = cupom.Produto(101, "Laranja", "cx", 3.32, "ST")
produto3 = cupom.Produto(102, "Leite", "l", 2.15, "")
produto4 = cupom.Produto(103, "batata", "k", 0, "")


ENDERECO_COMPLETO = cupom.Endereco(LOGRADOURO, NUMERO, COMPLEMENTO, BAIRRO,
                                   MUNICIPIO, ESTADO, CEP)

LOJA_COMPLETA = cupom.Loja(NOME_LOJA, ENDERECO_COMPLETO, TELEFONE, OBSERVACAO,
                           CNPJ, INSCRICAO_ESTADUAL)

VENDA_COMPLETA = LOJA_COMPLETA.vender(DATA_HORA_VENDA, CCF, COO)

VENDA_COMPLETA.adicionar_item(1,produto1, 10)
VENDA_COMPLETA.adicionar_item(2,produto2, 5)

# Cenário 1

TEXTO_ESPERADO_CENARIO_1 = '''Loja 1
Log 1, 10 C1
Bai 1 - Mun 1 - E1
CEP:11111-111 Tel (11) 1111-1111
Obs 1
CNPJ: 11.111.111/1111-11
IE: 123456789
------------------------------
25/11/2020 10:30:40V CCF:021784 COO: 035804
CUPOM FISCAL
ITEM CODIGO DESCRICAO QTD UN VL UNIT(R$) ST VL ITEM(R$)
1 100 Banana 10 cx 7.45 ST 74.50
2 101 Laranja 5 cx 3.32 ST 16.60
------------------------------
TOTAL R$ 91.10'''


def test_cenario1_venda1():
    assert (
        VENDA_COMPLETA.imprime_cupom() == TEXTO_ESPERADO_CENARIO_1
    )

# Cenário 2

TEXTO_ESPERADO_CENARIO_2_VENDA_1 = '''Loja 1
Log 1, 10 C1
Bai 1 - Mun 1 - E1
CEP:11111-111 Tel (11) 1111-1111
Obs 1
CNPJ: 11.111.111/1111-11
IE: 123456789
------------------------------
25/11/2020 10:30:40V CCF:021784 COO: 035804
CUPOM FISCAL
ITEM CODIGO DESCRICAO QTD UN VL UNIT(R$) ST VL ITEM(R$)
1 100 Banana 1 cx 7.45 ST 7.45
------------------------------
TOTAL R$ 7.45'''

cenario2_venda1 = LOJA_COMPLETA.vender(DATA_HORA_VENDA, CCF, COO)
cenario2_venda1.adicionar_item(1, produto1, 1)

def test_cenario2_venda1():
    assert (
        cenario2_venda1.imprime_cupom() == TEXTO_ESPERADO_CENARIO_2_VENDA_1
    )

TEXTO_ESPERADO_CENARIO_2_VENDA_2 = '''Loja 1
Log 1, 10 C1
Bai 1 - Mun 1 - E1
CEP:11111-111 Tel (11) 1111-1111
Obs 1
CNPJ: 11.111.111/1111-11
IE: 123456789
------------------------------
25/11/2020 10:30:40V CCF:021784 COO: 035804
CUPOM FISCAL
ITEM CODIGO DESCRICAO QTD UN VL UNIT(R$) ST VL ITEM(R$)
1 101 Laranja 3 cx 3.32 ST 9.96
------------------------------
TOTAL R$ 9.96'''

cenario2_venda2 = LOJA_COMPLETA.vender(DATA_HORA_VENDA, CCF, COO)
cenario2_venda2.adicionar_item(1, produto2, 3)

def test_cenario2_venda2():
    assert (
        cenario2_venda2.imprime_cupom() == TEXTO_ESPERADO_CENARIO_2_VENDA_2
    )

# Cenário 3

TEXTO_ESPERADO_CENARIO_3 = '''Loja 1
Log 1, 10 C1
Bai 1 - Mun 1 - E1
CEP:11111-111 Tel (11) 1111-1111
Obs 1
CNPJ: 11.111.111/1111-11
IE: 123456789
------------------------------
25/11/2020 10:30:40V CCF:021784 COO: 035804
CUPOM FISCAL
ITEM CODIGO DESCRICAO QTD UN VL UNIT(R$) ST VL ITEM(R$)
1 100 Banana 3 cx 7.45 ST 22.35
2 102 Leite 5 l 2.15  10.75
------------------------------
TOTAL R$ 33.10'''


cenario3_venda1 = LOJA_COMPLETA.vender(DATA_HORA_VENDA, CCF, COO)
cenario3_venda1.adicionar_item(1, produto1, 3)
cenario3_venda1.adicionar_item(2, produto3, 5)

def test_cenario3_venda1():
    assert (
        cenario3_venda1.imprime_cupom() == TEXTO_ESPERADO_CENARIO_3
    )

#Cenario 4

cenario4_venda1 = LOJA_COMPLETA.vender(DATA_HORA_VENDA, CCF, COO)
cenario4_venda1.adicionar_item(1, produto1, 2)

TEXTO_ESPERADO_CENARIO_4_VENDA_1 = "Voce não pode inserir o mesmo produto com itens diferentes"

def test_cenario4_venda1():
  verifica_item(TEXTO_ESPERADO_CENARIO_4_VENDA_1,cenario4_venda1, 2, produto1, 2)


cenario4_venda2 = LOJA_COMPLETA.vender(DATA_HORA_VENDA, CCF, COO)

TEXTO_ESPERADO_CENARIO_4_VENDA_2 = "Insira a quantidade de itens"

def test_cenario4_venda2():
  verifica_item(TEXTO_ESPERADO_CENARIO_4_VENDA_2, cenario4_venda2, 2, produto1, 0)

cenario4_venda3 = LOJA_COMPLETA.vender(DATA_HORA_VENDA, CCF, COO)

TEXTO_ESPERADO_CENARIO_4_VENDA_3 = "item não pode ser adicionado na venda com produto nesse estado"

def test_cenario4_venda3():
  verifica_item(TEXTO_ESPERADO_CENARIO_4_VENDA_3, cenario4_venda3, 2, produto4, 1)


#Cenario 5

cenario5_venda1 = LOJA_COMPLETA.vender(DATA_HORA_VENDA, CCF, COO)

TEXTO_ESPERADO_CENARIO_5_VENDA_1 = "Você precisa inserir itens na sua venda"

def test_cenario5_venda1():
  verifica_campo_obrigatorio_objeto(TEXTO_ESPERADO_CENARIO_5_VENDA_1, cenario5_venda1)