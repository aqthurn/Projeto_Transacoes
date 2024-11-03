import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
from pandas.plotting import table

class Conexao:
    def __init__(self):
        self.connection = self.conectar()
        self.cursor = self.connection.cursor()

    def conectar(self):
        try:
            connection = sqlite3.connect("hugobanco.db")
            return connection
        except sqlite3.Error as e:
            print(f'Erro ao conectar ao banco de dados: {e}')
            return None

    def create_table(self):
        try:
            sql = '''
                    CREATE TABLE IF NOT EXISTS transacoes(
                        id_transacao INTEGER PRIMARY KEY,
                        valor FLOAT,
                        nome_transacao VARCHAR(300),
                        tipo_transacao VARCHAR(100),
                        data VARCHAR(12)
                    )'''
            self.cursor.execute(sql)
            self.connection.commit()
            print('Tabela criada com sucesso')
        except sqlite3.Error as e:
            print(f'Erro ao criar a tabela: {e}')

    def insert_transacao(self, valor, nome, tipo, data):
        try:
            sql = '''
                    INSERT INTO transacoes(valor, nome_transacao, tipo_transacao, data)
                    VALUES(?, ?, ?, ?)
                  '''
            self.cursor.execute(sql, (valor, nome, tipo, data))
            self.connection.commit()
            print('Transação inserida com sucesso')
        except sqlite3.Error as e:
            print(f'Erro ao inserir transação: {e}')

    def update_transacao(self, id_transacao, nome, valor, tipo, data):
        try:
            sql = '''
                UPDATE transacoes
                SET nome_transacao = ?, valor = ?, tipo_transacao = ?, data = ?
                WHERE id_transacao = ?
            '''
            self.cursor.execute(sql, (nome, valor, tipo, data, id_transacao))
            self.connection.commit()
            print('Transação atualizada com sucesso')
        except sqlite3.Error as e:
            print(f'Erro ao atualizar transação: {e}')   
            
    def delete_transacao(self, id_transacao):
        try:
            sql = '''
                    DELETE FROM transacoes
                    WHERE id_transacao = ?
                  '''
            self.cursor.execute(sql, (id_transacao,))
            self.connection.commit()
            print('Transação deletada com sucesso')
        except sqlite3.Error as e:
            print(f'Erro ao deletar transação: {e}')

    def read_all(self):
        try:
            sql = '''SELECT * FROM transacoes'''
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f'Erro ao ler todas as transações: {e}')
            return []

    def read_one(self, id_transacao):
        try:
            sql = '''SELECT * FROM transacoes WHERE id_transacao = ?'''
            self.cursor.execute(sql, (id_transacao,))
            row = self.cursor.fetchone()
            return row
        except sqlite3.Error as e:
            print(f'Erro ao ler transação: {e}')
            return None

    def read_data_por_ano(self, ano):
        try:
            query = "SELECT * FROM transacoes WHERE strftime('%Y', data) = ?"
            self.cursor.execute(query, (str(ano),))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f'Erro ao ler transações por ano: {e}')
            return []

    def read_data_por_mes(self, ano, mes):
        try:
            query = "SELECT * FROM transacoes WHERE strftime('%Y', data) = ? AND strftime('%m', data) = ?"
            self.cursor.execute(query, (str(ano), str(mes).zfill(2)))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f'Erro ao ler transações por mês: {e}')
            return []

    def read_data_por_dia(self, data_pesquisa):
        try:
            query = "SELECT * FROM transacoes WHERE data = ?"
            self.cursor.execute(query, (data_pesquisa,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f'Erro ao ler transações por dia: {e}')
            return []

    def close(self):
        if self.connection:
            self.connection.close()
            print('Conexão fechada com sucesso')
        else:
            print('Nenhuma conexão ativa para fechar')

    def calcular_total_por_periodo(self, periodo):
        try:
            query = f"""
                SELECT strftime('{periodo}', data) AS period, 
                       id_transacao, valor, nome_transacao, tipo_transacao, data,
                       SUM(CASE WHEN tipo_transacao = 'entrada' THEN valor ELSE -valor END) AS total
                FROM transacoes
                GROUP BY period
            """
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            return results
        except sqlite3.Error as e:
            print(f'Erro ao calcular total por período: {e}')
            return []

    def calcular_total_semanal(self):
        return self.calcular_total_por_periodo('%Y-%W')

    def calcular_total_mensal(self):
        return self.calcular_total_por_periodo('%Y-%m')

    def calcular_total_anual(self):
        return self.calcular_total_por_periodo('%Y')

def save_dataframe_as_pdf(df, filename):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    fig, ax = plt.subplots(figsize=(12, 6))  # Adjust size for more columns
    ax.axis('tight')
    ax.axis('off')
    table(ax, df, loc='center', cellLoc='center', colWidths=[0.1]*len(df.columns))  # where df is your data frame

    # Save the figure
    plt.savefig(f"{filename}.png")

    # Create PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.image(f"{filename}.png", x=10, y=10, w=190)
    pdf.output(f"{filename}.pdf", "F")

if __name__ == '__main__':
    conexao = Conexao()
    conexao.create_table()
    
    # Inserir transações de entrada e saída
    conexao.insert_transacao(5000, 'Entrada 1', 'entrada', '2024-01-01')
    conexao.insert_transacao(5000, 'Entrada 2', 'entrada', '2024-05-01')
    conexao.insert_transacao(5000, 'Entrada 3', 'entrada', '2024-09-01')
    conexao.insert_transacao(2000, 'Saída 1', 'saida', '2024-03-01')
    conexao.insert_transacao(3000, 'Saída 2', 'saida', '2024-07-01')
    
    # Calcular e imprimir os totais
    transacoes_semanal = conexao.calcular_total_semanal()
    transacoes_mensal = conexao.calcular_total_mensal()
    transacoes_anual = conexao.calcular_total_anual()
    
    # Criar tabelas para exibir os resultados
    df_semanal = pd.DataFrame(transacoes_semanal, columns=['Semana', 'ID Transacao', 'Valor', 'Nome Transacao', 'Tipo Transacao', 'Data', 'Total'])
    df_mensal = pd.DataFrame(transacoes_mensal, columns=['Mes', 'ID Transacao', 'Valor', 'Nome Transacao', 'Tipo Transacao', 'Data', 'Total'])
    df_anual = pd.DataFrame(transacoes_anual, columns=['Ano', 'ID Transacao', 'Valor', 'Nome Transacao', 'Tipo Transacao', 'Data', 'Total'])
    
    print('Totais Semanais:')
    print(df_semanal)
    print('\nTotais Mensais:')
    print(df_mensal)
    print('\nTotais Anuais:')
    print(df_anual)
    
    # Save DataFrames as PDF
    save_dataframe_as_pdf(df_semanal, 'C:\\Users\\Arthur\\OneDrive\\Documentos\\totais_semanal')
    save_dataframe_as_pdf(df_mensal, 'C:\\Users\\Arthur\\OneDrive\\Documentos\\totais_mensal')
    save_dataframe_as_pdf(df_anual, 'C:\\Users\\Arthur\\OneDrive\\Documentos\\totais_anual')

    
    conexao.close()