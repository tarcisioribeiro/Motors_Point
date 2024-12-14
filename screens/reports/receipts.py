import pandas as pd
import streamlit as st
from data.cache.session_state import logged_user, logged_user_password
from dictionary.user_stats import user_name
from dictionary.style import system_font
from datetime import datetime
from dictionary.vars import operational_system, today, actual_horary, to_remove_list, absolute_app_path, decimal_values, SAVE_FOLDER
from functions.query_executor import QueryExecutor
from functions.variable import Variable
from PIL import Image, ImageDraw, ImageFont
from time import sleep


class Receipts:
    def __init__(self):

        query_executor = QueryExecutor()
        variable = Variable()

        def validate_query(table: str, date, account: str, value: float):

            if table == "despesas":
                id_query = """
                            SELECT 
                                despesas.id_despesa
                            FROM
                                despesas
                                INNER JOIN usuarios ON despesas.proprietario_despesa = usuarios.nome AND despesas.documento_proprietario_despesa = usuarios.cpf
                            WHERE
                                despesas.data = '{}'
                                    AND despesas.conta = '{}'
                                    AND despesas.valor = {}
                                    AND usuarios.login = '{}'
                                    AND usuarios.senha = '{}';""".format(
                    date.strftime("%Y-%m-%d"),
                    account,
                    value,
                    logged_user,
                    logged_user_password,
                )

            if table == "receitas":
                id_query = """
                            SELECT 
                                receitas.id_receita
                            FROM
                                receitas
                                INNER JOIN usuarios ON receitas.proprietario_receita = usuarios.nome AND receitas.documento_proprietario_receita = usuarios.cpf
                            WHERE
                                receitas.data = '{}'
                                    AND receitas.conta = '{}'
                                    AND receitas.valor = {}
                                    AND usuarios.login = '{}'
                                    AND usuarios.senha = '{}';""".format(
                    date.strftime("%Y-%m-%d"),
                    account,
                    value,
                    logged_user,
                    logged_user_password,
                )

            if table == "despesas_cartao_credito":
                id_query = """
                                SELECT 
                                    despesas_cartao_credito.id_despesa_cartao
                                FROM
                                    despesas_cartao_credito
                                        INNER JOIN
                                    usuarios ON despesas_cartao_credito.proprietario_despesa_cartao = usuarios.nome
                                        AND despesas_cartao_credito.doc_proprietario_cartao = usuarios.cpf
                                WHERE
                                    despesas_cartao_credito.data = '{}'
                                        AND despesas_cartao_credito.cartao = '{}'
                                        AND despesas_cartao_credito.valor = {}
                                        AND usuarios.login = '{}'
                                        AND usuarios.senha = '{}';""".format(
                    date.strftime("%Y-%m-%d"),
                    account,
                    value,
                    logged_user,
                    logged_user_password,
                )

            if table == "emprestimos":
                id_query = """
                                SELECT 
                                    emprestimos.id_emprestimo
                                FROM
                                    emprestimos
                                        INNER JOIN
                                    usuarios ON emprestimos.credor = usuarios.nome
                                        AND emprestimos.documento_credor = usuarios.cpf
                                WHERE
                                    emprestimos.data = '{}'
                                        AND emprestimos.conta = '{}'
                                        AND emprestimos.valor = {}
                                        AND usuarios.login = '{}'
                                        AND usuarios.senha = '{}';""".format(
                    date.strftime("%Y-%m-%d"),
                    account,
                    value,
                    logged_user,
                    logged_user_password,
                )

            data_exists = False


            id = query_executor.complex_consult_query(id_query)
            id = query_executor.treat_numerous_simple_result(id, to_remove_list)
            
            if len(id) >= 1:
                ids_string = ""

                for i in range(0, len(id)):
                    if i == 0:
                        ids_string = id[i]
                    else:
                        ids_string = ids_string + ", " + id[i]

                return ids_string, True

            elif len(id) == 0:
                return 0, False

        def execute_query(table: str, id_list):

            if table == "despesas_cartao_credito":
                values_query = """SELECT descricao, valor, data, horario, categoria, cartao FROM {} WHERE id_despesa_cartao IN({});""".format(table, id_list)
            elif table == "receitas":
                values_query = """SELECT descricao, valor, data, horario, categoria, conta FROM {} WHERE id_receita IN({});""".format(table, id_list)
            elif table == "despesas":
                values_query = """SELECT descricao, valor, data, horario, categoria, conta FROM {} WHERE id_despesa IN({});""".format(table, id_list)

            consult_values = query_executor.complex_compund_query(values_query, 6, "query_values")

            return consult_values

        def treat_receipt_values(receipt_list):

            len_lists_receipt = 0
            for i in range(0, len(receipt_list)):
                len_lists_receipt += len(receipt_list[i])

            if len(receipt_list) >= 5 and len_lists_receipt >= 5:

                description = receipt_list[0]
                description_list = []

                for i in range(0, len(description)):
                    aux_description = query_executor.treat_simple_result(description[i], to_remove_list)
                    description_list.append(aux_description)

                value = receipt_list[1]
                value_list = []

                for i in range(0, len(value)):
                    aux_value = query_executor.treat_simple_result(value[i], to_remove_list)
                    aux_value = float(aux_value)
                    value_list.append(aux_value)

                date = receipt_list[2]
                date_list = []
                
                for i in range(0, len(date)):
                    aux_date = query_executor.treat_simple_result(date[i], to_remove_list)
                    aux_date = aux_date.replace(" ", "-")
                    date_list.append(aux_date)

                time = receipt_list[3]
                time_list = []

                for i in range(0, len(time)):
                    aux_time = query_executor.treat_simple_result(time[i], to_remove_list)
                    aux_time = str(aux_time)
                    time_list.append(aux_time)

                category = receipt_list[4]
                category_list = []

                for i in range(0, len(category)):
                    aux_category = query_executor.treat_simple_result(category[i], to_remove_list)
                    category_list.append(aux_category)

                account = receipt_list[5]
                account_list = []

                for i in range(0, len(account)):
                    aux_account = query_executor.treat_simple_result(account[i], to_remove_list)
                    account_list.append(aux_account)

                return description_list, value_list, date_list, time_list, category_list, account_list

        def generate_transfer_receipt(id, description, value, date, category, origin_account, destiny_account):

            # origin_account_image = query_executor.simple_consult_query(account_image_query.format(origin_account, logged_user, logged_user_password))
            # origin_account_image = query_executor.treat_simple_result(origin_account_image, to_remove_list)
            # origin_account_image_path = SAVE_FOLDER + origin_account_image
            # origin_pasted_image = Image.open(origin_account_image_path)

            # destiny_account_image = query_executor.simple_consult_query(account_image_query.format(destiny_account, logged_user, logged_user_password))
            # destiny_account_image = query_executor.treat_simple_result(destiny_account_image, to_remove_list)
            # destiny_account_image_path = SAVE_FOLDER + destiny_account_image
            # destiny_pasted_image = Image.open(destiny_account_image_path)

            float_value = round(value, 2)
            str_value = str(float_value)
            str_value = str_value.replace(".", ",")

            last_two_digits = str_value[-2:]
            if last_two_digits in decimal_values:
                str_value = str_value + "0"

            reference_number = ""
            if id <= 9:
                reference_number = """REF: 000{}""".format(id)
            if id >= 10 and id <= 99:
                reference_number = """REF: 00{}""".format(id)
            if id >= 100 and id <= 999:
                reference_number = """REF: 0{}""".format(id)
            
            width, height = 900, 450
            dpi = 300
            image = Image.new("RGB", (width, height), "white")
            draw = ImageDraw.Draw(image)
            font_size = 20

            if operational_system == "nt":
                font = ImageFont.truetype("cour.ttf", font_size)
            elif operational_system == "posix":
                font = ImageFont.truetype(
                    "{}{}".format(absolute_app_path, system_font),
                    font_size,
                )

            border_color = "black"
            border_width = 4
            border_box = [
                (border_width, border_width),
                (width - border_width, height - border_width),
            ]
            draw.rectangle(border_box, outline=border_color, width=border_width)

            header_font_size = 20

            if operational_system == "nt":
                header_font = ImageFont.truetype("cour.ttf", header_font_size)
            elif operational_system == "posix":
                header_font = ImageFont.truetype(
                    "{}{}".format(absolute_app_path, system_font),
                    font_size,
                )

            header_text = "Comprovante de Transferência"
            header_text_width, header_text_height = draw.textsize(
                header_text, font=header_font
            )
            header_position = ((width - header_text_width) / 2, 10)
            draw.text(header_position, header_text, fill="black", font=header_font)

            draw.line([(20, 40), (width - 20, 40)], fill="black", width=2)
            draw.text((20, 60), f"Descrição: {description}", fill="black", font=font)
            draw.text((20, 90), f"Valor: R$ {str_value}", fill="black", font=font)
            draw.text((20, 120), f"Data: {date.strftime('%d/%m/%Y')}", fill="black", font=font)
            draw.text((20, 150), f"Categoria: {category}", fill="black", font=font)
            draw.text((20, 180), f"Conta de Origem: {origin_account}", fill="black", font=font)
            draw.text((20, 210), f"Conta de Destino: {destiny_account}", fill="black",font=font)
            draw.line([(20, 240), (width - 20, 240)], fill="black", width=2)
            draw.line([(width - 400, height - 60), (width - 20, height - 60)],fill="black", width=2)
            draw.text((520, 400), f"{user_name}", fill="black", font=font)
            draw.text((20, height - 40), reference_number, fill="black", font=font)

            image.paste((20, 250))
            image.paste((170, 250))
            image.paste((320, 250))

            caminho_arquivo = "{}/data/receipts/transfers/Comprovante_de_transferencia_{}_{}.png".format(absolute_app_path, today, actual_horary)

            image.save(caminho_arquivo, dpi=(dpi, dpi))
            st.image(caminho_arquivo, use_container_width=True)

            with open(caminho_arquivo, "rb") as file:
                download_button = st.download_button(label=":floppy_disk: Baixar imagem", data=file, file_name=caminho_arquivo)

        def generate_receipt(table: str, id, description: str, value: float, date, category: str, account: str):

            # account_image = query_executor.simple_consult_query(account_image_query.format(account, logged_user, logged_user_password))
            # account_image = query_executor.treat_simple_result(account_image, to_remove_list)
            # account_image_path = SAVE_FOLDER + account_image

            table_dictionary = {
                "receitas": "Receita",
                "emprestimos": "Empréstimo",
                "despesas": "Despesa",
                "despesas_cartao_credito": "Despesa de Cartão"
            }

            table = table_dictionary[table]

            value = round(value, 2)
            value = str(value)
            value = value.replace(".", ",")

            last_two_digits = value[-2:]
            if last_two_digits in decimal_values:
                value = value + "0"

            reference_number = ""
            if id <= 9:
                reference_number = """REF: 000{}""".format(id)
            if id >= 10 and id <= 99:
                reference_number = """REF: 00{}""".format(id)
            if id >= 100 and id <= 999:
                reference_number = """REF: 0{}""".format(id)

            table = table.capitalize()
            description = description.replace("'", "")
            category = category.capitalize()
            category = category.replace("'", "")
            account = account.replace("'", "")

            date = datetime.strptime(date, "%Y-%m-%d")
            date = date.strftime("%d/%m/%Y")

            width, height = 800, 400
            dpi = 300
            image = Image.new("RGB", (width, height), "white")
            draw = ImageDraw.Draw(image)
            font_size = 20

            if operational_system == "nt":
                font = ImageFont.truetype("cour.ttf", font_size)
            elif operational_system == "posix":
                font = ImageFont.truetype("{}{}".format(absolute_app_path, system_font), font_size)

            border_color = "black"
            border_width = 4
            border_box = [(border_width, border_width),(width - border_width, height - border_width)]
            draw.rectangle(border_box, outline=border_color, width=border_width)

            header_font_size = 20

            if operational_system == "nt":
                header_font = ImageFont.truetype("cour.ttf", font_size)
            elif operational_system == "posix":
                header_font = ImageFont.truetype(
                    "{}{}".format(absolute_app_path, system_font),
                    font_size,
                )

            header_text = "Comprovante de {}".format(table)
            header_text_width, header_text_height = draw.textsize(
                header_text, font=header_font
            )
            header_position = ((width - header_text_width) / 2, 10)
            draw.text(header_position, header_text, fill="black", font=header_font)

            draw.line([(20, 40), (width - 20, 40)], fill="black", width=2)
            draw.text((20, 60), f"Descrição: {description}", fill="black", font=font)
            draw.text((20, 90), f"Valor: R$ {value}", fill="black", font=font)
            draw.text((20, 120), f"Data: {date}", fill="black", font=font)
            draw.text((20, 150), f"Categoria: {category}", fill="black", font=font)
            draw.text((20, 180), f"Conta: {account}", fill="black", font=font)
            draw.line([(20, 210), (width - 20, 210)], fill="black", width=2)
            draw.line([(width - 400, height - 60), (width - 20, height - 60)], fill="black", width=2)
            draw.text((400, 360), f"{user_name}", fill="black", font=font)
            draw.text((20, height - 40), reference_number, fill="black", font=font)

            # pasted_image = Image.open(account_image_path)

            # image.paste(pasted_image, (20, 220))

            caminho_arquivo = "{}/data/receipts/reports/Relatorio_{}_{}.png".format(
             absolute_app_path, today, actual_horary
            ) 
            image.save(caminho_arquivo, dpi=(dpi, dpi))
            st.image(caminho_arquivo, use_container_width=True)

            with open(caminho_arquivo, "rb") as file:
                download_button = st.download_button(
                    label=":floppy_disk: Baixar imagem",
                    data=file,
                    file_name="Relatorio_{}_{}.png".format(today, actual_horary),
                )

        def get_receipt_input():

            col4, col5, col6 = st.columns(3)

            # user_current_accounts = query_executor.complex_consult_query(user_current_accounts_query)
            # user_current_accounts = query_executor.treat_numerous_simple_result(user_current_accounts, to_remove_list)

            # if len(user_current_accounts) > 0:

            with col4:

                receipt_options = {
                    "Despesa": "despesas",
                    "Despesa de Cartão": "despesas_cartao_credito",
                    "Receita": "receitas",
                    "Empréstimo": "emprestimos"
                }

                st.subheader(body=":computer: Entrada de Dados")

                with st.expander(label="Filtros", expanded=True):
                    report_type = st.selectbox(label="Relatório", options=receipt_options.keys())
                    date = st.date_input(label="Data")
                    account = st.selectbox(label="Conta", options=["user_current_accounts"])
                    value = st.number_input(label="Valor",placeholder="Informe o valor",min_value=0.01,step=0.01)
                    confirm_data = st.checkbox(label="Confirmar dados")

                send_value_button = st.button(label=":white_check_mark: Enviar dados")

                if send_value_button and confirm_data:

                    table = receipt_options[report_type]

                    with col5:
                        with st.spinner(text="Aguarde..."):
                            sleep(2.5)
                        st.subheader(body=":page_facing_up: Resultados")

                        query_data, is_query_valid = validate_query(table, date, account, value)

                        if is_query_valid == True:

                            with st.expander(label=":bar_chart: Resultados", expanded=True):

                                st.info("Registro(s) encontrado(s): {}.".format(query_data))

                                query = execute_query(table, query_data)
                                description, value, date, time, category, account = treat_receipt_values(query)

                                str_value_list = []

                                for i in range(0, len(value)):
                                    aux_value = str(value[i])
                                    aux_value = aux_value.replace(".", ",")
                                    last_two_digits = aux_value[-2:]
                                    if last_two_digits in decimal_values:
                                        aux_value = aux_value + "0"
                                    aux_value = 'R$ ' + aux_value
                                    str_value_list.append(aux_value)

                                formatted_date_list = []

                                for i in range(0, len(date)):
                                    aux_date = date[i]
                                    aux_date = datetime.strptime(aux_date, '%Y-%m-%d')
                                    aux_date = aux_date.strftime('%d/%m/%Y')
                                    formatted_date_list.append(aux_date)
                                
                                str_ids_list = []
                                aux_str = query_data.replace(",", "").split()
                                str_ids_list = aux_str
                                
                                ids_list = []
                                for i in range(0, len(str_ids_list)):
                                    aux_int = int(str_ids_list[i])
                                    ids_list.append(aux_int)

                                data_df = pd.DataFrame(
                                    {
                                        "Descrição": description,
                                        "Valor": str_value_list,
                                        "Data": formatted_date_list,
                                        "Categoria": category,
                                        "Conta": account
                                    })

                                st.dataframe(data_df, hide_index=True, use_container_width=True)

                                confirm_register_selection = st.checkbox(label="Confirmar seleção")

                            generate_receipt_button = st.button(label=":pencil: Gerar Comprovante")

                            if confirm_register_selection == True and generate_receipt_button:
                                with st.spinner(text="Aguarde..."):
                                    sleep(2.5)

                                with col6:
                                    st.subheader(body=":pencil: Comprovante")
                                    generate_receipt(table, 106, description, value, date, category, account)

                                log_query = '''INSERT INTO financas.logs_atividades (usuario_log, tipo_log, conteudo_log) VALUES ( %s, %s, %s);'''
                                log_values = (logged_user, "Consulta", "Consultou um comprovante de {} na data {}, associado a conta {}.".format(report_type, date, account))
                                query_executor.insert_query(log_query, log_values, "Log gravado.", "Erro ao gravar log:")

                        elif is_query_valid == False:
                            with st.expander(label="Resultados", expanded=True):
                                st.info("Nenhum resultado Encontrado.")

                elif confirm_data == False and send_value_button:
                    with col5:
                        with st.spinner(text="Aguarde..."):
                            sleep(2.5)
                        st.subheader(body=":white_check_mark: Validação de dados")
                        with st.expander(label="Avisos", expanded=True):
                            st.warning(body="Revise e confirme os dados antes de prosseguir.")

            with col5:
                st.warning(body="Você ainda não possui contas cadastradas.")
                    
        self.main_menu = get_receipt_input
        self.generate_receipt = generate_receipt
        self.generate_transfer_receipt = generate_transfer_receipt