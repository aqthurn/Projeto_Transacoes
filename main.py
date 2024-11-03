from PyQt5 import uic, QtWidgets, QtCore
import sys
import datetime
from conexao import Conexao
from PyQt5.QtWidgets import QSizePolicy, QAction, QKeySequenceEdit
from conexao import Conexao, save_dataframe_as_pdf
import pandas as pd
from fpdf import FPDF
# Permite que a janela seja redimensionável

class MainWindow(QtWidgets.QMainWindow):
    

   class RelatorioPDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Relatório de Transações", 0, 1, "C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", 0, 0, "C")

def calcular_totais_transacoes():
    conexao = Conexao()
    # Obtendo transações
    transacoes = conexao.read_all()
    
    # Inicializando totais
    total = 0.0  # Este será o total líquido (entradas - saídas)

    # Filtrando e somando valores de entradas e saídas
    for transacao in transacoes:
        try:
            valor = float(transacao[1])  # Supondo que transacao[1] é o valor
            tipo = transacao[3].lower()   # Supondo que transacao[3] é o tipo

            if tipo == "entrada":
                total += valor  # Adiciona ao total
            elif tipo == "saida":
                total -= valor  # Subtrai do total
        except (ValueError, IndexError) as e:
            print(f"Erro ao processar a transação {transacao}: {e}")

    return total

def gerar_relatorio_pdf(caminho_pdf):
    # Calcula os totais
    total = calcular_totais_transacoes()
    
    # Cria o PDF
    pdf = MainWindow.RelatorioPDF()
    pdf.add_page()
    pdf.set_font("Arial", "", 12)
    
    # Adiciona as informações de total líquido
    pdf.cell(0, 10, f"Total Líquido: R$ {total:.2f}", 0, 1)
    
    # Adiciona uma tabela com as transações detalhadas
    pdf.cell(0, 10, "", 0, 1)
    pdf.cell(0, 10, "Detalhes das Transações", 0, 1)
    
    # Definindo cabeçalho da tabela
    pdf.set_font("Arial", "B", 10)
    pdf.cell(30, 10, "ID", 1)
    pdf.cell(50, 10, "Nome", 1)
    pdf.cell(30, 10, "Tipo", 1)
    pdf.cell(30, 10, "Valor", 1)
    pdf.cell(30, 10, "Data", 1)
    pdf.ln()

    # Preenchendo a tabela com as transações
    pdf.set_font("Arial", "", 10)
    conexao = Conexao()
    transacoes = conexao.read_all()
    for transacao in transacoes:
        pdf.cell(30, 10, str(transacao[0]), 1)  # ID
        pdf.cell(50, 10, transacao[2], 1)       # Nome
        pdf.cell(30, 10, transacao[3], 1)       # Tipo
        
        # Formata o valor diretamente, assumindo que é um float
        try:
            valor_formatado = f"R$ {float(transacao[1]):.2f}"
        except ValueError:  # Caso o valor não possa ser convertido
            valor_formatado = "Erro"

        pdf.cell(30, 10, valor_formatado, 1)  # Valor
        pdf.cell(30, 10, transacao[4], 1)       # Data
        pdf.ln()

    # Salva o PDF no caminho especificado
    pdf.output(caminho_pdf)
    print(f"Relatório salvo em {caminho_pdf}")



 
    def __init__(self):
        super().__init__()
        self.conexao = Conexao()
        self.conexao.create_table()
        self.initUI()


    def chamar_gerar_relatorio_pdf(self):
        tela_cadastro.pushButton_6.clicked.connect(self.chamar_gerar_relatorio_pdf)
        print("Botão pressionado: gerando relatório...")
        caminho_pdf = "C:\\Users\\Arthur\\OneDrive\\Documentos\\relatorio_transacoes.pdf"
        try:
            gerar_relatorio_pdf(caminho_pdf)
            print("Relatório gerado e salvo em:", caminho_pdf)
        except Exception as e:
            print(f"Erro ao gerar o relatório: {e}")
        tela_cadastro.pushButton_6.clicked.connect(self.chamar_gerar_relatorio_pdf) 
def abrir_janela_inserir():
    tela_inserir_matriculas.show()








