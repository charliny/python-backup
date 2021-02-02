import schedule
import time
import shutil
from smb.SMBConnection import SMBConnection
import os
import zipfile
from datetime import datetime as dt


def data_e_dia():
    weekday_name = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    wkday = dt.now().weekday()
    dia_da_semana = weekday_name[wkday]
    data_hora = str(dt.now().strftime('%d_%m_%Y')).replace(':', '.')
    data = data_hora[:10]
    return dia_da_semana, data


def criar_arquivo_zip(output_filename, source_dir):
    relroot = os.path.abspath(os.path.join(source_dir, os.pardir))
    with zipfile.ZipFile(output_filename, "w", zipfile.ZIP_DEFLATED) as zip:
        for root, dirs, files in os.walk(source_dir):
            # add directory (needed for empty dirs)
            zip.write(root, os.path.relpath(root, relroot))
            for file in files:
                filename = os.path.join(root, file)
                if os.path.isfile(filename):  # regular files only
                    arcname = os.path.join(os.path.relpath(root, relroot), file)
                    zip.write(filename, arcname)


def bkp_servidor(salvar_em, fazer_bkp_de):
    userID = 'usuario'
    password = 'senha'
    client_machine_name = 'SERVER'
    server_name = 'SERVER'
    server_ip = 'IP'
    domain_name = 'dominio'
    conn = SMBConnection(userID, password, client_machine_name, server_name, domain=domain_name, use_ntlm_v2=True,
                         is_direct_tcp=True)
    conn.connect(server_ip, 445)
    shares = conn.listShares()
    for share in shares:
        if share.name == 'name':
            criar_arquivo_zip(salvar_em, fazer_bkp_de)
            print('Backup realizado com sucesso!')
    conn.close()


def main():
    try:

        dia, data = data_e_dia()

        salvar_em = r'CAMINHO_+_NOMEAQUIVO'.format(data, dia)
        nome_arquivo = str('NOMEAQUIVO-' + dt.now().strftime('%d-%m-%y') + '-12.rar')
        fazer_bkp_de = r"CAMINHO_+_NOMEAQUIVO{}".format(nome_arquivo)
        bkp_servidor(salvar_em, fazer_bkp_de, nome_arquivo)

    except Exception as e:
        print('Erro no programa principal: ' + str(e))


if __name__ == "__main__":
    main()
