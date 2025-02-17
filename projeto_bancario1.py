def exibir_menu():
    """Exibe o menu de opções e retorna a escolha do usuário."""
    return input("""
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [q] Sair

    => """)

def depositar(saldo, extrato):
    """Realiza um depósito e retorna o saldo e extrato atualizados."""
    try:
        valor = float(input("Informe o valor do depósito: "))
        if valor > 0:
            saldo += valor
            extrato.append(f"Depósito: R$ {valor:.2f}")
            print("Depósito realizado com sucesso!")
        else:
            print("Operação falhou! O valor informado é inválido.")
    except ValueError:
        print("Operação falhou! Digite um valor numérico.")
    
    return saldo, extrato

def sacar(saldo, extrato, numero_saques, limite, LIMITE_SAQUES):
    """Realiza um saque e retorna os valores atualizados."""
    try:
        valor = float(input("Informe o valor do saque: "))

        if valor > saldo:
            print("Operação falhou! Você não tem saldo suficiente.")
        elif valor > limite:
            print("Operação falhou! O valor do saque excede o limite.")
        elif numero_saques >= LIMITE_SAQUES:
            print("Operação falhou! Número máximo de saques excedido.")
        elif valor > 0:
            saldo -= valor
            extrato.append(f"Saque: R$ {valor:.2f}")
            numero_saques += 1
            print("Saque realizado com sucesso!")
        else:
            print("Operação falhou! O valor informado é inválido.")
    except ValueError:
        print("Operação falhou! Digite um valor numérico.")

    return saldo, extrato, numero_saques

def exibir_extrato(saldo, extrato):
    """Exibe o extrato das operações realizadas."""
    print("\n================ EXTRATO ================")
    print("\n".join(extrato) if extrato else "Não foram realizadas movimentações.")
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

def main():
    saldo = 0
    limite = 500
    extrato = []
    numero_saques = 0
    LIMITE_SAQUES = 3

    while True:
        opcao = exibir_menu()

        if opcao == "d":
            saldo, extrato = depositar(saldo, extrato)
        elif opcao == "s":
            saldo, extrato, numero_saques = sacar(saldo, extrato, numero_saques, limite, LIMITE_SAQUES)
        elif opcao == "e":
            exibir_extrato(saldo, extrato)
        elif opcao == "q":
            print("Saindo do sistema. Obrigado por usar nosso banco!")
            break
        else:
            print("Operação inválida, por favor selecione novamente.")

if __name__ == "__main__":
    main()