def setup_button_for_search_dialog(tela_cadastro, dialog):
    # Conecta o botão de pesquisa ao diálogo
    tela_cadastro.pushButton_7.clicked.connect(lambda: show_search_dialog(dialog))

def show_search_dialog(dialog):
    # Exibe o diálogo de pesquisa
    dialog.exec_()

def limpa_tabela(valor):
    # Valor é o valor de linhas que terá a tabela
    conexao = Conexao()
    if valor == 1:
        tela_cadastro.tableWidget.setRowCount(1)
        tela_cadastro.tableWidget.setColumnCount(len(conexao.read_all()[0]))
        tela_cadastro.tableWidget.setHorizontalHeaderLabels(["id transação","Valor","nome da transação", "tipo", "data"])
        tela_cadastro.tableWidget.setRowCount(valor)
        tela_cadastro.tableWidget.setColumnCount(len(conexao.read_all()[0]))
        tela_cadastro.tableWidget.setHorizontalHeaderLabels(["id transação","Valor","nome da transação", "tipo", "data"])

def voltar():
    tela_inserir_matriculas.close()
    tela_cadastro.close()

def atualiza_tabela_principal():
    conexao = Conexao()
    # Recupera todas as transações do banco de dados
    rows = conexao.read_all()

    # Limpa a tabela se não houver dados disponíveis
    if not rows:
        tela_cadastro.tableWidget.setRowCount(0)
        tela_cadastro.tableWidget.setColumnCount(0)
        tela_cadastro.tableWidget.setHorizontalHeaderLabels([])  # Limpa os rótulos do cabeçalho
        return

    # Define o número de linhas e colunas
    tela_cadastro.tableWidget.setRowCount(len(rows))
    tela_cadastro.tableWidget.setColumnCount(len(rows[0]))  # O número de colunas da primeira linha

    # Define os nomes das colunas
    tela_cadastro.tableWidget.setHorizontalHeaderLabels(["ID Transação", "Valor", "Nome da Transação", "Tipo", "Data"])

    # Preenche a tabela com os dados das transações
    for i, row in enumerate(rows):  # Para cada linha
        for j, value in enumerate(row):  # Para cada coluna
            item = QtWidgets.QTableWidgetItem(str(value))
            tela_cadastro.tableWidget.setItem(i, j, item)

def fechar_janela_inserir():
    atualiza_tabela_principal()
    tela_inserir_matriculas.lineEdit.setText('')
    tela_inserir_matriculas.lineEdit_2.setText('')
    tela_inserir_matriculas.close()

def inserir_dados():
    # Definindo tipos válidos de transação
    numeros = '123456789'
    caracteres_especiais = "!@#$%¨&*()-=+[]"

    try:
        # Resgatando o valor dos campos da janela inserir
        nome_transacao = tela_inserir_matriculas.lineEdit.text()  # Campo para o nome da transação
        valor = tela_inserir_matriculas.lineEdit_2.text()  # Campo para o valor
        tipo_transacao = tela_inserir_matriculas.comboBox.currentText()  # QComboBox para o tipo
        data_transacao = tela_inserir_matriculas.dateTimeEdit.dateTime().toString("yyyy-MM-dd")  # QDateTimeEdit para data

        # Verificando se os campos obrigatórios estão preenchidos
        if not nome_transacao or not valor or not tipo_transacao:
            QtWidgets.QMessageBox.about(tela_inserir_matriculas, 'Erro', 'Por favor, preencha todos os campos antes de inserir')
            return

        # Convertendo valor para float
        try:
            valor = float(valor)
        except ValueError:
            QtWidgets.QMessageBox.about(tela_inserir_matriculas, 'Erro', 'Insira apenas números no campo Valor')
            return

        # Validando o nome para impedir números e caracteres especiais
        for char in nome_transacao:
            if char in numeros or char in caracteres_especiais:
                QtWidgets.QMessageBox.about(tela_inserir_matriculas, 'Erro', 'Por favor, não insira números ou caracteres especiais no campo "nome da transação"')
                return

        # Inserir no banco de dados com o campo data (simulação)
        conexao = Conexao()
        resposta = conexao.insert_transacao(valor, nome_transacao, tipo_transacao, data_transacao)
        atualiza_tabela_principal()
        QtWidgets.QMessageBox.about(tela_inserir_matriculas, 'Sucesso', 'Transação inserida com sucesso')

    except Exception as e:
        QtWidgets.QMessageBox.about(tela_inserir_matriculas, 'Erro', f'Ocorreu um erro: {e}')
    
    return
