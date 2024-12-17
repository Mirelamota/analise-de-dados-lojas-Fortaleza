import pandas as pd

# Carregar os arquivos CSV
lojas = pd.read_csv(r"C:\Users\rafae\OneDrive\Documentos\analise de dados loja due\dados\ReadMe\lojas.csv")
produtos = pd.read_csv(r"C:\Users\rafae\OneDrive\Documentos\analise de dados loja due\dados\ReadMe\produtos.csv")
estoque = pd.read_csv(r"C:\Users\rafae\OneDrive\Documentos\analise de dados loja due\dados\ReadMe\estoques.csv")
vendas = pd.read_csv(r"C:\Users\rafae\OneDrive\Documentos\analise de dados loja due\dados\ReadMe\vendas.csv")

# Verificar as primeiras linhas de cada tabela
print("Lojas:")
print(lojas.head(), "\n")

print("Produtos:")
print(produtos.head(), "\n")

print("Estoque:")
print(estoque.head(), "\n")

print("Vendas:")
print(vendas.head(), "\n")


# Resumo estatístico das vendas
print(vendas.describe())

# Contar o número de registros únicos em cada tabela
print("Lojas únicas:", len(lojas))
print("Produtos únicos:", len(produtos))
print("Vendas registradas:", len(vendas))


# Unir vendas e produtos para análise detalhada
vendas_produtos = vendas.merge(produtos, on="ID_Produto").merge(lojas, on="ID_Loja")

# Visualizar as primeiras linhas da tabela combinada
print(vendas_produtos.head())


# Adicionar coluna de receita
vendas_produtos["Receita"] = vendas_produtos["Quantidade"] * vendas_produtos["Preco_Unitario"]

# Analisar impacto das promoções
impacto_promocoes = vendas_produtos.groupby("Promocao")["Receita"].sum()
print("Impacto das promoções:\n", impacto_promocoes)


import matplotlib.pyplot as plt
import seaborn as sns

# Gráfico de barras: Receita por loja
sns.barplot(data=vendas_produtos, x="Nome_Loja", y="Receita", ci=None)
plt.title("Receita por Loja")
plt.show()

# Gráfico de barras: Receita de produtos promocionais vs. não promocionais
sns.barplot(data=vendas_produtos, x="Promocao", y="Receita", ci=None)
plt.title("Impacto das Promoções na Receita")
plt.show()


import matplotlib.pyplot as plt
import seaborn as sns

# Gráfico de Receita por Loja
receita_loja = vendas_produtos.groupby("Nome_Loja")["Receita"].sum().reset_index()

sns.barplot(data=receita_loja, x="Nome_Loja", y="Receita")
plt.title("Receita por Loja")
plt.ylabel("Receita (R$)")
plt.xlabel("Loja")
plt.show()


import plotly.express as px

# Gráfico interativo de produtos mais vendidos
produtos_vendidos = vendas_produtos.groupby("Nome_Produto")["Quantidade"].sum().reset_index()

fig = px.bar(produtos_vendidos, x="Nome_Produto", y="Quantidade",
             title="Produtos Mais Vendidos", labels={"Quantidade": "Unidades Vendidas"})
fig.show()


#Quais categorias de produtos são mais vendidas em cada loja?

# Relacionar tabelas de vendas, produtos e lojas
vendas_produtos_lojas = vendas.merge(produtos, on="ID_Produto").merge(lojas, on="ID_Loja")

# Agrupar por loja e categoria
categorias_vendas = vendas_produtos_lojas.groupby(["Nome_Loja", "Categoria"])["Quantidade"].sum().reset_index()

# Visualizar categorias mais vendidas por loja
import seaborn as sns
import matplotlib.pyplot as plt

sns.barplot(data=categorias_vendas, x="Nome_Loja", y="Quantidade", hue="Categoria")
plt.title("Categorias mais vendidas por loja")
plt.ylabel("Quantidade vendida")
plt.xlabel("Loja")
plt.legend(title="Categoria")
plt.show()

