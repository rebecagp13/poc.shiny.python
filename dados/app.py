# bibliotecas
from shiny import ui, render, App 
import pandas as pd
import plotnine as p9

# dados
dados = pd.read_csv("dados/dados.csv", converters ={"data":pd.to_datetime})

# interface do usuário
# tem que colocar algum conteúdo pra ela rodar
app_ui = ui.page_sidebar(
   
    #input
    # indicando o tipo de input q quer colocar
    ui.sidebar(
        ui.markdown(
            "**Entra em campo a seleção de dados macroeconômicos!**"
        ),
        ui.markdown(
            "Defina os times de países e indicadores, explore o jogo de visualizações e marque gol na análise de dados!"
        ),
        ui.input_selectize(
        id = "botao_variavel",
        label = "Selecionar variável:",
        choices = dados.variavel.unique().tolist(),
        selected = "PIB (%, cresc.anual)"
        ),
        ui.input_radio_buttons(
            id = "botao_grafico",
            label = "Selecionar tipo de gráfico:",
            choices = ["Coluna", "Linha", "Área"]
        )
        ),
    # output
    ui.layout_columns(
        ui.card(
            ui.input_selectize(
                id = "botao_pais1",
                label = "Selecione o 1º país:",
                choices = dados.pais.unique().tolist(),
                selected = "Uruguay"
                ),
            ui.output_plot("grafico_pais1")
            ),
        ui.card(
            ui.input_selectize(
                id = "botao_pais2",
                label = "Selecione o 2º país:",
                choices = dados.pais.unique().tolist(),
                selected = "Brazil"
                ),
            ui.output_plot("grafico_pais2")
            ),
    ),
    
    title = ui.h2(ui.strong("Macro Copa"))
)

# lógica de servidor
# tem que definir uma função pro servidor
# aqui vai escrever o código que gera o gráfico
# nome da função tem que ser o nome do id do grafico
# objeto externo tem que colocar @
def server(input, output, session):
    
    @render.plot
    def grafico_pais1():
        selecao_pais1 = input.botao_pais1()
        selecao_var = input.botao_variavel()
        tabela_pais1 = dados.query("pais == @selecao_pais1 and variavel == @selecao_var")
        grafico_pais1 = (
            p9.ggplot(tabela_pais1) +
            p9.aes(x = "data", y = "valor")
        )
        if input.botao_grafico() == "Coluna":
            return grafico_pais1 + p9.geom_col()
        elif input.botao_grafico() == "Linha":
            return grafico_pais1 + p9.geom_line()
        else:
            return grafico_pais1 + p9.geom_area()
        
    @render.plot
    def grafico_pais2():
        selecao_pais2 = input.botao_pais2()
        selecao_var = input.botao_variavel()
        tabela_pais2 = dados.query("pais == @selecao_pais2 and variavel == @selecao_var")
        grafico_pais2 = (
            p9.ggplot(tabela_pais2) +
            p9.aes(x = "data", y = "valor")
        )
        if input.botao_grafico() == "Coluna":
            return grafico_pais2 + p9.geom_col()
        elif input.botao_grafico() == "Linha":
            return grafico_pais2 + p9.geom_line()
        else:
            return grafico_pais2 + p9.geom_area()                    

# dashboard
app = App(app_ui, server)