agendamentos = []
id_contador = 1

tipos_medicos = [
    "Cardiologia - Dr. João",
    "Pediatria - Dra. Maria",
    "Ortopedia - Dr. Lucas",
    "Dermatologia - Dra. Ana",
    "Ginecologia - Dra. Paula",
    "Clínico Geral - Dr. Roberto"
]

horarios_disponiveis = {
    "Cardiologia - Dr. João": ["08:00", "09:00", "10:00"],
    "Pediatria - Dra. Maria": ["13:00", "14:00", "15:00"],
    "Ortopedia - Dr. Lucas": ["09:30", "10:30", "11:30"],
    "Dermatologia - Dra. Ana": ["08:30", "09:30", "10:30"],
    "Ginecologia - Dra. Paula": ["14:00", "15:00", "16:00"],
    "Clínico Geral - Dr. Roberto": ["07:00", "08:00", "09:00"]
}

def selecionar_horario(especialidade):
    print(f"\nHorários disponíveis para {especialidade}:\n")

    horas = horarios_disponiveis.get(especialidade, [])

    if not horas:
        print("Nenhum horário disponível para este médico.")
        return None
    
    for i, h in enumerate(horas, start=1):
        print(f"{i} - {h}")

    while True:
        escolha = input("\nEscolha o número do horário desejado: ").strip()

        if escolha.isdigit():
                escolha = int(escolha)

        if 1 <= escolha <= len(horas):
            return horas[escolha - 1]
        
        print("Opção inválida! Tente novamente.")

def horario_ocupado(especialidade, data, hora):
    return any(
        ag["especialidade"] == especialidade and
        ag["data"] == data and
        ag["hora"] == hora
        for ag in agendamentos
    )
def selecionar_especialidade():
    print("\nSelecione a especialidade desejada:")
    for i, esp in enumerate(tipos_medicos, start=1):
        print(f"{i} - {esp}")
    print("0 - Digitar manualmente")

    while True:
        escolha = input("\nDigite o número da opção: ").strip()

        if escolha.isdigit():
            escolha = int(escolha)

            if 1 <= escolha <= len(tipos_medicos):
                return tipos_medicos[escolha - 1]

            elif escolha == 0:
                return input("Digite a especialidade desejada: ").strip()

        print("Opção inválida! Tente novamente.")


def verificar_agendamento(nome):
    return next(
        (a for a in agendamentos if a["paciente"].lower() == nome.lower()),
        None
    )

def adicionar_agendamento():
    global id_contador
    print("\nVamos marcar uma consulta! Estou aqui pra te ajudar \n")

    paciente = input("Qual o nome completo do paciente? ").strip()
    while not paciente:

        paciente = input("   Ops, não entendi o nome. Pode repetir? ").strip()

    ag_existente = verificar_agendamento(paciente)

    if ag_existente:
        print(f"""
 Atenção! Este paciente já tem um agendamento:

• {ag_existente['especialidade']}
• {ag_existente['data']} às {ag_existente['hora']}
""")
        continuar = input("Deseja marcar mesmo assim? (s/n): ").strip().lower()
        if continuar != "s":
            print("\nTudo bem! O agendamento não foi criado.\n")
            return

    print("\nAgora vamos escolher o tipo de médico:")
    especialidade = selecionar_especialidade()

    data = input("Qual a data desejada? (dd/mm): ").strip()
    while True:
        hora = selecionar_horario(especialidade)

        if horario_ocupado(especialidade, data, hora):
            print("\nEste horário já está ocupado para este médico neste dia!")
            print("Por favor, escolha outro horário.\n")
        else:
            break

    agendamento = {
        "id": id_contador,
        "paciente": paciente.title(),
        "especialidade": especialidade,
        "data": data,
        "hora": hora
    }

    agendamentos.append(agendamento)
    id_contador += 1

    print(f"""
Pronto, {paciente.split()[0]}! 
Sua consulta foi agendada com sucesso!

Resumo:
• Paciente: {paciente.title()}
• {especialidade}
• {data} às {hora}

Qualquer coisa é só me chamar que alteramos rapidinho!
""")


