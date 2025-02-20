from datetime import datetime

menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[u] Criar Usuário (Cliente)
[c] Criar Conta Corrente (Vincular com Usuário)
[q] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3
usuarios = []  # Lista para armazenar os usuários
contas = []  # Lista para armazenar as contas correntes
numero_conta_sequencial = 1  # Inicia o número da conta em 1

# Funções para Operações Bancárias
def realizar_deposito(saldo, valor, extrato):  # Parâmetros apenas por posição
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
    else:
        print("Operação falhou! O valor informado é inválido.")
    
    return saldo, extrato

def realizar_saque(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    if valor <= 0:
        print("Operação falhou! O valor informado é inválido.")
        return saldo, extrato

    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")
    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")
    else:
        saldo -= valor
        # Adiciona a data e hora no formato "dia-mês-ano" ao extrato
        data_hora_saque = datetime.now().strftime("%d-%m-%Y")
        extrato += f"Saque: R$ {valor:.2f} em {data_hora_saque}\n"
        numero_saques += 1
        print(f"Saque de R$ {valor:.2f} realizado com sucesso!")

    return saldo, extrato

def exibir_extrato(saldo, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

# Função para criar usuário
def criar_usuario():
    nome = input("Informe o nome do usuário: ")
    data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
    cpf = input("Informe o CPF do usuário (apenas números): ")
    
    # Verificar se o CPF já está cadastrado
    if any(usuario['cpf'] == cpf for usuario in usuarios):
        print("CPF já cadastrado! Não é possível cadastrar novamente.")
        return

    endereco = input("Informe o endereço do usuário (logradouro, número, bairro, cidade/sigla Estado): ")
    
    # Criar o dicionário do usuário
    usuario = {"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco}
    usuarios.append(usuario)
    print(f"Usuário {nome} cadastrado com sucesso!")

# Função para criar conta corrente e vincular com usuário através do CPF
def criar_conta_corrente():
    global numero_conta_sequencial  # Tornar a variável acessível dentro da função

    if not usuarios:
        print("Não há usuários cadastrados. Crie um usuário antes de criar uma conta.")
        return

    cpf_informado = input("Informe o CPF do usuário (apenas números) para vincular a conta: ")

    # Procurar o usuário com o CPF informado
    usuario_encontrado = next((usuario for usuario in usuarios if usuario['cpf'] == cpf_informado), None)

    if usuario_encontrado is None:
        print("Usuário com o CPF informado não encontrado.")
        return

    # Criar uma nova conta para o usuário encontrado
    conta = {"agencia": "0001", "numero_conta": numero_conta_sequencial, "usuario": usuario_encontrado}
    contas.append(conta)

    # Incrementar o número da conta para a próxima
    numero_conta_sequencial += 1

    print(f"Conta corrente {conta['numero_conta']} criada e vinculada ao usuário {usuario_encontrado['nome']} com sucesso!")

# Função para autenticar o usuário
def autenticar_usuario():
    # Solicita nome e CPF do usuário, com a opção de sair
    nome_informado = input("Informe seu nome ou digite 'sair' para sair: ")
    
    if nome_informado.lower() == 'sair':
        print("Saindo do programa...")
        return None  # Retorna None para indicar que o usuário escolheu sair

    cpf_informado = input("Informe seu CPF (apenas números): ")
    
    # Buscar usuário pelo nome e CPF
    usuario_autenticado = next((usuario for usuario in usuarios if usuario['nome'] == nome_informado and usuario['cpf'] == cpf_informado), None)

    if usuario_autenticado is None:
        print("Usuário não encontrado ou dados incorretos.")
        cadastro = input("Deseja se cadastrar? (s/n): ").strip().lower()
        if cadastro == "s":
            criar_usuario()
        else:
            print(f"Saudação: Olá, {nome_informado}. Programa encerrado.")
            return None  # Retorna None para encerrar a aplicação
    else:
        print(f"Usuário {usuario_autenticado['nome']} autenticado com sucesso!")
        return usuario_autenticado

# Loop Principal
while True:
    usuario = autenticar_usuario()
    if usuario is None:
        break  # Se o usuário escolheu sair, sai do loop principal
    
    while True:
        opcao = input(menu)

        if opcao == "d":
            try:
                valor = float(input("Informe o valor do depósito: "))
                saldo, extrato = realizar_deposito(saldo, valor, extrato)  # Passando parâmetros por posição
            except ValueError:
                print("Valor inválido! Por favor, insira um número.")

        elif opcao == "s":
            try:
                valor = float(input("Informe o valor do saque: "))
                saldo, extrato = realizar_saque(saldo=saldo, valor=valor, extrato=extrato, limite=limite, numero_saques=numero_saques, limite_saques=LIMITE_SAQUES)  # Parâmetros por nome
            except ValueError:
                print("Valor inválido! Por favor, insira um número.")

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)  # Passando saldo por posição e extrato por nome

        elif opcao == "u":
            criar_usuario()

        elif opcao == "c":
            criar_conta_corrente()

        elif opcao == "q":
            print("Saindo...")
            break  # Sai do loop interno de operações bancárias

    if opcao == "q":
        break  # Sai do loop principal, encerrando o programa
