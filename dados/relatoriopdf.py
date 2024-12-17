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
pdf.multi_cell(0, 10, txt="Este relatório apresenta os insights gerados a partir dos dados de vendas das três lojas em Fortaleza. "
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
