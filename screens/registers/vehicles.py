from data.cache.session_state import logged_user
from dictionary.vars import today, to_remove_list
from functions.query_executor import QueryExecutor
from functions.get_actual_time import GetActualTime
from time import sleep
import re
import streamlit as st


class Vehicles:

    def __init__(self):

        query_executor = QueryExecutor()
        get_actual_time = GetActualTime()

        def validate_year(str_year: str):
            if len(str_year) == 4 and str_year.isdigit():
                st.success(body="Ano válido.")
                return True
            else:
                st.error(body="Ano inválido.")
                return False

        
        def validate_plate(plate: str):

            plate = plate.strip().upper()

            old_pattern = r"^[A-Z]{3}-?\d{4}$"
            mercosul_pattern = r"^[A-Z]{3}\d[A-Z]\d{2}$"

            if re.match(old_pattern, plate):
                st.success(body="Placa válida no modelo antigo de emplacamento.")
                return True        
            elif re.match(mercosul_pattern, plate):
                st.success(body="Placa válida no modelo Mercosul de emplacamento.")
                return True
            else:
                st.error(body="Placa inválida.")
                return False

        def main_menu():

            col1, col2, col3 = st.columns(3)

            check_if_clients_exists_query = '''SELECT COUNT(id_cliente) FROM clientes;'''
            check_if_clients_exists = query_executor.simple_consult_query(check_if_clients_exists_query)
            check_if_clients_exists = int(query_executor.treat_simple_result(check_if_clients_exists, to_remove_list))

            if check_if_clients_exists == 0:
                with col2:
                    st.warning(body="Ainda não há clientes cadastrados.")

            elif check_if_clients_exists >= 1:

                get_clients_query = '''SELECT id_cliente, nome FROM clientes;'''
                get_clients = query_executor.complex_consult_query(get_clients_query)
                clients = dict(get_clients)

                get_brands_query = '''SELECT nome FROM marcas;'''
                get_brands = query_executor.complex_consult_query(get_brands_query)
                brands = query_executor.treat_numerous_simple_result(get_brands, to_remove_list)
                brands.sort()
                

                with col1:
                    st.subheader(body=":computer: Entrada de Dados")

                    with st.expander(label="Dados", expanded=True):
                        proprietary = st.selectbox(label="Proprietário", options=clients.values())
                        searched_value = proprietary
                        proprietary_id = next((k for k, v in clients.items() if v == searched_value), None)
                        plate = st.text_input(label="Placa do veículo", max_chars=10, placeholder="ABC-1234")
                        brand = st.selectbox(label="Marca", options=brands)
                        model = st.text_input(label="Modelo", max_chars=100)
                        year = st.text_input(label="Ano", max_chars=4)
                        confirm_vehicle_data = st.checkbox(label="Confirmar dados")

                    register_vehicle = st.button(label=":floppy_disk: Registrar veículo")

                    if confirm_vehicle_data and register_vehicle:
                        with col2:
                            with st.spinner(text="Aguarde..."):
                                sleep(2.5)

                            st.subheader(body=":white_check_mark: Validação dos dados")
                        
                        if plate != "" and model != "" and year != "":
                            with col2:
                                with st.expander(label="Dados", expanded=True):
                                    is_plate_valid = validate_plate(plate)
                                    is_year_valid = validate_year(year)

                                    if is_year_valid and is_plate_valid:
                                        actual_time = get_actual_time.get_actual_time()
                                        
                                        st.success(body="Dados válidos.")

                                        new_car_query = '''INSERT INTO veiculos (cliente_id, placa, marca, modelo, ano) VALUES (%s, %s, %s, %s, %s)'''
                                        new_car_values = (proprietary_id, plate, brand, model, year)
                                        query_executor.insert_query(new_car_query, new_car_values, "Carro cadastrado com sucesso!", "Erro ao cadastrar carro:")

                                        log_query = '''INSERT INTO logs_atividades (data_log, horario_log, usuario_log, tipo_log, conteudo_log) VALUES (%s, %s, %s, %s, %s);'''
                                        log_values = (today, actual_time, logged_user, "Cadastro", "O usuário cadastrou um veículo modelo {} ano {} da marca {}.".format(model, year, brand))
                                        query_executor.insert_query(log_query, log_values, "Log gravado com sucesso!", "Erro ao gravar log:")

                                    elif is_year_valid == False and is_plate_valid == False:
                                        with col2:
                                            with st.expander(label="Dados", expanded=True):
                                                st.error(body="Dados inválidos.")
                                                st.error(body="Ano inválido.")

                        elif plate == "" or model == "" or year == "":
                            with col2:
                                with st.expander(label="Aviso", expanded=True):
                                    if plate == "":
                                        st.warning(body="A placa do veículo não foi informada.")
                                    if model == "":
                                        st.warning(body="O modelo do veículo não foi informado.")
                                    if year == "":
                                        st.warning(body="O ano do veículo não foi informado.")

                    elif confirm_vehicle_data == False and register_vehicle:

                        with col2:
                            with st.spinner(text="Aguarde..."):
                                sleep(2.5)

                            st.subheader(body=":white_check_mark: Validação de Dados")
                            with st.expander(label="Aviso", expanded=True):
                                st.warning(body="Revise e confirme os dados antes de prosseguir.")

        self.main_menu = main_menu