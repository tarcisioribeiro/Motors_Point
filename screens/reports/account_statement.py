from data.cache.session_state import logged_user, logged_user_password
from datetime import datetime
from dictionary.sql import user_current_accounts_query, expenses_statement_query, revenues_statement_query
from dictionary.user_stats import user_name
from dictionary.vars import to_remove_list, today, absolute_app_path
from dictionary.style import system_font
from fpdf import FPDF
from functions.get_actual_time import GetActualTime
from functions.query_executor import QueryExecutor
from time import sleep
import pandas as pd
import streamlit as st


class AccountStatement:

    def __init__(self):

        query_executor = QueryExecutor()
        actual_time = GetActualTime()

        def mount_statement_query(statement_type: str, accounts: list, initial_data: str, final_data: str):

            statement_query_list = []

            str_accounts = '''('''

            for i in range(0, len(accounts)):
                if i < (len(accounts) - 1):
                    str_accounts += "'" + str(accounts[i]) + "'" + ''', '''
                elif i == len(accounts) - 1:
                    str_accounts += "'" + str(accounts[i]) + "'"

            str_accounts = str_accounts + ''')'''

            complete_expenses_statement_query = expenses_statement_query.format(initial_data, final_data, str_accounts, logged_user, logged_user_password)
            complete_revenues_statement_query = revenues_statement_query.format(initial_data, final_data, str_accounts, logged_user, logged_user_password)

            if statement_type == 'Receitas':
                statement_query_list.append(complete_revenues_statement_query)
            elif statement_type == 'Despesas':
                statement_query_list.append(complete_expenses_statement_query)
            elif statement_type == 'Receitas e Despesas':
                statement_query_list.append(complete_revenues_statement_query)
                statement_query_list.append(complete_expenses_statement_query)
            
            return statement_query_list

        def consult_statement(statement_query_list: list):

            data_df_list = []
            statement_types = ["Receitas", "Despesas"]

            for position in range(len(statement_query_list)):

                empty_list = query_executor.complex_compund_query(statement_query_list[position], 6, 'statement_')
                description, value, date, time, category, account = (empty_list)

                if len(description) == 0 and len(value) == 0 and len(date) == 0 and len(time) == 0 and len(category) == 0 and len(account) == 0:
                    with st.expander(label="Relatório", expanded=True):
                        st.info(body="Nao há registros neste período.")

                elif len(description) > 0 and len(value) > 0 and len(date) > 0 and len(time) > 0 and len(category) > 0 and len(account) > 0: 

                    aux_str = ""

                    for i in range(0, len(time)):
                        aux_str = str(time[i])
                        time[i] = aux_str

                    with st.expander(label="Relatório de {}".format(statement_types[position]), expanded=True):

                        data_df = pd.DataFrame(
                            {
                                "Descrição": description,
                                "Valor": value,
                                "Data": date,
                                "Horário": time,
                                "Categoria": category,
                                "Conta": account,
                            }
                        )

                        data_df["Valor"] = data_df["Valor"].apply(lambda x: f"R$ {x:.2f}".replace(".", ","))
                        data_df["Data"] = pd.to_datetime(data_df["Data"]).dt.strftime("%d/%m/%Y")
                        st.dataframe(data_df, hide_index=True, use_container_width=True)

                    data_df_list.append(data_df)
            
            return value, data_df_list

        def generate_pdf(df: list, statement_type: str, initial_data: str, final_data: str, accounts: list):

            unformatted_today = datetime.strptime(today, '%Y-%m-%d')
            formatted_today = unformatted_today.strftime('%d/%m/%Y')

            time = actual_time.get_actual_time()

            accounts_str = ""
            for item in range(0, len(accounts)):
                if item < (len(accounts) - 1):
                    accounts_str = accounts_str + accounts[item] + ", "
                if item == len(accounts) - 1:
                    accounts_str = accounts_str + accounts[item] + "."

            pdf = FPDF(unit="mm", format="A4")
            pdf.add_page()
            pdf.add_font("SystemFont", "", "{}{}".format(absolute_app_path, system_font), uni=True)
            
            pdf.set_font("SystemFont", size=16)
            pdf.cell(0, 10, statement_type, ln=True, align="C")
            pdf.ln(10)

            pdf.set_font("SystemFont", size=12)
            pdf.cell(0, 5, "Período de consulta: {} à {}".format(initial_data, final_data), ln=True)
            pdf.set_font("SystemFont", size=12)
            pdf.cell(0, 10, "Contas consultadas: {}".format(accounts_str), ln=True)
            pdf.ln(5)

            statement_types = ["Receitas", "Despesas"]

            for i in range(0, len(df)):

                pdf.set_font("SystemFont", size=14)
                pdf.cell(0, 10, "{}".format(statement_types[i]), ln=True)
                pdf.ln(5)

                col_width = (pdf.w / len(df[i].columns)) * 0.85

                pdf.set_font("SystemFont", size=10)

                for col in df[i].columns:
                    pdf.cell(col_width, 5, col, border=1, align="C")
                pdf.ln()
                pdf.set_font("SystemFont", size=10)
                for _, row in df[i].iterrows():
                    for cell in row:
                        pdf.cell(col_width, 10, str(cell), border=1, align="C")
                    pdf.ln()
                pdf.ln(10)

            pdf.cell(0, 10, "Horário da consulta: {}, às {}.".format(formatted_today, time), align="R", ln=True)
            pdf.cell(0, 10, "Nome do usuário: {}.".format(user_name), align="R", ln=True)
            pdf.ln(5)

            return pdf

        def main_menu():

            user_current_accounts = query_executor.complex_consult_query(user_current_accounts_query)
            user_current_accounts = query_executor.treat_numerous_simple_result(user_current_accounts, to_remove_list)

            col4, col5, col6 = st.columns(3)

            if len(user_current_accounts) > 0:

                with col4:
                    st.subheader(body=":computer: Entrada de Dados")
                    with st.expander(label="Dados", expanded=True):

                        statement_option = st.selectbox(label="Tipos de extrato", options=["Selecione uma opção", "Receitas", "Despesas", "Receitas e Despesas"])
                        selected_accounts = st.multiselect(label="Contas", options=user_current_accounts, placeholder="Escolha a(s) conta(s)")
                        initial_data = st.date_input(label="Data de início")
                        final_data = st.date_input(label="Data de fim")
                        confirm_choice = st.checkbox(label="Confirmar dados")

                    consult_tables = st.button(label=":chart: Gerar Relatórios")

                if confirm_choice and consult_tables:

                    with col5:

                        with st.spinner(text="Aguarde..."):
                            sleep(2.5)

                        st.subheader(body=":bar_chart: Resultados")
                    
                        if statement_option != "Selecione uma opção" and len(selected_accounts) > 0 and (initial_data <= final_data):
                                query_list = mount_statement_query(statement_option, selected_accounts, initial_data, final_data)

                                value, dataframes = consult_statement(query_list)

                                with col6:
                                    with st.spinner(text="Aguarde..."):
                                        sleep(2.5)

                                    total_value = 0
                                    for i in range(0, len(value)):
                                        total_value += value[i]
                                        medium_value = round((total_value / len(value)), 2)
                                        
                                    medium_value = str(medium_value)
                                    medium_value = medium_value.replace(".", ",")
                                    total_value = str(total_value)
                                    total_value = total_value.replace(".", ",")

                                    st.subheader(body=":information_source: Informações")

                                    with st.expander(label="Dados", expanded=True):
                                        st.info(body="Quantidade de {}: {}.".format(statement_option.lower(), len(value)))
                                        st.info(body="Valor total das {}: R$ {}.".format(statement_option.lower(), total_value))
                                        st.info(body="Valor médio das {}: R$ {}.".format(statement_option.lower(), medium_value))

                                    formatted_initial_data = initial_data.strftime("%d/%m/%Y")
                                    formatted_final_data = final_data.strftime("%d/%m/%Y")

                                    log_query = '''INSERT INTO financas.logs_atividades (usuario_log, tipo_log, conteudo_log) VALUES ( %s, %s, %s);'''
                                    log_values = (logged_user, "Consulta", "Consultou o relatório de {} entre o período de {} a {}.".format(statement_option, formatted_initial_data, formatted_final_data))
                                    query_executor.insert_query(log_query, log_values, "Log gravado.", "Erro ao gravar log:")

                                    time = actual_time.get_actual_time()

                                    pdf = generate_pdf(dataframes, statement_option, formatted_initial_data, formatted_final_data, selected_accounts)
                                    pdf_bytes = pdf.output(dest='S').encode('latin1')
    
                                    st.download_button(
                                        label=":floppy_disk: Baixar PDF",
                                        data=pdf_bytes,
                                        file_name="extrato_bancario_{}_{}_a_{}_{}.pdf".format(statement_option.replace(" ", "_").lower(), initial_data, final_data, time),
                                        mime="application/pdf",
                                    )

                        elif (len(selected_accounts) == 0) or (initial_data > final_data) or (statement_option == "Selecione uma opção"):
                            with st.expander(label="Avisos", expanded=True):
                                if statement_option == "Selecione uma opção":
                                    st.error(body="Selecione um tipo de extrato.")
                                if len(selected_accounts) == 0:
                                    st.error(body="Nenhuma conta selecionada.")
                                if initial_data > final_data:
                                    st.error(body="A data inicial não pode ser maior que a final.")

            elif len(user_current_accounts) == 0:
                with col5:
                    st.warning(body="Você ainda não possui contas cadastradas.")

        self.main_menu = main_menu