def export_to_pdf(self):
    transacoes = self.conexao.read_all()
    df = pd.DataFrame(transacoes, columns=["ID", "Valor", "Nome", "Tipo", "Data"])
    save_dataframe_as_pdf(df, 'C:\\Users\\Arthur\\OneDrive\\Documentos\\totais_semanal')


def abrir_janela_atualizar():
    tela_atualizar.show()

def fechar_janela_atualizar():
    atualiza_tabela_principal()
    tela_atualizar.lineEdit.setText('')
    tela_atualizar.lineEdit_2.setText('')
    #tela_atualizar.lineEdit_4.setText('')
    tela_atualizar.close()

def atualizar_dados():
    # Caracteres inválidos para nome da transação
    numeros = '1234567890'
    caracteres_especiais = "!@#$%¨&*()-=+[]"
    
    try:
        # Resgatando valores dos campos
        id_transacao = tela_atualizar.lineEdit_id.text().strip()  # Obtém o ID da transação
        nome_transacao = tela_atualizar.lineEdit.text().strip()
        valor = tela_atualizar.lineEdit_2.text().strip()
        tipo_transacao = tela_atualizar.comboBox.currentText()  # Captura o tipo de transação selecionado no comboBox
        data = tela_atualizar.dateTime().toString("yyyy-MM-dd")  # Obtém a data da transação

        # Verifica se o campo ID da transação não está vazio
        if not id_transacao.isdigit():
            QtWidgets.QMessageBox.about(tela_atualizar, 'Erro', 'ID da transação inválido.')
            return
        id_transacao = int(id_transacao)

        # Validação do campo "Valor"
        try:
            valor = float(valor)
            if valor < 0:
                raise ValueError("O valor deve ser positivo.")
        except ValueError:
            QtWidgets.QMessageBox.about(tela_atualizar, 'Erro', 'Por favor, insira um valor numérico positivo.')
            return

        # Validação do campo "Nome da Transação"
        if any(char in numeros + caracteres_especiais for char in nome_transacao):
            QtWidgets.QMessageBox.about(tela_atualizar, 'Erro', 'O nome da transação não deve conter números ou caracteres especiais.')
            return

        # Atualização no banco de dados
        conexao = Conexao()
        conexao.update_transacao(id_transacao, nome_transacao, data, valor, tipo_transacao)

        atualiza_tabela_principal()
        QtWidgets.QMessageBox.about(tela_atualizar, 'Conexão banco de dados', 'Atualização feita com sucesso')

    except Exception as e:
        QtWidgets.QMessageBox.about(tela_atualizar, 'Erro', f'Ocorreu um erro: {e}')

    return
def abrir_janela_excluir():
    tela_excluir.show()

def fechar_janela_excluir():
    atualiza_tabela_principal()
    tela_excluir.lineEdit.setText('')
    tela_excluir.close()

def excluir_dados():
    try:
        id_transacao = tela_excluir.lineEdit.text()
        id_transacao = int(id_transacao)
        if id_transacao < 1 or id_transacao > 300:
            QtWidgets.QMessageBox.about(tela_excluir, 'Erro', 'Por favor insira um id de transacão válido')
            return
        conexao = Conexao()
        response = conexao.read_one(id_transacao)
        if response == None:
            QtWidgets.QMessageBox.about(tela_excluir, 'Erro', 'Falha ao excluir, id inexistente na tabela')
            return

    except Exception:
        QtWidgets.QMessageBox.about(tela_excluir, 'Erro', 'Insira apenas números')
        return

    # Parte da inserção no banco de dados
    conexao = Conexao()
    resposta = conexao.delete_transacao(id_transacao)
    atualiza_tabela_principal()
    QtWidgets.QMessageBox.about(tela_excluir, 'Conexão banco de dados', 'Registro excluido com sucesso')
    
    return  

