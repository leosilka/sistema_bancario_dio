print('''
=======================================
        SISTEMA BANCÁRIO v2
=======================================
''')
#VARIAVEIS
continuar = True
usuarios = []
contas = []
extrato = []
contador_contas = 1
#FUNÇÃO CADASTRO DO USUARIO
def cadastro_usuario(nome, data_nascimento, cpf):
    usuario = {
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco,
        "contas": [],
        "saldo": 0,
        "numero_saque": 0,
        "extrato": [],
    }
    usuarios.append(usuario)

#FUNÇÃO CADASTRO DE ENDEREÇO
def cadastro_endereco(logradouro, numero, bairro, cidade, estado):
    endereco = {
        "logradouro": logradouro,
        "numero": numero,
        "bairro": bairro,
        "cidade": cidade,
        "estado": estado,        
    }
    return endereco

#FUNÇÃO CADASTRO DE CONTA CORRENTE
def cadastro_conta(agencia, numero_conta, usuario):
    global contador_contas
    conta_corrente = {
        "agencia": agencia,
        "conta": numero_conta
    }
    usuario['contas'].append(conta_corrente)
    contador_contas += 1
    contas.append(conta_corrente)
    return conta_corrente

# Função para exibir o extrato de um usuário
def exibir_extrato(usuario):
    print(f"Extrato do Cliente: {usuario['nome']}")
    for i, transacao in enumerate(usuario["extrato"], start=1):
        tipo, valor = transacao
        if tipo == "deposito":
            print(f"{i}. Depósito: R${valor:.2f}")
        elif tipo == "saque":
            print(f"{i}. Saque: R${valor:.2f}")

