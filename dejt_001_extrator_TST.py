# -*- coding: utf-8 -*-
#coding: utf-8
import sys
sys.path.append("..")

import logging
import logging.config
import os
import argparse
import subprocess
from datetime import datetime
from datetime import date
from threading import Thread
import re
import urllib.request
import shutil
import glob
from datetime import datetime
from datetime import date
from datetime import timedelta
from pyvirtualdisplay import Display

import time

from src.webdriver.driversfactory import DriverFactory
from src.util.utilities2 import Utilities

print('inicio')




class start_robo ():

    def __init__ (self):
        # util = Utilities()
        self.util = Utilities(sys.argv[0], os.getpid())
        self.config = self.util.get_config()
        self.veficador_finalizacao=0
        self.erros_gatilho = 0
        self.inicioExecucao = time.time()

        self.hora_de_inicio_processo=datetime.today().strftime("%Y/%m/%d %H:%M:%S")

        ###Dados do Robô
        self.status = "Sucesso"
        self.robo_pid = os.getpid()
        self.robo_nome=self.util.pega_nome_robo(sys.argv[0])

        self.dir_raiz=self.util.pegar_caminho_diretorio_do_arquivo(sys.argv[0])

        self.robo_codigo = '{}_{}'.format(self.robo_nome, self.robo_pid)

        self.robo_descricao = self.config[f'{self.robo_nome}']['descricao']
        self.util.create_robo_header(self.robo_codigo, '{}'.format(self.robo_descricao))



        #### variaveis do config ini
        # self.url = self.config[f'{self.robo_nome}']['url']

        dir = self.config[f'{self.robo_nome}']['dir']
        windir = self.config[f'{self.robo_nome}']['windir']
        url_diario = self.config[f'{self.robo_nome}']['url_diario']
        output = self.config[f'{self.robo_nome}']['output']

        xpath_dropdown_orgao = self.config[f'{self.robo_nome}']['xpath_dropdown_orgao']
        xpath_value_TST = self.config[f'{self.robo_nome}']['xpath_value_TST']
        xpath_input_dataini = self.config[f'{self.robo_nome}']['xpath_input_dataini']
        xpath_input_datafim = self.config[f'{self.robo_nome}']['xpath_input_datafim']
        xpath_button_pesquisar = self.config[f'{self.robo_nome}']['xpath_button_pesquisar']
        xpath_corpo_msg = self.config[f'{self.robo_nome}']['xpath_corpo_msg']
        xpath_linha_TR_resultados = self.config[f'{self.robo_nome}']['xpath_linha_TR_resultados']
        xpath_proxima_pag = self.config[f'{self.robo_nome}']['xpath_proxima_pag']
        xpath_contador_pag = self.config[f'{self.robo_nome}']['xpath_contador_pag']



        self.util.criar_diretorio(f'{dir_html}/{self.robo_nome}')
        self.util.criar_diretorio(f'{dir_html}/{self.robo_nome}/controle')
        self.util.criar_diretorio(f'{dir_html}/{self.robo_nome}/upload')
        self.util.criar_diretorio(f'{dir_html}/{self.robo_nome}/download')
        self.util.criar_diretorio(f'{dir_html}/{dir}/TMP')



        ### Cria logger
        self.log_config=self.config['log']['log_config']
        self.log_file=self.config['log']['log_file']
        self.log_dir = self.config['log']['log_dir']
        self.util.sobrescrever_arquivo(self.log_dir + self.robo_nome + '.pid', '{}'.format(self.robo_pid))

        logging.config.fileConfig(self.log_config)

        self.logger = logging.getLogger('robos.{}'.format(self.robo_codigo))
        self.util.duplica_log_robo(logging,self.logger,self.log_dir,self.robo_nome)


        # Carrega configurações para envio de e-mail em caso de erro
        self.mailer = Mailler_gmail(self.config['log_error_gmail']['email_logger_nome_remetente'],  # Nome do remetente
                               self.config['log_error_gmail']['email_logger_remetente'],  # Email do remetente
                               self.config['log_error_gmail']['email_logger_server'],
                               self.config['log_error_gmail']['email_logger_port'],
                               self.config['log_error_gmail']['email_logger_user'],
                               self.config['log_error_gmail']['email_logger_password'],
                               self.robo_pid)


        #######

        try:
            self.logger.info('Inicia captura de argumentos')
            parser = argparse.ArgumentParser(description='argumentos')
            parser.add_argument('--headless', '-H', dest="arg_headless", type=str, help="headless, True=background or False=Foregrand-grafico", default="True")
            parser.add_argument('--acao', '-a', dest="arg_tipo_acao", type=str, help="tipo acao: bkp", default="")
            # parser.add_argument('--userfile', '-u', dest="arg_usuarios_file", type=str, help="caminho completo para o arquivo de usuarios.csv", default=f'{self.usuarios_csv}')
            args = parser.parse_args()
        except Exception as e:
            self.logger.error(f'ERRO: ao pegar arg parser  {e}')

        try:
            self.tipo_acao=args.arg_tipo_acao
            self.logger.debug(f'arg_headless: {args.arg_headless}')
            if f'{args.arg_headless}' == 'False':
                self.headless = False
            else:
                self.headless = True
            self.logger.info(f'Fim captura de argumentos - self.headless="{self.headless}')
        except Exception as e:
            self.tipo_acao= ''
            self.headless = True
            self.logger.error(f'headless={self.headless} erro {e}')
        self.logger.warning(f'headless={self.headless}')

        try:
            erro = ''
            self.logger.info('Instancia extrator')
            extrator = Extrator(self.headless,
                                self.logger,  # 1
                                self.util,
                                self.mailer,  # 2
                                self.robo_codigo,  # 3
                                self.robo_nome,  # 4
                                self.robo_pid,  # 5
                                self.robo_descricao,  # 6
                                self.log_file,

                                dir,
                                url_login,
                                user,
                                senha,
                                xpath_input_user,
                                xpath_input_senha,
                                xpath_button_login,
                                xpath_primeiro_checkbox,
                                xpath_olho_monitorar,
                                xpath_grafico_barras,
                                xpath_acompanhamento_filas,
                                dir_html,
                                url_html,
                                dir_monitoramento,
                                self.tipo_acao

                                )

            if f'{self.tipo_acao}' == 'bkp':
                extrator.converte_png_to_mp4()
            else:
                extrator.iniciar()


            ciclo_tentativas = 0
            while ciclo_tentativas > 0:
                try:
                    extrator.iniciar()
                except Exception as e:
                    self.logger.error(f'{user}: erro extrator.iniciar():{e}')

                valor_finalizacao = extrator.verifica_fim()
                self.logger.warning(f'{user}: INI ({ciclo_tentativas}) valor_finalizacao={valor_finalizacao}')
                ciclo_tentativas -= 1
                if ciclo_tentativas <= 1 or valor_finalizacao != 0:
                    ciclo_tentativas = 0
                    self.logger.warning(f'{user}: FIM ({ciclo_tentativas}) do iniciar extrator')
                    time.sleep(10)
                else:
                    self.logger.warning(f'{user}: ERROS FIM ({ciclo_tentativas}) do iniciar extrator')


        except Exception as e:
            self.logger.error(f' ERRO: Instancia extrator: {e}')
            erro = e

        exit()


        #####################3









##########################################

start_robo()
