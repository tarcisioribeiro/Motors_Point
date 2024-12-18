from data.cache.session_state import logged_user
from dictionary.vars import today, to_remove_list
from functions.query_executor import QueryExecutor
from functions.validate_document import Documents
from functions.get_actual_time import GetActualTime
from time import sleep
import streamlit as st
import re


class Clients:

    def __init__(self):

        query_executor = QueryExecutor()
        validate_document = Documents()

        def validate_phone_number(phone_number: str):
            phone_number = re.sub(r"\D", "", phone_number)
            
            pattern = r"^(?:\d{2})?\d{8,9}$"
            
            if re.match(pattern, phone_number):
                st.success(body=f"Número de telefone válido: {phone_number}")
                return True
            else:
                st.error(body=f"Número de telefone inválido: {phone_number}")
                return False

        def main_menu():

            col1, col2, col3 = st.columns(3)

            with col1:
                st.subheader(body=":computer: Entrada de Dados")
                with st.expander(label="Dados", expanded=True):
                    client_name = st.text_input(label="Nome do cliente", max_chars=100)
                    client_document = st.text_input(label="CPF/CNPJ do cliente", placeholder="XXX.XXX.XXX-XX")
                    client_phone = st.text_input(label="Telefone do cliente", max_chars=15)
                    confirm_client_data = st.checkbox(label="Confirmar dados")

                register_button = st.button(label=":floppy_disk: Cadastrar cliente")
        
            if confirm_client_data and register_button:

                if client_name != "" and client_document != "" and client_phone != "":

                    with col2:

                        with st.spinner(text="Aguarde..."):
                            sleep(2.5)
                        st.subheader(body=":white_check_mark: Validação de Dados")

                        with st.expander(label="Dados", expanded=True):

                            is_client_document_valid = validate_document.validate_owner_document(client_document)
                            is_phone_valid = validate_phone_number(client_phone)

                            if is_client_document_valid == True and is_phone_valid == True:
                                actual_time = GetActualTime().get_actual_time()
                                
                                st.success(body="Dados válidos.")

                                check_if_user_exists_query = '''SELECT COUNT(id_cliente) FROM clientes WHERE nome = "{}";'''.format(client_name)
                                check_if_user_exists = query_executor.simple_consult_query(check_if_user_exists_query)
                                check_if_user_exists = query_executor.treat_simple_result(check_if_user_exists, to_remove_list)
                                check_if_user_exists = int(check_if_user_exists)
                                
                                if check_if_user_exists == 0:

                                    insert_query = '''INSERT INTO clientes (nome, cpf_cnpj, telefone_celular) VALUES (%s, %s, %s)'''
                                    insert_values = (client_name, client_document, client_phone)
                                    query_executor.insert_query(insert_query, insert_values, "Cliente cadastrado com sucesso!", "Erro ao cadastrar cliente:")

                                    log_query = '''INSERT INTO logs_atividades (data_log, horario_log, usuario_log, tipo_log, conteudo_log) VALUES (%s, %s, %s, %s, %s)'''
                                    log_values = (today, actual_time, logged_user, "Cadastro", "O usuário {} cadastrou o cliente {}.".format(logged_user, client_name))
                                    query_executor.insert_query(log_query, log_values, "Log gravado com sucesso!", "Erro ao gravar log:")
                            
                                else:
                                    st.error(body="O cliente {} já foi cadastrado anteriormente.".format(client_name))

                elif client_name == "" or client_document == "" or client_phone == "":
                    with col2:

                        with st.spinner(text="Aguarde..."):
                            sleep(2.5)

                        st.subheader(body=":white_check_mark: Validação de Dados")

                        with st.expander(label="Aviso", expanded=True):
                            st.warning(body="Revise e confirme os dados antes de prosseguir.")
                            if client_name == "":
                                st.warning(body="O nome do cliente não foi informado.")
                            if client_document == "":
                                st.warning(body="O documento não foi preenchido.")
                            if client_phone == "":
                                st.warning(body="O telefone não foi preenchido.")   

            elif confirm_client_data == False and register_button:

                with col2:

                    with st.spinner(text="Aguarde..."):
                        sleep(2.5)

                    st.subheader(body=":white_check_mark: Validação de Dados")

                    with st.expander(label="Aviso", expanded=True):
                        st.warning(body="Revise e confirme os dados antes de prosseguir.")
                        if client_name == "":
                            st.warning(body="O nome do cliente não foi informado.")
                        if client_document == "":
                            st.warning(body="O documento não foi preenchido.")
                        if client_phone == "":
                            st.warning(body="O telefone não foi preenchido.")

        self.main_menu = main_menu