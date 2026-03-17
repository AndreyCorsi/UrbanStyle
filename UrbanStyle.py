from dataclasses import dataclass
from datetime import datetime

@dataclass
class Fornecedor:
    id: int
    nome_empresa: str
    cnpj: str

@dataclass
class Produto:
    id: int
    nome: str
    descricao: str
    categoria: str
    tamanho: str
    cor: str
    marca: str
    sku: str
    estoque: int
    estoque_min: int
    valor_custo: float
    valor_venda: float
    margem: float
    id_fornecedor: int
    id_funcionario: int
    id_categoriaR: int

@dataclass
class MovimentoEstoque:
    id: int
    produto_id: int
    tipo: str         
    quantidade: int
    data_hora: str

@dataclass
class Compra:
    id: int
    produto_id: int
    quantidade: int
    total: float
    data_hora: str
    
@dataclass
class Cliente:
    id: int
    nome: str
    cpf: str
    email: str
    endereco: str
    data_nascimento: str
    numero_telefone: str
    id_categoria: int

@dataclass
class Funcionario:
    id: int
    nome: str
    cpf: str
    email: str
    endereco: str
    data_nascimento: str
    numero_telefone: str
    setor: str
    cargo: str
    nivel_permissao: str
    
clientes = []
produtos = []
movimentos = []
compras = []
fornecedores = []
carrinho = []
funcionarios = []

def proximo_id(lista):
    return len(lista) + 1
    
def agora():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
# Fornecedor
def cadastrar_fornecedor():
    print("\n --- CADASTRAR FORNECEDOR ---")
    nome = input("Nome da empresa:")
    cnpj = input("CNPJ:")
    fornecedor = Fornecedor(proximo_id(fornecedores), nome, cnpj)
    fornecedores.append(fornecedor)
    print("Fornecedor cadastrado!")

def listar_fornecedores():
    print("\n--- Fornecedores ---")
    for f in fornecedores:
        print(f)
        
# Produto
def cadastrar_produto():
    if not fornecedores or not funcionarios:
        print("Erro: Cadastre fornecedor e funcionário primeiro.")
        return
    print("\n--- CADASTRAR PRODUTO ---")
    nome = input("Nome: ")
    descricao = input("Descrição: ")
    categoria = input("Categoria: ")
    tamanho = input("Tamanho: ")
    cor = input("Cor: ")
    marca = input("Marca: ")
    sku = input("SKU: ")
    estoque = int(input("Qtd: "))
    estoque_min = int(input("Estoque Mínimo: "))
    custo = float(input("Custo: "))
    venda = float(input("Venda: "))
    margem = venda - custo
    id_fornecedor = int(input("ID Fornecedor: "))
    id_funcionario = int(input("ID Funcionário: "))
    id_categoriaR = int(input("ID CategoriaR (1-Roupas, 2-Calçados, 3-Aces): "))
    
    p = Produto(proximo_id(produtos), nome, descricao, categoria, tamanho, cor, marca, sku, 
                estoque, estoque_min, custo, venda, margem, id_fornecedor, id_funcionario, id_categoriaR)
    produtos.append(p)
    if estoque > 0:
        movimentos.append(MovimentoEstoque(proximo_id(movimentos), p.id, "ENTRADA_INICIAL", estoque, agora()))
    print("Produto cadastrado!")
    
def listar_produtos():
    print("\n--- PRODUTOS ---")
    for p in produtos:
        print(p)
        
# ESTOQUE
def entrada_estoque():
    print("\n--- ENTRADA DE ESTOQUE ---")
    listar_produtos()
    pid = int(input("ID do produto: "))
    quantidade = int(input("Quantidade:"))
    for p in produtos:
        if p.id == pid:
            p.estoque += quantidade
            movimentos.append(MovimentoEstoque(proximo_id(movimentos), pid, "ENTRADA", quantidade, agora()))
            print("Entrada registrada!")
            return

def saida_estoque(tipo):
    print("\n--- SAÍDA DE ESTOQUE ---")
    listar_produtos()
    pid = int(input("ID do produto:"))
    quantidade = int(input("Quantidade:" ))
    for p in produtos:
        if p.id == pid:
            if quantidade <= p.estoque:
                p.estoque -= quantidade
                movimentos.append(MovimentoEstoque(proximo_id(movimentos), pid, tipo, quantidade, agora()))
                print("Saída registrada!")
            else:
                print("Estoque insuficiente.")
            return

# COMPRA
def comprar():
    print("\n--- COMPRA ---")
    listar_produtos()
    pid = int(input("ID do produto:"))
    quantidade = int(input("Quantidade:"))
    for p in produtos:
        if p.id == pid:
            if quantidade <= p.estoque:
                p.estoque -= quantidade
                total = p.valor_venda * quantidade
                compras.append(Compra(proximo_id(compras), pid, quantidade, total, agora()))
                movimentos.append(MovimentoEstoque(proximo_id(movimentos), pid, "SAIDA_VENDA", quantidade, agora()))
                print("Compra realizada! Total:", total)
            else:
                print("Estoque insuficiente.")
            return
                    
