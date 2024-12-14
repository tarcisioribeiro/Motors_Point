from data.cache.session_state import logged_user, logged_user_password


check_user_query = """
                SELECT 
                    COUNT(id_usuario)
                from 
                    usuarios;
                """

doc_name_query = """SELECT usuarios.nome, usuarios.cpf, usuarios.telefone FROM usuarios WHERE login = '{}' AND senha = '{}'""".format(
    logged_user, logged_user_password
)

name_query: str = (
    "SELECT nome FROM usuarios WHERE login = '{}' AND senha = '{}'".format(
        logged_user, logged_user_password
    )
)
sex_query: str = "SELECT sexo FROM usuarios WHERE login = '{}' AND senha = '{}'".format(
    logged_user, logged_user_password
)

check_if_user_document_exists_query = (
    """SELECT COUNT(id_usuario) FROM usuarios WHERE cpf = {};"""
)
check_if_user_login_exists_query = (
    """SELECT COUNT(id_usuario) FROM usuarios WHERE login = '{}';"""
)
