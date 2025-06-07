import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import re

# Crear carpeta para guardar gráficos dentro de la carpeta web
os.makedirs("../web/graficos", exist_ok=True)

# Cargar dataset desde la carpeta data
df = pd.read_csv('../data/Top_Selling_Games.csv')
df = df.dropna()  # Limpiar datos

# Top 10 juegos más vendidos
top_10 = df.sort_values(by='Units Sold (millions)', ascending=False).head(10)
plt.figure(figsize=(10,6))
sns.barplot(x='Units Sold (millions)', y='Game Title', data=top_10, palette='mako')
plt.title("Top 10 Juegos Más Vendidos")
plt.tight_layout()
plt.savefig("../web/graficos/top_10_juegos.png")

# Ventas por plataforma
ventas_por_plataforma = df.groupby("Platform(s)")["Units Sold (millions)"].sum().sort_values(ascending=False)
plt.figure(figsize=(12,6))
ventas_por_plataforma.plot(kind='bar', color='coral')
plt.ylabel("Millones de Copias")
plt.title("Ventas por Plataforma")
plt.tight_layout()
plt.savefig("../web/graficos/ventas_por_plataforma.png")

# Correlaciones
plt.figure(figsize=(8,6))
sns.heatmap(df[["Units Sold (millions)"]].corr(), annot=True, cmap='coolwarm')
plt.title("Correlaciones entre variables")
plt.tight_layout()
plt.savefig("../web/graficos/correlaciones.png")

# Ventas por género (si existe la columna)
if "Genre" in df.columns:
    ventas_por_genero = df.groupby("Genre")["Units Sold (millions)"].sum().sort_values(ascending=False)
    plt.figure(figsize=(12,6))
    ventas_por_genero.plot(kind='bar', color='skyblue')
    plt.ylabel("Millones de Copias")
    plt.title("Ventas por Género")
    plt.tight_layout()
    plt.savefig("../web/graficos/ventas_por_genero.png")

# Ventas por década (si existe la fecha de lanzamiento)
if "Initial release date" in df.columns:
    # Limpiar anotaciones entre corchetes como [c]
    df['Initial release date'] = df['Initial release date'].apply(lambda x: re.sub(r'\[.*?\]', '', str(x)).strip())
    df['Año'] = pd.to_datetime(df['Initial release date'], errors='coerce').dt.year
    df = df.dropna(subset=['Año'])
    df['Década'] = (df['Año'] // 10 * 10).astype(int).astype(str) + 's'
    ventas_por_decada = df.groupby('Década')['Units Sold (millions)'].sum().sort_index()
    plt.figure(figsize=(10,6))
    ventas_por_decada.plot(kind='bar', color='mediumseagreen')
    plt.ylabel("Millones de Copias")
    plt.title("Ventas por Década")
    plt.tight_layout()
    plt.savefig("../web/graficos/ventas_por_decada.png")
