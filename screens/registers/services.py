from dictionary.vars import today, to_remove_list
from data.cache.session_state import logged_user
from functions.query_executor import QueryExecutor
from functions.get_actual_time import GetActualTime
from time import sleep
import streamlit as st


class Services:

    def __init__(self):

        query_executor = QueryExecutor()
        time = GetActualTime()

        def main_menu():

            col1, col2, col3 = st.columns(3)

            with col1:
                st.subheader(body=":computer: Entrada de Dados")
                with st.expander(label="Dados", expanded=True):
                    services_description = st.text_input(label="Descrição", placeholder="Descrição", max_chars=100)
                    value = st.number_input(label="Preço", min_value=0.01, step=0.01)
                    confirm_service_data = st.checkbox(label="Confirmar dados")

                register_new_part = st.button(label=":floppy_disk: Cadastrar novo serviço")

            if confirm_service_data and register_new_part:
                
                with col2:
                    with st.spinner(text="Aguarde..."):
                        sleep(2.5)

                    st.subheader(body=":white_check_mark: Validação de Dados")

                    with st.expander(label="Dados", expanded=True):

                        if services_description != "":
                            st.success(body="Dados válidos.")

                            new_service_query = '''INSERT INTO servicos (descricao, preco) VALUES (%s, %s);'''
                            service_values = (services_description, value)
                            query_executor.insert_query(new_service_query, service_values, "Serviço cadastrado com sucesso!", "Erro ao cadastrar serviço:")

                            actual_time = time.get_actual_time()

                            log_query = '''INSERT INTO logs_atividades (data_log, horario_log, usuario_log, tipo_log, conteudo_log) VALUES (%s, %s, %s, %s, %s);'''
                            log_values = (today, actual_time, logged_user, "Cadastro", "O usuário cadastrou o serviço {}.".format(services_description))
                            query_executor.insert_query(log_query, log_values, "Log gravado com sucesso!", "Erro ao gravar log:")

        self.main_menu = main_menu