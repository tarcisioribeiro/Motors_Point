#!/bin/bash
red() {
    echo -e "\033[31m$1\033[0m"
}
green() {
    echo -e "\033[32m$1\033[0m"
}

blue() {
    echo -e "\033[34m$1\033[0m"
}

FOLDER=$(pwd)

#!/bin/bash

while true; do
    blue "\nDigite a senha de root:"
    read -s root_password
    sleep 1
    blue "\nDigite a senha de root novamente: "
    read -s confirm_root_password
    sleep 1

    echo "$root_password" | sudo -S echo "Senha de root aceita."

    if [ $? -eq 0 ]; then
        green "\nVocê tem permissões de root. Continuando com o script..."
        sleep 1
        blue "\nInstalando dependências..."
        sleep 5
        apt install build-essential openssh-server git neofetch curl net-tools wget mysql-server python3-venv python3-tk python3-pip python3.10-full python3.10-dev dkms perl gcc make default-libmysqlclient-dev libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev libncurses5-dev libncursesw5-dev llvm xz-utils tk-dev libffi-dev liblzma-dev python3-openssl -y
        ufw enable
        ufw allow 8501
        ufw allow OpenSSH
        break
    else
        red "\nSenha de root incorreta. Saindo..."
        sleep 1
        exit 1
    fi
done

sleep 1
clear

while true; do
    blue "\nDefina a senha do banco de dados: "
    read -s password
    sleep 1
    blue "\nRepita a senha: "
    read -s confirmation
    sleep 1

    if [ "$password" = "$confirmation" ]; then
        green "\nSenhas coincidem. Configurando o banco de dados..."
        sleep 5
        sudo mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '$password';"
        cd documentation/
        mysql -u root -p"$password" < implantation_erp.sql
        break
    else
        red "\nAs senhas não coincidem. Tente novamente."
        sleep 1
    fi
done

sleep 1
clear

cd $FOLDER
blue "\nCriando ambiente virtual..."
sleep 5
python3 -m venv venv
blue "\nAtivando ambiente virtual..."
sleep 5
source venv/bin/activate
pip install -r requirements.txt

sleep 1
clear

echo "#!/bin/bash" >> motors_point.sh
echo "cd $FOLDER" >> motors_point.sh
echo "source venv/bin/activate" >> motors_point.sh
echo "streamlit run main.py --server.port 8510" >> motors_point.sh
chmod u+x motors_point.sh
sudo mv motors_point.sh /usr/bin/

echo "[Unit]" >> motors_point.service
echo "Description=Motors Point" >> motors_point.service
echo "[Service]" >> motors_point.service
echo "ExecStart=/usr/bin/motors_point.sh" >> motors_point.service
echo "[Install]" >> motors_point.service
echo "WantedBy=multi-user.target" >> motors_point.service
sudo mv motors_point.service /lib/systemd/system

sudo systemctl enable motors_point.service
sudo systemctl daemon-reload
sudo systemctl start motors_point.service

green "\nInstalação concluída."

link=$(python3 services/linux/get_ipv4.py)

sleep 5

blue "Você pode realizar o acesso a aplicação através dos seguintes links:\n"
green "$link"
