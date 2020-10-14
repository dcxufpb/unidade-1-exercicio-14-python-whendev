# coding: utf-8

class Endereco:
  
  def __init__(self, logradouro, numero, complemento, bairro, municipio, 
      estado, cep):
    self.logradouro = logradouro
    self.numero = numero
    self.complemento = complemento
    self.bairro = bairro
    self.municipio = municipio
    self.estado = estado
    self.cep = cep
  def validar_campos_obrigatorios(self):
    if (self.logradouro == "" or self.logradouro == None):
      raise Exception("O campo logradouro do endereço é obrigatório")

    if (self.numero == 0):
      self.numero = "s/n"
    
    if (self.municipio == "" or self.municipio == None):
      raise Exception("O campo município do endereço é obrigatório")
    
    if (self.estado == "" or self.estado == None):
      raise Exception("O campo estado do endereço é obrigatório")

  def dados_endereco(self):
      # Implemente aqui
    self.validar_campos_obrigatorios()
    
    _COMPLEMENTO = " " + self.complemento if self.complemento else ""

    _BAIRRO = self.bairro + " - " if self.bairro else ""

    _CEP = "CEP:" + self.cep if self.cep else ""

    _NUMERO =  self.numero if self.numero else "s/n"

    return f'''{self.logradouro}, {_NUMERO}{_COMPLEMENTO}
{_BAIRRO}{self.municipio} - {self.estado}
{_CEP}'''

class Loja:
  
  def __init__(self, nome_loja, endereco, telefone, observacao, cnpj, 
      inscricao_estadual):
    self.nome_loja = nome_loja
    self.endereco = endereco
    self.telefone = telefone
    self.observacao = observacao
    self.cnpj = cnpj
    self.inscricao_estadual = inscricao_estadual
    self.vendas = []

  def vender(self, datahora, ccf, coo):
    _venda = Venda(self, datahora, ccf, coo)
    self.vendas.append(_venda)
    return _venda
  

  def validar_campos_obrigatorios(self):
    if (self.nome_loja == "" or self.nome_loja == None):
      raise Exception("O campo nome da loja é obrigatório")
    
    if (self.cnpj == "" or self.cnpj == None):
      raise Exception("O campo CNPJ da loja é obrigatório")
    
    if (self.inscricao_estadual == "" or self.inscricao_estadual == None):
      raise Exception("O campo inscrição estadual da loja é obrigatório")

  def dados_loja(self):
    # Implemente aqui
    self.validar_campos_obrigatorios()

    _TELEFONE = ""
    
    if(self.endereco.cep):
      _TELEFONE = " Tel " + self.telefone if self.telefone else ""
    else:
      _TELEFONE = "Tel " + self.telefone if self.telefone else ""

    _OBSERVACAO = self.observacao if self.observacao else ""

    show = f'''{self.nome_loja}
{self.endereco.dados_endereco()}{_TELEFONE}
{_OBSERVACAO}
CNPJ: {self.cnpj}
IE: {self.inscricao_estadual}'''
    return show

class Produto:

  def __init__(self, codigo, descricao, unidade, valor_unitario, substituicao_tributaria):
    self.codigo = codigo
    self.descricao = descricao
    self.unidade = unidade
    self.valor_unitario = valor_unitario
    self.substituicao_tributaria = substituicao_tributaria

class Item:

  def __init__(self, venda, item, produto, quantidade):
    self.venda = venda
    self.item = item
    self.produto = produto
    self.quantidade = quantidade

  def valor_item(self):
    return self.quantidade * self.produto.valor_unitario

  def dados_item(self):
    return f'''{self.item} {self.produto.codigo} {self.produto.descricao} {self.quantidade} {self.produto.unidade} {self.produto.valor_unitario:.2f} {self.produto.substituicao_tributaria} {self.valor_item():.2f}\n'''

class Venda:

  def __init__(self, loja, datahora, ccf, coo):
    self.loja = loja
    self.datahora = datahora
    self.ccf = ccf
    self.coo = coo
    self.itens = []
    

  def validar_campos_obrigatorios(self):
    if not self.coo:
      raise Exception("O campo coo da venda é obrigatório")
    
    if not self.ccf:
      raise Exception("O campo ccf da venda é obrigatório")

    if not self.datahora:
      raise Exception("O campo data da venda é obrigatório")

    if not self.itens:
      raise Exception("Você precisa inserir itens na sua venda")

  def duplicado(self, produto, item):
    for itemlist in self.itens:
      if(itemlist.item != item and itemlist.produto.codigo == produto.codigo):
        return True
    return False

  def valida_item(self, item, produto, quantidade):
    if(self.duplicado(produto, item)):
      raise Exception("Voce não pode inserir o mesmo produto com itens diferentes")

    if(quantidade <= 0):
      raise Exception("Insira a quantidade de itens")

    if(produto.valor_unitario <= 0):
      raise Exception("item não pode ser adicionado na venda com produto nesse estado")
    

  def adicionar_item(self, item, produto, quantidade):
    self.valida_item(item, produto, quantidade)

    _itemVenda = Item(self, item, produto, quantidade)
    self.itens.append(_itemVenda)
  
  def dados_itens(self):
    _dados = "ITEM CODIGO DESCRICAO QTD UN VL UNIT(R$) ST VL ITEM(R$)\n"

    for item in self.itens:
      _dados += item.dados_item()

    return _dados

  def calcular_total(self):
    _total = 0
    for i in self.itens:
      _total += i.valor_item()
    
    return _total

      
  def dados_venda(self):
    self.validar_campos_obrigatorios()

    _texto_data = self.datahora.strftime("%d/%m/%Y")

    _texto_hora = self.datahora.time().strftime("%H:%M:%S")

    _dadosVenda = f'''{_texto_data} {_texto_hora}V CCF:{self.ccf} COO: {self.coo}'''
    return _dadosVenda

  def imprime_cupom(self):
    _dadosLoja = self.loja.dados_loja()

    _dadosVenda = self.dados_venda()
    _dadosItens = self.dados_itens()
    _cupom = "CUPOM FISCAL"
    return f'''{_dadosLoja}\n------------------------------\n{_dadosVenda}\n{_cupom}\n{_dadosItens}------------------------------\nTOTAL R$ {self.calcular_total():.2f}'''
