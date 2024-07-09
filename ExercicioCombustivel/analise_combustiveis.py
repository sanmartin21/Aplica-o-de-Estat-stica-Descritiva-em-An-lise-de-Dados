import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Estruturação dos dados
data = {
    'CIDADE': ['A', 'A', 'A', 'B', 'B', 'B', 'C', 'C', 'C'],
    'COMBUSTIVEL': ['gasolina', 'etanol', 'diesel', 'gasolina', 'etanol', 'diesel', 'gasolina', 'etanol', 'diesel'],
    'POSTO1': [7.5, 4.25, 6.45, 9.05, 4.05, 6.5, 6.85, 3.99, 7.65],
    'POSTO2': [6.9, 4, 6.5, 7.3, 3.98, 6.55, 7.25, 3.98, 6.05],
    'POSTO3': [7.85, 3.8, 6.9, 6.75, 4.05, 4.49, 7.29, 4.15, 6.1],
    'POSTO4': [6.4, 4.95, 7.15, 7.05, 4.05, 6.89, 6.99, 4.05, 7.55],
    'POSTO5': [7.2, 4.8, 7.05, 7, 3.95, 7.1, 7.15, 3.99, 5.99]
}

df = pd.DataFrame(data)
df = df.melt(id_vars=['CIDADE', 'COMBUSTIVEL'], var_name='POSTO', value_name='PRECO')

# Cálculo das estatísticas descritivas
stats = df.groupby(['CIDADE', 'COMBUSTIVEL'])['PRECO'].agg(['mean', 'median', 'std'])
stats['CV'] = stats['std'] / stats['mean'] * 100  # Coeficiente de variação em porcentagem

# Visualização estruturada dos dados
print("Dados Estruturados:")
print(df)

print("\nEstatísticas Descritivas por Cidade e Combustível:")
print(stats)

# Análise da maior discrepância de preços por combustível
discrepancia = df.groupby('COMBUSTIVEL')['PRECO'].agg(['mean', 'median', 'std'])
discrepancia['CV'] = discrepancia['std'] / discrepancia['mean'] * 100

print("\nDiscrepância dos Preços por Combustível:")
print(discrepancia)

# Identificando o combustível com maior discrepância de preço
comb_maior_discrepancia = discrepancia['CV'].idxmax()
maior_discrepancia_valor = discrepancia['CV'].max()

print(f"\nO combustível com maior discrepância de preço é o {comb_maior_discrepancia}, com um coeficiente de variação de {maior_discrepancia_valor:.2f}%.")

# Discussão dos resultados
print("\nDiscussão dos Resultados:")
for cidade in stats.index.levels[0]:
    for combustivel in stats.loc[cidade].index:
        cv = stats.loc[(cidade, combustivel), 'CV']
        if cv < 5:
            print(f"Na cidade {cidade}, o combustível {combustivel} tem um CV de {cv:.2f}%, indicando conformidade nos preços.")
        else:
            print(f"Na cidade {cidade}, o combustível {combustivel} tem um CV de {cv:.2f}%, indicando competitividade nos preços.")


# Configurando o estilo dos gráficos
sns.set(style="whitegrid")

# Boxplot dos preços por cidade e combustível
plt.figure(figsize=(12, 8))
sns.boxplot(data=df, x='CIDADE', y='PRECO', hue='COMBUSTIVEL')
plt.title('Distribuição dos Preços dos Combustíveis por Cidade')
plt.xlabel('Cidade')
plt.ylabel('Preço')
plt.legend(title='Combustível')
plt.show()

# Gráfico de barras do coeficiente de variação por cidade e combustível
plt.figure(figsize=(12, 8))
stats.reset_index(inplace=True)
sns.barplot(data=stats, x='CIDADE', y='CV', hue='COMBUSTIVEL')
plt.title('Coeficiente de Variação dos Preços dos Combustíveis por Cidade')
plt.xlabel('Cidade')
plt.ylabel('Coeficiente de Variação (%)')
plt.legend(title='Combustível')
plt.show()

# Gráfico de barras do coeficiente de variação por combustível
plt.figure(figsize=(10, 6))
sns.barplot(data=discrepancia.reset_index(), x='COMBUSTIVEL', y='CV')
plt.title('Coeficiente de Variação dos Preços por Combustível')
plt.xlabel('Combustível')
plt.ylabel('Coeficiente de Variação (%)')
plt.show()