def setup_button_for_date_search(tela_cadastro):
    # Configura o botão para abrir o calendário
    tela_cadastro.buttonSelectDate.clicked.connect(lambda: open_calendar(tela_cadastro))

def open_calendar(tela_cadastro):
    # Cria e configura o calendário
    calendar = QtWidgets.QCalendarWidget()
    calendar.setWindowTitle("Selecionar Data")
    calendar.setGridVisible(True)
    
    # Conecta a seleção da data à função de pesquisa e fecha o calendário
    calendar.clicked.connect(lambda date: select_date_and_search(calendar, date, tela_cadastro))
    
    # Exibe o calendário
    calendar.show()

def select_date_and_search(calendar, date, tela_cadastro):
    # Fecha o calendário após a seleção da data
    calendar.close()
    
    # Formata a data selecionada
    data_pesquisa = date.toString("yyyy-MM-dd")
    print(f"Data de pesquisa: {data_pesquisa}")

    # Chama a função de pesquisa com a data selecionada
    pesquisar_por_data(data_pesquisa, tela_cadastro)

def pesquisar_por_data(data_pesquisa, tela_cadastro):
    try:
        # Tenta converter a data para verificar o formato
        data = datetime.datetime.strptime(data_pesquisa, '%Y-%m-%d')
    except ValueError:
        QtWidgets.QMessageBox.about(tela_cadastro, 'Alerta', 'Por favor, selecione uma data válida no formato YYYY-MM-DD')
        return

    conexao = Conexao()
    # Verifica o nível de granularidade da pesquisa
    if data.day == 1 and data.month == 1:  # Apenas ano
        rows = conexao.read_data_por_ano(data.year)
    elif data.day == 1:  # Apenas mês
        rows = conexao.read_data_por_mes(data.year, data.month)
    else:  # Dia específico
        rows = conexao.read_data_por_dia(data_pesquisa)

    # Verifica se há resultados
    if not rows:
        QtWidgets.QMessageBox.about(tela_cadastro, 'Alerta', 'Valor não encontrado na tabela')
        return

    # Limpa a tabela e exibe os resultados
    limpa_tabela(len(rows))
    for i in range(len(rows)):
        for j in range(len(rows[0])):
            item = QtWidgets.QTableWidgetItem(f"{rows[i][j]}")
            tela_cadastro.tableWidget.setItem(i, j, item)

def alternar_tela_cheia():
    if tela_cadastro.isFullScreen():
        tela_cadastro.showNormal()  # Sai do modo tela cheia
    else:
        tela_cadastro.showFullScreen()  # Entra no modo tela cheia

def obter_nome_transacao(lineEdit):
    return lineEdit.text().strip()  # Retorna o texto do QLineEdit, removendo espaços extras

def pesquisar_por_nome_e_exibir(tela_cadastro, valor_pesquisa):
    transacao = valor_pesquisa.lower()  # Converte o texto para minúsculas
    print(f"Buscando por: {transacao}")  # Para depuração
    encontrou_correspondencia = False  # Para verificar se alguma linha foi exibida

    for row in range(tela_cadastro.tableWidget.rowCount()):
        item = tela_cadastro.tableWidget.item(row, 2)  # Supondo que o nome está na coluna 2
        
        if item:  # Verifica se o item não é None
            print(f"Linha {row}: {item.text()}")  # Imprime o texto do item
            if transacao in item.text().lower():  # Verifica se a transação está no texto
                tela_cadastro.tableWidget.showRow(row)  # Exibe a linha que corresponde
                encontrou_correspondencia = True  # Marque que encontramos uma correspondência
            else:
                tela_cadastro.tableWidget.hideRow(row)  # Oculta a linha que não corresponde
        else:
            tela_cadastro.tableWidget.hideRow(row)  # Oculta linhas onde não há item

    if not encontrou_correspondencia:
        print("Nenhuma correspondência encontrada.")  # Mensagem se nada foi encontrado

def mostrar_dialog_pesquisa(tela_cadastro):
    dialog_pesquisa = QtWidgets.QDialog()
    dialog_pesquisa.setWindowTitle("Pesquisar Transação")  # Define o título do diálogo
    setup_search_button_with_dialog(tela_cadastro, dialog_pesquisa)
    dialog_pesquisa.exec_()  # Exibe o diálogo como um modal

