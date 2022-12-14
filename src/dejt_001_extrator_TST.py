# -*- coding: utf-8 -*-
#coding: utf-8
import sys
#sys.path.append("../..")
sys.path.append("../")

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
import xlsxwriter
#import time


#from src.webdriver.driversfactory import DriverFactory
#from src.util.utilities2 import Utilities

from webdriver.driversfactory import DriverFactory
from util.utilities2 import Utilities



from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from pyvirtualdisplay import Display
from anticaptchaofficial.imagecaptcha import *
import pandas as pd
import random
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver import ActionChains
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
from datetime import date
from datetime import timedelta
from datetime import time
import time as ttime

from tika import parser


print('inicio')




class start_robo ():

    def __init__ (self):

        self.erro_final = 'ERRO_DESCONHECIDO_001'
        # util = Utilities()
        self.util = Utilities(sys.argv[0], os.getpid(), test_config_dir_direto=True)
        self.config = self.util.get_config()
        self.veficador_finalizacao=0
        self.erros_gatilho = 0
        self.inicioExecucao = time()

        agora=datetime.today()
        self.hora_de_inicio_processo=agora.strftime("%Y/%m/%d %H:%M:%S")


        ###Dados do Rob??
        self.status = "Sucesso"
        self.robo_pid = os.getpid()
        self.robo_nome=self.util.pega_nome_robo(sys.argv[0])

        self.dir_raiz=self.util.pegar_caminho_diretorio_do_arquivo(sys.argv[0])
        #print(self.dir_raiz)

        self.robo_codigo = '{}_{}'.format(self.robo_nome, self.robo_pid)

        self.robo_descricao = self.config[f'{self.robo_nome}']['descricao']
        self.util.create_robo_header(self.robo_codigo, '{}'.format(self.robo_descricao))

        self.log_config = os.path.abspath(self.config['log']['log_config'])
        self.log_file = os.path.abspath(self.config['log']['log_file'])
        self.log_dir = os.path.abspath(self.config['log']['log_dir'])
        self.util.criar_diretorio(self.log_dir)

        self.util.sobrescrever_arquivo(self.log_dir + '/' + self.robo_nome + '.pid', '{}'.format(self.robo_pid))
        logging.config.fileConfig(self.log_config)
        self.logger = logging.getLogger('robos.{}'.format(self.robo_codigo))
        self.util.duplica_log_robo(logging, self.logger, self.log_dir, self.robo_nome)


        #### variaveis do config ini
        # self.url = self.config[f'{self.robo_nome}']['url']

        #windir = self.dir_raiz + '/' + self.config[f'{self.robo_nome}']['windir']
        #dir = self.dir_raiz + '/' + self.config[f'{self.robo_nome}']['dir']
        #output = self.dir_raiz + '/' + self.config[f'{self.robo_nome}']['output']

        windir = os.path.abspath(self.config[f'{self.robo_nome}']['windir'])
        self.dir = os.path.abspath(self.config[f'{self.robo_nome}']['dir'])
        self.dir_download = os.path.abspath(self.dir + '/Downloads')
        self.output = os.path.abspath(self.config[f'{self.robo_nome}']['output'] + '/extracao_de_' + agora.strftime("%d-%m-%Y_%Hh%M"))


        self.url_diario = self.config[f'{self.robo_nome}']['url_diario']
        self.xpath_dropdown_orgao = self.config[f'{self.robo_nome}']['xpath_dropdown_orgao']
        self.xpath_value_TST = self.config[f'{self.robo_nome}']['xpath_value_TST']
        self.xpath_input_dataini = self.config[f'{self.robo_nome}']['xpath_input_dataini']
        self.xpath_input_datafim = self.config[f'{self.robo_nome}']['xpath_input_datafim']
        self.xpath_button_pesquisar = self.config[f'{self.robo_nome}']['xpath_button_pesquisar']
        self.xpath_corpo_msg = self.config[f'{self.robo_nome}']['xpath_corpo_msg']
        self.xpath_linha_TR_resultados = self.config[f'{self.robo_nome}']['xpath_linha_TR_resultados']
        self.xpath_proxima_pag = self.config[f'{self.robo_nome}']['xpath_proxima_pag']
        self.xpath_contador_pag = self.config[f'{self.robo_nome}']['xpath_contador_pag']
        self.xpath_legenda = self.config[f'{self.robo_nome}']['xpath_legenda']

        self.util.criar_diretorio(self.dir)
        self.util.limpar_diretorio(self.dir)


        self.util.criar_diretorio(self.dir_download)
        self.util.limpar_diretorio(self.dir_download)


        self.util.criar_diretorio(self.output)






        try:
            self.logger.info('Inicia captura de argumentos')
            parser = argparse.ArgumentParser(description='argumentos')
            parser.add_argument('--headless', '-H', dest="arg_headless", type=str, help="headless, True=background or False=Foregrand-grafico", default="True")
            #parser.add_argument('--acao', '-a', dest="arg_tipo_acao", type=str, help="tipo acao: bkp", default="")
            # parser.add_argument('--userfile', '-u', dest="arg_usuarios_file", type=str, help="caminho completo para o arquivo de usuarios.csv", default=f'{self.usuarios_csv}')
            args = parser.parse_args()
        except Exception as e:
            self.logger.error(f'ERRO: ao pegar arg parser  {e}')

        try:
            #self.tipo_acao=args.arg_tipo_acao
            self.logger.debug(f'arg_headless: {args.arg_headless}')
            if f'{args.arg_headless}' == 'False':
                self.headless = False
            else:
                self.headless = True
            self.logger.info(f'Fim captura de argumentos - self.headless="{self.headless}')
        except Exception as e:
           # self.tipo_acao= ''
            self.headless = True
            self.logger.error(f'headless={self.headless} erro {e}')
        self.logger.warning(f'headless={self.headless}')


        try:
            print('\n\n\n\n')
            self.logger.info('Iniciando extra????o')
            #self.headless=False

            self.navegacao()


            #list_files=[['20/10/2022', 'Edi????o 3583/2022 - Caderno do Tribunal Superior do Trabalho - Judici??rio', 'TMP/dejt_extrator_TST/2_Edicao_35832022__Caderno_do_Tribunal_Superior_do_Trabalho__Judiciario____Diario_3583__20_10_2022.pdf.pdf'],['21/10/2022', 'Edi????o 3584/2022 - Caderno do Tribunal Superior do Trabalho - Judici??rio', 'TMP/dejt_extrator_TST/1_Edicao_35842022__Caderno_do_Tribunal_Superior_do_Trabalho__Judiciario____Diario_3584__21_10_2022.pdf.pdf']]

            #self.leitor_pdf(list_files)


        except Exception as e:
            self.logger.info(f'ERRO na extra????o: {e}')
            self.erro_final = 'ERRO_NAVEGADOR_002'


    def forca_fechar(self):
        try:
            self.logger.info(f'For??ando fechar webdriver, caso tenha ficado aberto. Certo que dar?? um exception')
            self.util.saindo_driver(self.driver, self.logger)
        except Exception as e:
            self.logger.warning(f'alerta esperado alerta Normal For??ando fechar webdriver: {e}')

    def navegacao(self):
        try:
            #self.forca_fechar()
            #dir_download = os.path.abspath(f'{self.dir_raiz}/{self.dir_download}')
            dir_download = os.path.abspath(f'{self.dir_download}')
            driverfactory = DriverFactory()
            ############                                                                                             A     L
            self.driver = driverfactory.create_driver('chrome', self.headless, dir_download, False, 900, 600)
            self.driver.set_page_load_timeout(240)
            self.driver.implicitly_wait(15)

            self.pesquisar_TST()
            #self.forca_fechar()

        except Exception as e:
            #TODO: fazer um retry x3 para esse erro
            # Message: unknown error: net::ERR_NAME_NOT_RESOLVED

            
            err = f'{e}'.replace(';', ' ').replace('\n', ' ')
            self.logger.error(f'ERRO ao iniciar navega????o: {err}')
            self.forca_fechar()

    def pesquisar_TST(self):
        try:
            print('\n')
            #N_DAYS_AGO = 5
            #today = datetime.now()
            #n_days_ago = today - timedelta(days=N_DAYS_AGO)
            #print today, n_days_ago

            hoje = datetime.today()
            #data_hoje = datetime.today().strftime("%d/%m/%Y")
            data_hoje = hoje.strftime("%d/%m/%Y")

            ontem = hoje - timedelta(days=1)
            #ontem = hoje - timedelta(days=5)
            data_ontem = ontem.strftime("%d/%m/%Y")
            semana_passada = ontem - timedelta(days=7)
            #semana_passada = ontem - timedelta(days=0)
            #semana_passada = ontem - timedelta(days=2)
            data_semana_passada = semana_passada.strftime("%d/%m/%Y")


            self.logger.info(f'abrindo url {self.url_diario}')
            #ttime.sleep(3)
            self.driver.get(self.url_diario)
            ttime.sleep(1)
            self.logger.info(f'procurando xpath_dropdown_orgao')
            xpath_dropdown_orgao = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, f'{self.xpath_dropdown_orgao}')))
            self.logger.info(f'vai clicar xpath_dropdown_orgao')
            xpath_dropdown_orgao.click()
            #ttime.sleep(1)
            self.logger.info(f'procurando xpath_value_TST')
            xpath_value_TST = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, f'{self.xpath_value_TST}')))
            self.logger.info(f'vai clicar xpath_value_TST')
            xpath_value_TST.click()
            #ttime.sleep(1)

            self.logger.info(f'procurando xpath_input_dataini')
            xpath_input_dataini = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, f'{self.xpath_input_dataini}')))
            self.logger.info(f'vai colocando dataini={data_semana_passada}')
            xpath_input_dataini.clear()
            #ttime.sleep(1)
            #xpath_input_dataini.send_keys('17/10/2022')
            xpath_input_dataini.send_keys(f'{data_semana_passada}')
            #ttime.sleep(1)


            self.logger.info(f'procurando xpath_input_datafim')
            xpath_input_datafim = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, f'{self.xpath_input_datafim}')))
            self.logger.info(f'colocando datafim={data_ontem}')
            xpath_input_datafim.clear()
            #ttime.sleep(1)
            #xpath_input_datafim.send_keys('24/10/2022')
            xpath_input_datafim.send_keys(f'{data_ontem}')
            #ttime.sleep(3)






            self.logger.info(f'procurando xpath_button_pesquisar')
            xpath_button_pesquisar = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, f'{self.xpath_button_pesquisar}')))
            self.logger.info(f'vai clicar xpath_button_pesquisar')
            xpath_button_pesquisar.click()
            ttime.sleep(1)
            xpath_corpo_msg = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, f'{self.xpath_corpo_msg}')))
            #self.logger.info(f'Retorno: -1--{xpath_corpo_msg.text}--')
            if f'{xpath_corpo_msg.text}' == '':
                self.logger.info(f'sem erros "{xpath_corpo_msg.text}"')

                self.logger.info(f'testando integridade do reload da pagina')
                xpath_legenda = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, f'{self.xpath_legenda}')))
                self.logger.info(f'localizado ok: {xpath_legenda.text}')
                print('\n')
                self.download_cadernos()
                #self.forca_fechar()

            else:
                #algum erro
                self.logger.info(f'ERRO no Retorno: {xpath_corpo_msg.text}')
                self.erro_final=xpath_corpo_msg.text

            #ttime.sleep(10)

            print('\n')

        except Exception as e:
            self.logger.error(f'ERRO ao abrir url {self.url_diario}:  {e}')
            self.forca_fechar()



    def download_cadernos(self):
        print('\n')
        list_files = []

        try:
            self.logger.info('iniciando procedimento de download dos cadernos')

            self.logger.info('localizando total de paginas do site xpath_contador_pag')
            xpath_contador_pag = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, f'{self.xpath_contador_pag}')))
            self.logger.info(f'total de p??ginas xpath_contador_pag para extra????o = {xpath_contador_pag.text}')

            xpath_linha_TR_resultados = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, f'{self.xpath_linha_TR_resultados}')))

            #list_xpath_linha_TR_resultados = self.driver.find_elements_by_xpath(f'{self.xpath_linha_TR_resultados}')
            #list_xpath_linha_TR_resultados = self.driver.find_element("xpath", f'{self.xpath_linha_TR_resultados}')

            list_xpath_linha_TR_resultados = self.driver.find_elements(by=By.XPATH, value=f'{self.xpath_linha_TR_resultados}')


            #print(f'list_xpath_linha_TR_resultados = {list_xpath_linha_TR_resultados}')

            qtde_tr = len(list_xpath_linha_TR_resultados)

            self.logger.debug(f'qtde_tr = {qtde_tr}')
            counter_tr = 1
            for linha_tr in list_xpath_linha_TR_resultados:
                date_file = []
                data = self.driver.find_element(by=By.XPATH, value=f'({self.xpath_linha_TR_resultados})[{counter_tr}]/td[1]').text.strip(' ').strip('\n').strip(' ')
                titulo = self.driver.find_element(by=By.XPATH, value=f'({self.xpath_linha_TR_resultados})[{counter_tr}]/td[2]').text.strip(' ').strip('\n').strip(' ')
                link = self.driver.find_element(by=By.XPATH, value=f'({self.xpath_linha_TR_resultados})[{counter_tr}]/td[3]')
                self.logger.debug(f'Baixando pdf da linha {counter_tr} = {data} | {titulo}')
                link.click()
                #ttime.sleep(5)

                arq_baixado = self.util.wait_for_downloads(self.dir_download,460, 1)
                #ttime.sleep(1)
                nome_arq_baixado = self.util.pegar_nome_arquivo(arq_baixado)
                ext_arq = f'{arq_baixado}'.split('.')[-1]
                titulo_edit = self.util.somente_letras_numeros_espaco_ponto(self.util.removedor_acentuacao(f'{titulo}')).replace(" ","_")
                novo_nome=f'{self.dir}/{counter_tr}_{titulo_edit}____{nome_arq_baixado}.{ext_arq}'
                self.util.mover_arquivo(arq_baixado, novo_nome)
                #ttime.sleep(1)
                date_file.append(f'{data}')
                date_file.append(f'{titulo}')
                date_file.append(f'{novo_nome}')

                list_files.append(date_file)

                #self.logger.debug(f'varrendo linha {counter_tr} = {linha_tr.text}')

                counter_tr += 1


            #ttime.sleep(20)

            self.forca_fechar()
            self.leitor_pdf(list_files)

        except Exception as e:
            self.logger.error(f'ERRO ao baixar cadernos:  {e}')


    def leitor_pdf(self, list_files):
        try:
            self.logger.info(f'iniciando leitura de PDFs')
            #lista_controle = []
            lista_csv = []

            self.util.agregar_arquivo(self.output + f'/TST_Relatorio.csv', f'data;titulo;qtde_processos;arquivo')
            #self.util.agregar_arquivo(self.output + f'/TST_Relatorio.csv', f'data;titulo;qtde_processos;arquivo')
            #self.util.agregar_arquivo(self.output + f'/TST_Relatorio.csv', f'data;titulo;qtde_processos;arquivo')
            #self.util.agregar_arquivo(self.output + f'/TST_Relatorio.csv', f'data;titulo;qtde_processos;arquivo')
            #self.util.agregar_arquivo(self.output + f'/TST_Relatorio.csv', f'data;titulo;qtde_processos;arquivo')


            counter=0
            qtde=len(list_files)
            #counter = 100
            while counter < qtde:
                print('\n')
                #self.logger.info(f'lendo PDF ({counter}): {list_files[counter]}')
                data=list_files[counter][0]
                data_und = f'{data}'.replace('/','-')
                titulo=list_files[counter][1]
                arquivo=list_files[counter][2]
                #print(f'         data: {data}')
                #print(f'       titulo: {titulo}')
                #print(f'      arquivo: {arquivo}')
                self.logger.info(f'Iniciando PDF {counter + 1} de {qtde}: {data};{titulo}')
                self.logger.warning(f'Por favor, tenha paci??ncia, demora um pouquinho quando o PDF ?? grande!!')
                print('\n\n\n\n')
                #headers = {"X-Tika-OCRLanguage": "eng", "X-Tika-OCRTimeout": "300"}
                #text_tika = parser.from_file(doc, xmlContent=False, requestOptions={'headers': headers, 'timeout': 300})

                #raw = parser.from_file(f'{arquivo}')
                
                headers = {"X-Tika-OCRTimeout": "900"}
                raw = parser.from_file(f'{arquivo}', requestOptions={'headers': headers, 'timeout': 900})
                #raw = ['\nProcesso N?? 09\n']

                #raw ="{'metadata': {'Content-Type': 'application/pdf', 'Creation-Date': '2022-10-21T20:32:40Z', 'Last-Modified': '2022-10-21T20:33:04Z', 'Last-Save-Date': '2022-10-21T20:33:04Z', 'X-Parsed-By': ['org.apache.tika.parser.DefaultParser', 'org.apache.tika.parser.pdf.PDFParser'], 'X-TIKA:content_handler': 'ToTextContentHandler', 'X-TIKA:embedded_depth': '0', 'X-TIKA:parse_time_millis': '14929', 'access_permission:assemble_document': 'true', 'access_permission:can_modify': 'true', 'access_permission:can_print': 'true', 'access_permission:can_print_degraded': 'true', 'access_permission:extract_content': 'true', 'access_permission:extract_for_accessibility': 'true', 'access_permission:fill_in_form': 'true', 'access_permission:modify_annotations': 'true', 'created': '2022-10-21T20:32:40Z', 'date': '2022-10-21T20:33:04Z', 'dc:format': 'application/pdf; version=1.4', 'dcterms:created': '2022-10-21T20:32:40Z', 'dcterms:modified': '2022-10-21T20:33:04Z', 'hasSignature': 'true', 'meta:creation-date': '2022-10-21T20:32:40Z', 'meta:save-date': '2022-10-21T20:33:04Z', 'modified': '2022-10-21T20:33:04Z', 'pdf:PDFVersion': '1.4', 'pdf:charsPerPage': ['2724', '1384'], 'pdf:docinfo:created': '2022-10-21T20:32:40Z', 'pdf:docinfo:modified': '2022-10-21T20:33:04Z', 'pdf:docinfo:producer': 'iText 2.0.7 (by lowagie.com); modified using iText?? 5.2.1 ??2000-2012 1T3XT BVBA', 'pdf:encrypted': 'false', 'pdf:hasAcroFormFields': 'true', 'pdf:hasMarkedContent': 'false', 'pdf:hasXFA': 'false', 'pdf:hasXMP': 'false', 'pdf:unmappedUnicodeCharsPerPage': ['0','0'], 'producer': 'iText 2.0.7 (by lowagie.com); modified using iText?? 5.2.1 ??2000-2012 1T3XT BVBA', 'xmpTPg:NPages': '1718'}, 'content': '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n \n\n968000148\n\n\n\nProcesso N?? 09\n\n\n', 'status': 200}"
                #raw ="{'content': '\n\n968000148\n\n\n\nProcesso N?? 09\n\n\n', 'status': 200}"


                #print(f'raw:\n\n\n{raw}\n\n\n')

                #processos = re.findall(r'^Processo N??.*.[0-9]$', raw['content'])
                processosN = re.findall(r'\nProcesso N??.*.[0-9]\n', raw['content'])
                processos = [s.replace('\n','') for s in processosN]


                qtde_process=len(processos)
                #print(f'processos: {processos}')
                #self.logger.info(f'{data};{titulo}: localizado {qtde_process} processos')

                #print(f'total: {len(processos)}')

                #self.escreve_saida(processos, data, titulo)

                processos_texto = self.util.converte_lista_para_texto(processos, '\n')
                self.util.agregar_arquivo(self.output+f'/TST_{data_und}.csv',processos_texto)

                #lista_controle.append(f'{data};{titulo};{qtde_process};{arquivo}')

                self.util.agregar_arquivo(self.output+f'/TST_Relatorio.csv',f'{data};{titulo};{qtde_process};{arquivo}')


                lista_csv.append(self.output+f'/TST_{data_und}.csv')

                #print(f'processos_texto:{processos_texto}')


                #self.escreve_saida(processos, data, titulo)

                #for item in self.progressBar(self.escreve_saida(processos,data,titulo), prefix='Progress:', suffix='Complete', length=50):
                #    # Do stuff...
                #    ttime.sleep(0.1)
                #df = pd.read_csv(f'{self.dir_output_csv}/{nome_arquivo_final}.csv', sep=',', decimal='.', encoding='iso-8859-1')


                #df1.to_csv(f'{self.dir_output_final_padrao_DAVI}/{novo_nome}.csv', sep=',', index=False)


                self.util.sobrescrever_arquivo(arquivo+'.txt', raw['content'])
                #print(f'acabou arquivo: {arquivo}')
                self.logger.info(f'Finalizado PDF {counter + 1} de {qtde} com {qtde_process} processos: {data};{titulo} ')
                print('\n')

                counter += 1
                #ttime.sleep(10)

            df = pd.read_csv(self.output+f'/TST_Relatorio.csv', sep=';', encoding='utf-8')
            #headers = ["Processos"]
            #df.columns = headers

            #xls = f'{csv}'.replace('.csv', '.xls')
            #print(f'xls: {xls}')
            df.to_excel(self.output+f'/TST_Relatorio.xlsx', index=False, sheet_name='Relatorio')

            #self.util.auto_ajuste_largura_excel(self.output+f'/TST_Relatorio.xlsx', 'Relatorio')

            os.remove(self.output+f'/TST_Relatorio.csv')

            self.converte_csv_xls(lista_csv)
            print('\n')
        except Exception as e:
            self.logger.error(f'ERRO ao ler os PDFs baixados:  {e}')
            #TODO: mapear os erro
            # <urlopen error [Errno -3] Temporary failure in name resolution>



    def converte_csv_xls(self,lista_csv):
        print('\n')
        #mylist = ["a", "b", "a", "c", "c"]
        #mylist = list(dict.fromkeys(mylist))
        #print(mylist)

        lista_csv = list(dict.fromkeys(lista_csv))



        #print(f'lista_csv: {lista_csv}')

        for csv in lista_csv:
            #print(f'csv: {csv}')
            #df = pd.read_csv(f'{csv}', sep=';', decimal='.', encoding='utf-8')
            df = pd.read_csv(f'{csv}', sep=';',  encoding='utf-8')
            headers = ["Processos"]
            df.columns = headers

            xls = f'{csv}'.replace('.csv','.xlsx')
            self.logger.info(f'Gerando xlsx: {xls}')
            df.to_excel(f'{xls}', index=False, sheet_name='Processos')

            #self.util.auto_ajuste_largura_excel(xls, 'Processos')

            os.remove(f'{csv}')
            print('\n')


    def escreve_saida(self, processos, data, titulo):
        for procss in processos:
            #                    print(f'procss: {procss}')
            proc = f'{procss}'.strip('\n')
            self.util.agregar_arquivo(self.dir + 'saida.txt', f'{data};{titulo};{proc}')

    def progressBar(iterable, prefix='', suffix='', decimals=1, length=100, fill='???', printEnd="\r"):
        """
        Call in a loop to create terminal progress bar
        @params:
            iterable    - Required  : iterable object (Iterable)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        """
        total = len(iterable)

        # Progress Bar Printing Function
        def printProgressBar(iteration):
            percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
            filledLength = int(length * iteration // total)
            bar = fill * filledLength + '-' * (length - filledLength)
            print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)

        # Initial Call
        printProgressBar(0)
        # Update Progress Bar
        for i, item in enumerate(iterable):
            yield item
            printProgressBar(i + 1)
        # Print New Line on Complete
        print()

    def xxxxxx(self):
        ### Cria logger
        self.log_config=self.config['log']['log_config']
        self.log_file=self.config['log']['log_file']
        self.log_dir = self.config['log']['log_dir']
        self.util.sobrescrever_arquivo(self.log_dir + '/'  + self.robo_nome + '.pid', '{}'.format(self.robo_pid))

        logging.config.fileConfig(self.log_config)

        self.logger = logging.getLogger('robos.{}'.format(self.robo_codigo))
        self.util.duplica_log_robo(logging,self.logger,self.log_dir,self.robo_nome)


        # Carrega configura????es para envio de e-mail em caso de erro
        self.mailer = Mailler_gmail(self.config['log_error_gmail']['email_logger_nome_remetente'],  # Nome do remetente
                               self.config['log_error_gmail']['email_logger_remetente'],  # Email do remetente
                               self.config['log_error_gmail']['email_logger_server'],
                               self.config['log_error_gmail']['email_logger_port'],
                               self.config['log_error_gmail']['email_logger_user'],
                               self.config['log_error_gmail']['email_logger_password'],
                               self.robo_pid)


        #######



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

print('\n\n\n\n\n\n\n\n')
print('        #########################################################')
print('        ###                                                   ###')
print('        ##                 Extrator finalizado                 ##')
print('        ###                                                   ###')
print('        #########################################################')
print('\n\n\n\n')
ttime.sleep(40)
print('\n\n\n\n')