#SELEÇÃO DE OPÇÃO
while continuar:
    menu_opcao = int(input('''
Selecione uma das opções:\n
[1] Cadastrar Usuário
[2] Cadastrar Conta Corrente
[3] Realizar Deposito
[4] Realizar Saque
[5] Visualizar Extrato
[6] Usuários Cadastrados
[7] Sair\n\n'''))

    #NESTA PARTE O SISTEMA IRÁ INICIAR O CADASTRO DE USUÁRIO
    if menu_opcao == 1:
        continuar_cadastro = True
        while continuar_cadastro:
            cpf = input("\nInforme o CPF: ")
            
            cpf_existente = False
            for usuario in usuarios:
                if usuario["cpf"] == cpf:
                    cpf_existente = True
                    break
            
            if cpf_existente:
                print("\nCPF ja cadastrado.")
                break
            else:
                nome = input("Informe o nome do usuário: ")
                data_nascimento = input("Informe a data de nascimento: ")
                logradouro = input("Informe o nome do endereço: ")
                numero = int(input("Informe o numero da residencia: "))
                bairro = input("Informe o bairro: ")
                cidade = input("Informe a cidade: ")
                estado = input("Informe o estado: ")
                endereco = cadastro_endereco(logradouro=logradouro, numero=numero, bairro=bairro, cidade=cidade, estado=estado)
                cadastro_usuario(nome=nome, data_nascimento=data_nascimento, cpf=cpf)
                print("\nUsuário cadastrado: ", nome)
                continuar_cadastro = input("Deseja continuar cadastrando? [S/N] ").upper().strip()
                if continuar_cadastro == "S":
                    continuar_cadastro = True
                elif continuar_cadastro == "N":
                    continuar_cadastro = False
                else:
                    print("Opcao Invalida!")
    #NESTA PARTE SISTEMA IRÁ INCIAR O CADASTRO DE CONTA CORRENTE
    elif menu_opcao == 2:
        print("\nCadastro de Conta Corrente!")
        if not usuarios:
            print("Nao ha usuarios cadastrados. Cadastre um usuario antes de criar uma conta!")
            continue

        print("Usuarios disponiveis:")
        for i, usuario in enumerate(usuarios):
            print(f"{i + 1}. {usuario['nome']} ({usuario['cpf']})")

        escolha = int(input("Digite o numero que deseja associar a conta: "))
        if escolha < 1 or escolha > len(usuarios):
            print("Opcao Invalida.")
            continue

        usuario_escolhido = usuarios[escolha - 1]
        agencia = "0001"
        numero_conta = str(contador_contas).zfill(4)

        conta_cadastrada = cadastro_conta(agencia=agencia, numero_conta=numero_conta, usuario=usuario_escolhido)
        if conta_cadastrada:
            print("Conta cadastrada com sucesso: ", conta_cadastrada)
        else:
            print("Falha ao cadastrar a conta.")
    #NESSA PARTE O SISTEMA IRA REALIZAR O DEPOSITO
    elif menu_opcao == 3:
        def deposito (usuario, /, deposito, extrato):
            saldo = usuario["saldo"]
            print(f"Cliente: {usuario['nome']}, Depositado R${valor_deposito:.2f}, Saldo de R${saldo:.2f}")
        if not usuarios:
            print("Nao ha usuarios cadastrados!")
            continue

        print("Usuarios disponiveis:")
        for i, usuario in enumerate(usuarios):
            print(f"{i + 1}. {usuario['nome']} ({usuario['cpf']})")

        escolha = int(input("Selecione o cliente: "))
        if escolha < 1 or escolha > len(usuarios):
            print("Opcao Invalida.")
            continue

        usuario_deposito = usuarios[escolha - 1]
        valor_deposito = float(input("Informe o valor para deposito: R$"))
        usuario_deposito["saldo"] += valor_deposito
        usuario_deposito["extrato"].append(("deposito", valor_deposito))
        deposito(usuario_deposito, valor_deposito, extrato)
    #NESSA PARTE O SISTEMA IRA REALIZAR O SAQUE
    elif menu_opcao == 4:
        def saque(*, usuario, valor_saque,extrato, limite, limite_saque, saldo, numero_saque):
            saldo = usuario["saldo"]
            if valor_saque <= usuario_saque["saldo"]:
                if valor_saque <= LIMITE:
                    if usuario_saque["numero_saque"] <= 3:
                        print(f"Cliente: {usuario['nome']}, Sacado R${valor_saque:.2f}, Saldo de R${saldo:.2f}")
        LIMITE = 500.00
        LIMITE_SAQUE = 3
        saldo = 0
        if not usuarios:
            print("Nao ha usuarios cadastrados!")
            continue
        print("Usuarios disponiveis:")
        for i, usuario in enumerate(usuarios):
            print(f"{i + 1}. {usuario['nome']} ({usuario['cpf']})")
        escolha = int(input("Selecione o cliente: "))
        if escolha < 1 or escolha > len(usuarios):
            print("Opcao Invalida.")
            continue
        usuario_saque = usuarios[escolha - 1]
        numero_saque = usuario_saque.get("numero_saque", 0)
        valor_saque = 0
        if usuario_saque["numero_saque"] <= 3:
            valor_saque = float(input("Informe o valor para saque: R$"))
            if valor_saque <= LIMITE:
                if valor_saque <= usuario_saque["saldo"]:
                    usuario_saque["numero_saque"] += 1
                    usuario_saque["saldo"] -= valor_saque
                    usuario_saque["extrato"].append(("saque", valor_saque))
                else:
                    print("Saque Negado! Voce nao possui saldo!")
            else:
                print("Saque negado! Valor acima do permitido!")
        else:
            print("Saque negado! Voce atingiu o limite de saque!")
        saque(usuario=usuario_saque, valor_saque=valor_saque, extrato=extrato, limite=LIMITE, limite_saque=LIMITE_SAQUE, saldo=saldo, numero_saque=numero_saque)
    #NESSA PARTE O SISTEMA IRA CONSULTAR TODO O EXTRATO
    elif menu_opcao == 5:
        if not usuarios:
            print("Não há usuários cadastrados.")
            continue

        print("Usuários disponíveis:")
        for i, usuario in enumerate(usuarios):
            print(f"{i + 1}. {usuario['nome']} ({usuario['cpf']})")

        escolha = int(input("Selecione o cliente: "))
        if escolha < 1 or escolha > len(usuarios):
            print("Opção inválida.")
            continue

        usuario_extrato = usuarios[escolha - 1]
        exibir_extrato(usuario_extrato)

    #NESTA PARTE O USUÁRIO PODERÁ CONSULTAR OS CADASTROS QUE TEM EM SEU SISTEMA
    elif menu_opcao == 6:
        for i, usuario in enumerate(usuarios):
            print(f"{i + 1}. {usuario['nome']} ({usuario['cpf']})")
            if "contas" in usuario:
                contas_usuario = usuario['contas']
                print("Contas cadastradas:")
                for x, conta in enumerate(contas_usuario):
                    print(f"    Conta {x + 1}: Agencia: {conta['agencia']}, Conta: {conta['conta']}")
                continue
    #NESTA PARTE O USUÁRIO IRÁ ENCERRAR O PROGRAMA
    elif menu_opcao == 7:
        print("\nObrigado por usar nossos serviços!")
        break
    #CASO O USUÁRIO ESCOLHA UMA OPÇÃO INVÁLIDA, ELE RETORNARÁ AO MENU INICIAL
    else:
        print("\nOpção Inválida! Selecione uma opção válida!")
        continue
