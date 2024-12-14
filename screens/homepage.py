from datetime import datetime
from functions.query_executor import QueryExecutor
import pandas as pd
import streamlit as st


class Home:

    def __init__(self):

        col1, col2, col3 = st.columns(3)

        query_executor = QueryExecutor()

        def main_menu():
            
            with col1:
                st.header(body=":car: Motors Point")
            
            st.divider()

        self.main_menu = main_menu