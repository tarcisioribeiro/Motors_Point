from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton

class CadastroCliente(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cadastro de Clientes")
        self.setGeometry(100, 100, 400, 300)

        # Layout principal
        layout = QVBoxLayout()

        # Campos de entrada
        self.nome_label = QLabel("Nome:")
        self.nome_input = QLineEdit()
        self.telefone_label = QLabel("Telefone:")
        self.telefone_input = QLineEdit()
        self.email_label = QLabel("E-mail:")
        self.email_input = QLineEdit()
        self.endereco_label = QLabel("Endereço:")
        self.endereco_input = QLineEdit()

        # Botões
        self.salvar_btn = QPushButton("Salvar")
        self.voltar_btn = QPushButton("Voltar")

        # Adicionando widgets ao layout
        layout.addWidget(self.nome_label)
        layout.addWidget(self.nome_input)
        layout.addWidget(self.telefone_label)
        layout.addWidget(self.telefone_input)
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)
        layout.addWidget(self.endereco_label)
        layout.addWidget(self.endereco_input)
        layout.addWidget(self.salvar_btn)
        layout.addWidget(self.voltar_btn)

        # Configuração do layout
        self.setLayout(layout)

# Inicializando o aplicativo
app = QApplication([])
janela = CadastroCliente()
janela.show()
app.exec_()
