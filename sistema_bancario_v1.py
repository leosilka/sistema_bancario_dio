print('''
=======================================
        SISTEMA BANCÁRIO v1
=======================================
''')
resposta_encerrar = 'S'
saldo = 0
limite = 500
extrato = []
numero_saque = 0
mensagem_encerramento = "Obrigado por usar nosso sistema bancário! Ate mais 😊"
while (resposta_encerrar == 'S'):
    LIMITE_SAQUE = 2
    menu_opcao = int(input('''
    Selecione uma das opções:
        [ 1 ] - Deposito
        [ 2 ] - Saque
        [ 3 ] - Extrato
        [ 4 ] - Sair
    \n'''))

    if (menu_opcao == 1):
        deposito = float(input("Digite o valor que deseja realizar de deposito: "))
        saldo += deposito
        extrato.append(("Deposito", deposito))
        print(f"Deposito no valor de R${deposito:.2f} realizado. Seu saldo atual é R${saldo:.2f}.")
        resposta_encerrar = str(input("Deseja continuar? [S/N]" )).upper().strip()
    elif (menu_opcao == 2):
        if (numero_saque <= LIMITE_SAQUE):
            saque = float(input("Digite o valor que deseja realizar de saque: "))
            if (saque <= limite):
                if (saque <= saldo):
                    saldo -= saque
                    extrato.append(("Saque", saque))
                    numero_saque += 1
                    print(f"Saque realizado. Seu saldo atual é de R${saldo:.2f}.")
                    resposta_encerrar = str(input("Deseja continuar? [S/N]" )).upper().strip()
                elif (saque > saldo):
                    print(f"Saque não autorizado. Você não tem saldo válido!")
                    resposta_encerrar = str(input("Deseja continuar? [S/N]" )).upper().strip()
            else:
                print("Você não pode sacar este valor!")
        else:
            print("Saque não autorizado, você atingiu o limite diário!")
    elif (menu_opcao == 3):
        print("Extrato:")
        for transacao in extrato:
            tipo, valor = transacao
            if tipo == "Deposito":
                print(f"Deposito: R${valor:.2f}")
            elif tipo == "Saque":
                print(f"Saque: R${valor:.2f}")
        print(f"=======================\nSaldo final: R${saldo:.2f}\n=======================")
    elif (menu_opcao == 4):
        print(mensagem_encerramento)
        break
    else:
        print("Opção Inválida! Selecione uma opção válida!")
        continue
    print(mensagem_encerramento)
