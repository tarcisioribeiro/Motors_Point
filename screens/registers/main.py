from screens.registers.vehicles import Vehicles
from screens.registers.clients import Clients
from screens.registers.part import Parts
from screens.registers.services import Services
import streamlit as st


class Registers:

    def __init__(self):

        def registers_main_menu():

            col1, col2, col3 = st.columns(3)

            registers_menu_options = {
                "Clientes": Clients(),
                "Veículos": Vehicles(),
                "Peças": Parts(),
                "Serviços": Services(),
            }

            with col1:
                st.header(body=":memo: Cadastros")

            with col2:

                selected_menu_option = st.selectbox(
                    label="Menu", options=registers_menu_options.keys()
                )

            st.divider()

            if selected_menu_option:
                call_interface = registers_menu_options[selected_menu_option]
                call_interface.main_menu()

        self.main_menu = registers_main_menu