def listar_compras():
    print("\n--- COMPRAS ---")
    for c in compras:
        print(c)
        
def listar_movimentos():
    print("\n--- MOVIMENTOS ---")
    for m in movimentos:
        print(m)
        
# CLIENTE
def cadastrar_cliente():
    nome = input("Qual o seu nome: ")
    email = input("Qual o seu email: ")
    numero_telefone = input("Qual seu número de telefone: ")
    endereco = input("Qual seu endereço: ")
    data_nascimento = input("Qual sua data de nascimento: ")
    cpf = input("Qual seu CPF: ")
    id_cat = int(input("ID Categoria (1-Bronze, 2-Prata, 3-Ouro): "))
    c = Cliente(proximo_id(clientes), nome, cpf, email, endereco, data_nascimento, numero_telefone, id_cat)
    clientes.append(c)
    print("Cadastro efetuado com sucesso")
    
def listar_clientes():
    for c in clientes:
        print(c)
        
# Relatório Estoque
def estoque_baixo():
    print("\n ---Produtos com baixo estoque ---")
    for p in produtos:
        if p.estoque < p.estoque_min or p.estoque < 20:
            print(f"Alerta: {p.nome} está com {p.estoque} unidades (Mín SQL: {p.estoque_min})")
            
def produtos_mais_vendidos():
    print("\n--- PRODUTOS MAIS VENDIDOS ---")
    if not compras:
        print("Nenhuma venda registrada.")
        return
    vendas = {}
    for c in compras:
        vendas[c.produto_id] = vendas.get(c.produto_id, 0) + c.quantidade
    ranking = sorted(vendas.items(), key=lambda x: x[1], reverse=True)
    for pid, qtd in ranking:
        nome_p = next((p.nome for p in produtos if p.id == pid), "Desconhecido")
        print(f"{nome_p} | Quantidade: {qtd}")

def produto_menor_saida():
    print("\n--- PRODUTO COM MENOR QUANTIDADE DE SAÍDA ---")
    saidas = {}
    for m in movimentos:
        if "SAIDA" in m.tipo:  
            saidas[m.produto_id] = saidas.get(m.produto_id, 0) + m.quantidade
    if not saidas:
        print("Nenhuma saída registrada.")
        return
    menor_id = min(saidas, key=saidas.get)
    nome_p = next((p.nome for p in produtos if p.id == menor_id), "Desconhecido")
    print(f"Produto: {nome_p} | Saídas: {saidas[menor_id]}")
        
# Relatório Financeiro
def margem_lucro():
    print("\n --- Margem de lucro de um produto ---")
    listar_produtos()
    pid = int(input("Digite o ID do produto: "))
    for p in produtos:
        if p.id == pid:
            m_perc = (p.margem / p.valor_venda) * 100
            print(f"Produto: {p.nome} | Lucro: R$ {p.margem:.2f} | Margem: {m_perc:.2f}%")
            return
    print("Produto não encontrado.")
    
def faturamento():
    print("\n--- FATURAMENTO TOTAL ---")
    total = sum(c.total for c in compras)
    print(f"Faturamento total: R$ {total:.2f}")    
    
# Carrinho
def adicionar_carrinho():
    print("\n--- Adicionar ao carrinho ---")
    listar_produtos()
    pid = int(input("ID do produto: "))
    quantidade = int(input("Quantidade: "))
    for p in produtos:
        if p.id == pid:
            if quantidade <= p.estoque:
                carrinho.append({"produto_id": p.id, "nome": p.nome, "quantidade": quantidade, "valor": p.valor_venda})
                print("Produto adicionado!")
                return
            else:
                print("Estoque insuficiente.")
                return
    print("Produto não encontrado.")
    
def ver_carrinho():
    print("\n--- Ver Carrinho ---")
    if not carrinho:
        print("Carrinho vazio.")
        return
    total = 0
    for item in carrinho:
        subtotal = item["quantidade"] * item["valor"]
        total += subtotal
        print(f'{item["nome"]} | Qtd: {item["quantidade"]} | Subtotal: R$ {subtotal:.2f}')
    print(f"\nTOTAL: R$ {total:.2f}")
    
def finalizar_carrinho():
    print("\n--- FINALIZAR COMPRA ---")
    if not carrinho:
        print("Carrinho vazio.")
        return
    confirmar = input("Confirmar compra? (s/n): ")
    if confirmar.lower() == "s":
        for item in carrinho:
            for p in produtos:
                if p.id == item["produto_id"]:
                    p.estoque -= item["quantidade"]
                    compras.append(Compra(proximo_id(compras), p.id, item["quantidade"], item["quantidade"]*p.valor_venda, agora()))
                    movimentos.append(MovimentoEstoque(proximo_id(movimentos), p.id, "SAIDA_VENDA", item["quantidade"], agora()))
        carrinho.clear()
        print("Compra finalizada!")