def listar_agendamentos():
    print("\nAqui está a agenda do dia/todos os agendamentos:\n")

    if not agendamentos:
        print("Ainda não temos nenhum agendamento... Vamos marcar o primeiro?\n")
        return

    for ag in agendamentos:
        print(f"""
╔═══════════════════════════════════
║  ID da consulta: #{ag['id']}
║
║  Paciente: {ag['paciente']}
║  {ag['especialidade']}
║  {ag['data']}  |   {ag['hora']}
╚═══════════════════════════════════
""")
    print(f"Total de agendamentos: {len(agendamentos)}\n")


def atualizar_agendamento():
    print("\nVamos alterar um agendamento!\n")

    if not agendamentos:
        print("Ainda não temos agendamentos para alterar.\n")
        return

    listar_agendamentos()

    try:
        id_sel = int(input("Digite o número (ID) do agendamento que deseja mudar: "))
    except:
        print("Ops! Digite apenas o número do ID.\n")
        return

    ag = next((a for a in agendamentos if a["id"] == id_sel), None)
    if not ag:
        print("Nenhum agendamento encontrado com esse ID.\n")
        return

    print(f"\nAlterando o agendamento do(a) {ag['paciente']} - {ag['data']} às {ag['hora']}\n")

    novo_paciente = input(f"Novo nome do paciente (ENTER para manter \"{ag['paciente']}\"): ").strip()

    print("\nNova especialidade:")
    print("Pressione ENTER para manter a atual.")
    print("Ou escolha uma nova:\n")
    print("Digite X para manter atual e pular lista.")
    print("\nSelecione a especialidade desejada:")
    for i, esp in enumerate(tipos_medicos, start=1):
        print(f"{i} - {esp}")

    escolha = input("Digite ENTER, X ou um número da lista: ").strip()

    if escolha == "":
        nova_especialidade = ag["especialidade"]
    elif escolha.lower() == "x":
        nova_especialidade = ag["especialidade"]
    elif escolha.isdigit() and 1 <= int(escolha) <= len(tipos_medicos):
        nova_especialidade = tipos_medicos[int(escolha) - 1]
    else:
        nova_especialidade = input("Digite a nova especialidade: ").strip()

    nova_data = input(f"Nova data (ENTER para manter \"{ag['data']}\"): ").strip()
    nova_hora = input(f"Novo horário (ENTER para manter \"{ag['hora']}\"): ").strip()

    if novo_paciente: ag["paciente"] = novo_paciente.title()
    if nova_especialidade: ag["especialidade"] = nova_especialidade
    if nova_data: ag["data"] = nova_data
    if nova_hora: ag["hora"] = nova_hora

    print(f"""
Tudo certo! Agendamento atualizado com sucesso!

Novo resumo:
{ag['paciente']}
{ag['especialidade']}
{ag['data']} às {ag['hora']}
""")


def remover_agendamento():
    print("\nVamos desmarcar sua consulta.\n")

    if not agendamentos:
        print("Nenhum agendamento para remover.\n")
        return

    listar_agendamentos()

    try:
        id_seletor = int(input("Digite o número (ID) da consulta que deseja cancelar: "))
    except:
        print("Ops! Digite apenas o número do ID.\n")
        return

    verificar_lista = next((a for a in agendamentos if a["id"] == id_seletor), None)

    if verificar_lista:
        agendamentos.remove(verificar_lista)
        print("Consulta removida com sucesso!\n")
    else:
        print("Nenhuma consulta encontrada com esse número.\n")


def menu():
    print("""

       COMPLEXO HOSPITALAR UPE
        Sistema de Teleagendamento

   Olá! Bem-vindo(a)! Como posso te ajudar hoje?
""")

    while True:
        print("""
┌──────────────────────────────────────┐
│  1 ➜  Marcar nova consulta           │
│  2 ➜  Ver todos os agendamentos      │
│  3 ➜  Alterar ou remarcar consulta   │
│  4 ➜  Desmarcar ou remover consulta  │
│  0 ➜  Sair                           │
└──────────────────────────────────────┘
""")

        opcao = input("Digite o número da opção desejada: ").strip()

        if opcao == "1":
            adicionar_agendamento()
        elif opcao == "2":
            listar_agendamentos()
        elif opcao == "3":
            atualizar_agendamento()
        elif opcao == "4":
            remover_agendamento()
        elif opcao == "0":
            print("\nObrigada por usar nosso sistema!\nAté a próxima!\n")
            break
        else:
            print("Opção inválida! Tente novamente.\n")


menu()