#Quais lojas têm maior impacto positivo das promoções em suas vendas?

# Agrupando receita por loja e tipo de promoção
impacto_promocoes = vendas_produtos.groupby(["Nome_Loja", "Promocao"])["Receita"].sum().reset_index()

# Separando a receita de produtos promocionais e não promocionais
impacto_promocoes = impacto_promocoes.pivot(index="Nome_Loja", columns="Promocao", values="Receita").reset_index()
impacto_promocoes["Impacto (%)"] = (impacto_promocoes["Sim"] / (impacto_promocoes["Sim"] + impacto_promocoes["Não"])) * 100

print(impacto_promocoes)


#Quais produtos mais se beneficiaram de promoções?

# Filtrando produtos vendidos em promoção
produtos_promocao = vendas_produtos[vendas_produtos["Promocao"] == "Sim"]

# Calculando receita por produto
receita_promocao = produtos_promocao.groupby("Nome_Produto")["Receita"].sum().reset_index()
receita_promocao = receita_promocao.sort_values(by="Receita", ascending=False)

print(receita_promocao.head(10))  # Top 10 produtos em promoção


#Quem são os melhores vendedores (por loja e no geral)?

# Receita por vendedor e loja
desempenho_vendedores = vendas_produtos.groupby(["Nome_Loja", "Vendedor"])["Receita"].sum().reset_index()
desempenho_vendedores = desempenho_vendedores.sort_values(["Nome_Loja", "Receita"], ascending=[True, False])

print(desempenho_vendedores)

#Existe relação entre desempenho de vendedores e vendas de produtos em promoção?

# Receita por vendedor para produtos promocionais e não promocionais
relacao_promocoes = vendas_produtos.groupby(["Vendedor", "Promocao"])["Receita"].sum().reset_index()

# Separando em dois grupos para comparação
receita_vendedor_promocao = relacao_promocoes.pivot(index="Vendedor", columns="Promocao", values="Receita").reset_index()

print(receita_vendedor_promocao)

#Algum vendedor se destaca em categorias específicas de produtos?

# Receita por vendedor e categoria de produto
vendedor_categoria = vendas_produtos.groupby(["Vendedor", "Categoria"])["Receita"].sum().reset_index()
vendedor_categoria = vendedor_categoria.sort_values(["Vendedor", "Receita"], ascending=[True, False])

print(vendedor_categoria)


from fpdf import FPDF
import os

# Configurando o PDF
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font("Arial", size=12)

# Adicionando título e introdução
pdf.set_font("Arial", style='B', size=16)
pdf.cell(200, 10, txt="Relatório de Análise de Vendas - Rede de Lojas", ln=True, align='C')
pdf.ln(10)
pdf.set_font("Arial", size=12)
pdf.multi_cell(0, 10, txt="Este relatório apresenta os insights gerados a partir dos dados de vendas das lojas em Fortaleza. "
                           "As análises incluem categorias mais vendidas, impacto de promoções, e desempenho de vendedores.")

# Salvando gráficos como imagens e adicionando ao PDF
graficos_dir = "graficos"
os.makedirs(graficos_dir, exist_ok=True)

# Supondo que já tenha gerado os gráficos usando Matplotlib
grafico_arquivo = os.path.join(graficos_dir, "categorias_vendas.png")
plt.savefig(grafico_arquivo)
pdf.image(grafico_arquivo, x=10, y=60, w=190)

# Conclusão
pdf.add_page()
pdf.set_font("Arial", style='B', size=14)
pdf.cell(0, 10, txt="Conclusão", ln=True, align='L')
pdf.set_font("Arial", size=12)
pdf.multi_cell(0, 10, txt="Os dados mostram que promoções aumentaram significativamente as vendas em todas as lojas, "
                           "e alguns vendedores se destacaram em categorias específicas. A loja do Meireles obteve o maior impacto de promoções.")

# Salvar o PDF
pdf.output("relatorio_analise_vendas.pdf")
print("Relatório gerado com sucesso!")