#Funcionarios
def cadastrar_funcionario():
    nome = input("Qual o seu nome: ")
    email = input("Qual o seu email: ")
    numero_telefone = input("Qual seu número de telefone: ")
    endereco = input("Qual seu endereço: ")
    data_nascimento = input("Qual sua data de nascimento: ")
    cpf = input("Qual seu CPF: ")
    setor = input("Setor: ")
    cargo = input("Cargo: ")
    perm = input("Nível Permissão: ")
    f = Funcionario(proximo_id(funcionarios), nome, cpf, email, endereco, data_nascimento, numero_telefone, setor, cargo, perm)
    funcionarios.append(f)
    print("Cadastro efetuado com sucesso")

def listar_funcionarios():
    print("\n--- Funcionarios ---")
    for f in funcionarios:
        print(f)
    
# MENU
def menuADM():
    while True:
        print("\n ----Urban Style----")
        print("1 - Cadastro fornecedor")
        print("2 - Cadastrado produto")
        print("3 - Cadastrado cliente")
        print("4 - Cadastro de funcionario")
        print("5 - Realizar compra")
        print("6 - Listar produtos")
        print("7 - Listar compras")
        print("8 - Listar clientes")
        print("9 - Listar funcionarios")
        print("0 - Sair")
        op = input("Escolha: ")
        if op == "1": cadastrar_fornecedor()
        elif op == "2": cadastrar_produto()
        elif op == "3": cadastrar_cliente()
        elif op == "4": cadastrar_funcionario()
        elif op == "5": comprar()
        elif op == "6": listar_produtos()
        elif op == "7": listar_compras()
        elif op == "8": listar_clientes()
        elif op == "9": listar_funcionarios()
        elif op =="0": break

def menuoperacional():
    while True:
        print("\n--- MENU CLIENTE ---")
        print("1 - Cadastrado cliente")
        print("2 - Listar clientes")
        print("3 - Adicionar carrinho")
        print("4 - Visualizar carrinho")
        print("5 - Finalizar compra")
        print("0 - Sair")
        op = input("Escolha: ")
        if op == "1": cadastrar_cliente()
        elif op == "2": listar_clientes()
        elif op == "3": adicionar_carrinho()
        elif op == "4": ver_carrinho()
        elif op == "5": finalizar_carrinho()
        elif op == "0": break
            
def menurelatorioestoq():
    while True:
        print("\n--- RELATÓRIO ESTOQUE ---")
        print("1 - Produtos com baixo estoque ")
        print("2 - Produto com menor quantidade de saida ")
        print("0 - Sair")
        op = input("Escolha:")
        if op == "1": estoque_baixo()
        elif op == "2": produto_menor_saida()
        elif op == "0": break
            
def menurelatoriofinan():
    while True:
        print("\n--- RELATÓRIO FINANCEIRO ---")
        print("1 - Margem de lucros")
        print("2 - Produtos mais vendidos")
        print("3 - Faturamento")
        print("0 - Sair")
        op = input("Escolha:")
        if op == "1": margem_lucro()
        elif op == "2": produtos_mais_vendidos()
        elif op == "3": faturamento()
        elif op == "0": break
            
def menurelatorios():
    while True:
        print("\n--- MENU RELATÓRIOS ---")
        print("1 - Relatório Estoque")
        print("2 - Relatório Financeiro")
        print("0 - Sair")
        op = input("Escolha:")
        if op == "1": menurelatorioestoq()
        elif op == "2": menurelatoriofinan()
        elif op == "0": break
    
def menumovimentoestoque():
    while True:
        print("\n--- MOVIMENTAÇÃO ESTOQUE ---")
        print("1 - Entrada de estoque")
        print("2 - Saída por venda")
        print("3 - Saída por troca")
        print("4 - Saída por avaria")
        print("5 - Listar movimentos")
        print("0 - Sair")
        op = input("Escolha:")
        if op == "1": entrada_estoque()
        elif op == "2": saida_estoque("SAIDA_VENDA")
        elif op == "3": saida_estoque("SAIDA_TROCA")
        elif op == "4": saida_estoque("SAIDA_AVARIA")
        elif op == "5": listar_movimentos()
        elif op == "0": break
        
def menu():
    while True:
        print("\n========== URBAN STYLE SYSTEM ==========")
        print("1 - Área administrativa")
        print("2 - Área do cliente")
        print("3 - Área de movimento de estoque")
        print("4 - Relatórios")
        print("0 - Sair")
        op = input("Escolha: ")
        if op == "1": menuADM()
        elif op == "2": menuoperacional()
        elif op == "3": menumovimentoestoque()
        elif op == "4": menurelatorios()
        elif op == "0": break
            
menu()