def setup_search_button_with_dialog(tela_cadastro, dialog_pesquisa):
    layout = QtWidgets.QVBoxLayout()

    lineEdit_pesquisa = QtWidgets.QLineEdit()
    lineEdit_pesquisa.setPlaceholderText("Digite o nome da pesquisa")
    layout.addWidget(lineEdit_pesquisa)

    botao_confirmar_pesquisa = QtWidgets.QPushButton("Pesquisar")
    layout.addWidget(botao_confirmar_pesquisa)

    dialog_pesquisa.setLayout(layout)

    # Conectar o botão de pesquisa para realizar a ação
    botao_confirmar_pesquisa.clicked.connect(lambda: realizar_pesquisa_dialog(lineEdit_pesquisa, dialog_pesquisa, tela_cadastro))

def realizar_pesquisa_dialog(lineEdit, dialog, tela_cadastro):
    valor_pesquisa = obter_nome_transacao(lineEdit)  # Obtém o nome da transação
    print(f"Nome da transação a ser pesquisado: {valor_pesquisa}")  # Para depuração

    # Chame a função de pesquisa passando o valor da pesquisa
    pesquisar_por_nome_e_exibir(tela_cadastro, valor_pesquisa)

    dialog.close()  # Fecha o diálogo após a pesquisa
def att_tabela_cadastro():
    tela_cadastro.tableWidget.clearContents()  # Limpa a tabela

    # Create a connection to the database
    conexao = Conexao()

    # Fetch all data from the database
    data = conexao.read_all()

    # Update the table with the fetched data
    tela_cadastro.tableWidget.setRowCount(len(data))
    tela_cadastro.tableWidget.setColumnCount(len(data[0]) if data else 0)

    for row_index, row_data in enumerate(data):
        for col_index, col_data in enumerate(row_data):
            tela_cadastro.tableWidget.setItem(row_index, col_index, QtWidgets.QTableWidgetItem(str(col_data)))

    # Close the database connection
    conexao.close()

# Connect the push button to the function
    tela_cadastro.pushButton_8.clicked.connect(att_tabela_cadastro)








# The rest of your code


app = QtWidgets.QApplication(sys.argv)
tela_cadastro = uic.loadUi('tela_cadastro.ui')
tela_inserir_matriculas = uic.loadUi('inserir_dados.ui')
tela_atualizar = uic.loadUi('atualizar_dados.ui')
tela_excluir = uic.loadUi('tela_excluir.ui')
setup_button_for_date_search(tela_cadastro)
dialog_pesquisa = QtWidgets.QDialog()
setup_search_button_with_dialog(tela_cadastro, dialog_pesquisa)

# Conectando os botoes da janela principal as funções da janela principal
tela_cadastro.pushButton_2.clicked.connect(abrir_janela_inserir)
tela_cadastro.pushButton_7.clicked.connect(lambda: dialog_pesquisa.exec_())
tela_cadastro.pushButton_3.clicked.connect(abrir_janela_atualizar)
tela_cadastro.pushButton_5.clicked.connect(voltar)
tela_cadastro.pushButton_4.clicked.connect(abrir_janela_excluir)
tela_cadastro.pushButton_8.clicked.connect(att_tabela_cadastro)
tela_cadastro.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

# Conectando os botões da janela de inserir as funções da janela de inserir
tela_inserir_matriculas.pushButton_2.clicked.connect(fechar_janela_inserir)
tela_inserir_matriculas.pushButton.clicked.connect(inserir_dados)

# Conectando os botões da jenala atualizar as funções da janela atualizar
tela_atualizar.pushButton_2.clicked.connect(fechar_janela_atualizar)
tela_atualizar.pushButton.clicked.connect(atualizar_dados)

# Conectando os botões da janela excluir as funções da janela excluir
tela_excluir.pushButton_2.clicked.connect(fechar_janela_excluir)
tela_excluir.pushButton.clicked.connect(excluir_dados)

atualiza_tabela_principal()

tela_cadastro.show()
sys.exit(app.exec_())