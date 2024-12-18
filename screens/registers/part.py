from dictionary.vars import today, to_remove_list
from data.cache.session_state import logged_user
from functions.query_executor import QueryExecutor
from functions.get_actual_time import GetActualTime
from time import sleep
import streamlit as st


class Parts:

    def __init__(self):

        query_executor = QueryExecutor()
        time = GetActualTime()

        def main_menu():

            col1, col2, col3 = st.columns(3)

            with col1:
                st.subheader(body=":computer: Entrada de Dados")
                with st.expander(label="Dados", expanded=True):
                    part_description = st.text_input(label="Descrição", placeholder="Descrição", max_chars=100)
                    value = st.number_input(label="Preço", min_value=0.01, step=0.01)
                    confirm_part_data = st.checkbox(label="Confirmar dados")

                register_new_part = st.button(label=":floppy_disk: Cadastrar nova peça")

            if confirm_part_data and register_new_part:
                
                with col2:
                    with st.spinner(text="Aguarde..."):
                        sleep(2.5)

                    st.subheader(body=":white_check_mark: Validação de Dados")

                    with st.expander(label="Dados", expanded=True   ):

                        if part_description != "":
                            st.success(body="Dados válidos.")

                            new_part_query = '''INSERT INTO pecas (descricao, preco) VALUES (%s, %s);'''
                            part_values = (part_description, value)
                            query_executor.insert_query(new_part_query, part_values, "Peça cadastrada com sucesso!", "Erro ao cadastrar peça:")

                            actual_time = time.get_actual_time()

                            log_query = '''INSERT INTO logs_atividades (data_log, horario_log, usuario_log, tipo_log, conteudo_log) VALUES (%s, %s, %s, %s, %s);'''
                            log_values = (today, actual_time, logged_user, "Cadastro", "O usuário cadastrou a peça {}.".format(part_description))
                            query_executor.insert_query(log_query, log_values, "Log gravado com sucesso!", "Erro ao gravar log:")

        self.main_menu = main_menu