import flet as ft
import json
import os

ARQUIVO_DADOS = "tarefas.json"


def carregar_tarefas():
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def salvar_tarefas(tarefas):
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(tarefas, f, ensure_ascii=False, indent=2)


def main(page: ft.Page):
    page.title = "Lista de Tarefas"
    page.window.width = 500
    page.window.height = 700
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 20

    tarefas = carregar_tarefas()

    lista_view = ft.ListView(
        expand=True,
        spacing=10
    )

    campo_titulo = ft.TextField(
        label="Título da tarefa",
        expand=True
    )

    campo_prioridade = ft.Dropdown(
        label="Prioridade",
        width=150,
        options=[
            ft.DropdownOption(key="Baixa", text="Baixa"),
            ft.DropdownOption(key="Média", text="Média"),
            ft.DropdownOption(key="Alta", text="Alta"),
        ],
        value="Média",
    )

    # --------------------------------
    # EDITAR TAREFA
    # --------------------------------
    def editar_tarefa(indice):
        tarefa = tarefas[indice]

        campo_editar_titulo = ft.TextField(
            label="Título da tarefa",
            value=tarefa["titulo"]
        )

        campo_editar_prioridade = ft.Dropdown(
            label="Prioridade",
            options=[
                ft.DropdownOption(key="Baixa", text="Baixa"),
                ft.DropdownOption(key="Média", text="Média"),
                ft.DropdownOption(key="Alta", text="Alta"),
            ],
            value=tarefa["prioridade"],
        )

        def salvar_edicao(e):
            novo_titulo = (
                campo_editar_titulo.value.strip()
                if campo_editar_titulo.value
                else ""
            )

            if novo_titulo == "":
                campo_editar_titulo.error_text = "Digite um título"
                page.update()
                return

            tarefas[indice]["titulo"] = novo_titulo
            tarefas[indice]["prioridade"] = campo_editar_prioridade.value

            salvar_tarefas(tarefas)

            page.pop_dialog()

            atualizar_lista()

        dialogo = ft.AlertDialog(
            modal=True,
            title=ft.Text("Editar tarefa"),
            content=ft.Column(
                controls=[
                    campo_editar_titulo,
                    campo_editar_prioridade,
                ],
                tight=True,
            ),
            actions=[
                ft.Button(
                    content="Cancelar",
                    on_click=lambda e: page.pop_dialog(),
                ),
                ft.Button(
                    content="Salvar",
                    on_click=salvar_edicao,
                ),
            ],
        )

        page.show_dialog(dialogo)

    # --------------------------------
    # ATUALIZAR LISTA
    # --------------------------------
    def atualizar_lista():
        lista_view.controls.clear()

        for indice, tarefa in enumerate(tarefas):

            def marcar_concluida(e, i=indice):
                tarefas[i]["concluida"] = e.control.value
                salvar_tarefas(tarefas)
                atualizar_lista()

            def excluir_tarefa(e, i=indice):
                tarefas.pop(i)
                salvar_tarefas(tarefas)
                atualizar_lista()

            checkbox = ft.Checkbox(
                label=tarefa["titulo"],
                value=tarefa["concluida"],
                on_change=marcar_concluida
            )

            prioridade = ft.Text(
                f'Prioridade: {tarefa["prioridade"]}'
            )

            botao_editar = ft.Button(
                content="Editar",
                on_click=lambda e, i=indice: editar_tarefa(i)
            )

            botao_excluir = ft.Button(
                content="Excluir",
                on_click=excluir_tarefa
            )

            linha = ft.Row(
                controls=[
                    checkbox,
                    prioridade,
                    botao_editar,
                    botao_excluir,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )

            lista_view.controls.append(linha)

        page.update()

    # --------------------------------
    # ADICIONAR TAREFA
    # --------------------------------
    def adicionar_tarefa(e):
        titulo = (
            campo_titulo.value.strip()
            if campo_titulo.value
            else ""
        )

        if titulo == "":
            campo_titulo.error_text = "Digite um título"
            page.update()
            return

        campo_titulo.error_text = None

        nova_tarefa = {
            "titulo": titulo,
            "prioridade": campo_prioridade.value,
            "concluida": False,
        }

        tarefas.append(nova_tarefa)

        salvar_tarefas(tarefas)

        campo_titulo.value = ""
        campo_prioridade.value = "Média"

        atualizar_lista()

    # --------------------------------
    # BOTÃO ADICIONAR
    # --------------------------------
    botao_adicionar = ft.Button(
        content="Adicionar tarefa",
        on_click=adicionar_tarefa
    )

    # --------------------------------
    # TELA
    # --------------------------------
    page.add(
        ft.Text(
            "Minha Lista de Tarefas",
            size=24,
            weight=ft.FontWeight.BOLD
        ),

        ft.Row(
            controls=[
                campo_titulo,
                campo_prioridade
            ]
        ),

        botao_adicionar,

        ft.Divider(),

        lista_view,
    )

    atualizar_lista()


ft.run(main)