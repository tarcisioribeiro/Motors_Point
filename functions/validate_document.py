import streamlit as st
import re


class Documents:
    def __init__(self):

        def validate_credit_card(card_number: str):

            total=0

            st.info('Validando cartão...')

            if (len(card_number) != 16):
                return False
                
            for i in range(0,16,2):
                accumulated = int(card_number[i]) * 2
                if (accumulated > 9):
                    accumulated = accumulated - 9
                total = total + accumulated

            for i in range(1,17,2):
                total = total + int(card_number[i])
                
            if ((total%10) != 0 or total > 150):
                return False

            return True
        
        def validate_cpf(cpf: str):
            st.info(body="Validando CPF...")
            
            if cpf == cpf[0] * len(cpf):
                st.error(body="CPF inválido: todos os números são iguais.")
                return False
            
            first_sum = sum(int(cpf[i]) * (10 - i) for i in range(9))
            first_digit = (first_sum * 10 % 11) % 10

            second_sum = sum(int(cpf[i]) * (11 - i) for i in range(10))
            second_digit = (second_sum * 10 % 11) % 10

            if int(cpf[9]) == first_digit and int(cpf[10]) == second_digit:
                return True
            else:
                st.error(body="CPF inválido.")
                return False

        def validate_cnpj(cnpj: str):
            st.info(body="Validando CNPJ...")
            
            if cnpj == cnpj[0] * len(cnpj):
                st.error(body="CNPJ inválido: todos os números são iguais.")
                return False

            weights_first = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
            weights_second = [6] + weights_first

            first_sum = sum(int(cnpj[i]) * weights_first[i] for i in range(12))
            first_digit = (first_sum % 11)
            first_digit = 0 if first_digit < 2 else 11 - first_digit

            second_sum = sum(int(cnpj[i]) * weights_second[i] for i in range(13))
            second_digit = (second_sum % 11)
            second_digit = 0 if second_digit < 2 else 11 - second_digit

            if int(cnpj[12]) == first_digit and int(cnpj[13]) == second_digit:
                return True
            else:
                st.error(body="CNPJ inválido.")
                return False

        def validate_owner_document(owner_document: str):
            owner_document = re.sub(r"\D", "", owner_document)
            
            if len(owner_document) == 11:
                return validate_cpf(owner_document)
            elif len(owner_document) == 14:
                return validate_cnpj(owner_document)
            else:
                st.error(body="O documento deve conter 11 caracteres (CPF) ou 14 caracteres (CNPJ), desconsiderando pontuações.")
                return False

        self.validate_owner_document = validate_owner_document
        self.validate_credit_card = validate_credit_card