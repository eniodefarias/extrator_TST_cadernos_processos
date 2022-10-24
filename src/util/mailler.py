# -*- coding: utf-8 -*-
#coding: utf-8

import smtplib
from smtplib import SMTPException
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from mimetypes import guess_type
from email import encoders
import os
from os.path import basename
import time
import logging
import logging
import logging.config
import re
import socket
import sys
sys.path.append("..")
import inspect
# from Engine.util.utilities import Utilities
from Engine.util.utilities2 import Utilities
#import datetime
from datetime import datetime
#from datetime import *
from datetime import datetime
from datetime import date
from datetime import timedelta
import os.path
import socket


class Mailler_gmail():

    def __init__(self, remetente_nome, remetente, servidor, port, username=None, password=None, pid=None, bkp_user_senha=''):
        # def __init__(self, remetente_nome, remetente, servidor, port, username, password,pid):
        print('\n')

        print('carregando dados do email')
        self.bkp_user_senha=bkp_user_senha
        self.remetente_nome = remetente_nome
        self.remetente = remetente
        self.servidor = servidor
        self.porta = port

        self.usuario_exclusivo = username
        self.senha_exclusivo = password

        print(f'self.remetente_nome = {self.remetente_nome}')
        print(f'self.remetente = {self.remetente}')
        print(f'self.servidor = {self.servidor}')
        print(f'self.porta = {self.porta}')
        print(f'username = {username}')
        print(f'password = {password}')
        print(f'pid = {pid}')

        ###############################################################################################
        # esta gambiarra, alterna em hardcode os emails:   sistema.retentiva   e   sistema.retentiva.01
        # então mantenha sempre a senha dos dois emails sempre iguais Retentiva!2019

        now = datetime.now()
        print(f'now = {now}')
        # hora_atual = int(format(int(now.hour), "01d"))


        hora_atual = int(format(int(now.day), "01d"))
        print(f'hora_atual = {hora_atual}')
        resto = hora_atual % 2

        # self.usexrname = usernxame
        # print(f'self.usexrname = {self.userxname}')
        # self.password = password
        # print(f'self.password = {self.password}')
        # if resto == 0:
        #     print('Número é par')
        #     #self.usexrname = username
        #     self.usernaxme = username
        # else:
        #     print('Número é impar')
        #     self.userxname = f"{username}.01"
        #     #self.usernxame = f"{username}.01"

        #
        ###############################################################################################



        #self.usxername = userxname





        # print(f' dentro mailler:   self.usernxame={self.usernxame}    -    self.password={self.password}')
        time.sleep(1)

        robo_pid = pid  # sempre colocar na função, mesmo que em branco '', mas o melhor é se colocar mesmo, mas caso não coloque não vai prejudicar.

        # util = Utilities()

        util = Utilities(sys.argv[0], os.getpid())
        self.util=util
        config = util.get_config()
        self.config = config

        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        filename = module.__file__

        robo_nome=util.pega_nome_robo(filename)
        robo_codigo = '{}_{}'.format(robo_nome,robo_pid)





        ### Cria logger
        log_config=config['log']['log_config']
        log_file=config['log']['log_file']
        log_dir = config['log']['log_dir']
        logging.config.fileConfig(log_config)
        self.logger = logging.getLogger('robos.{}'.format(robo_codigo))
        util.duplica_log_robo(logging,self.logger,log_dir,robo_nome)



        ####################################
        ################################
        self.erros_envios_usuario_exclusivo = 0
        self.pega_user_senha()

        ################################
        ####################################





        self.email_cco_default=config['log_error_gmail']['email_cco_default']


        self.logger.info('Iniciando carteiro gmail ' + remetente_nome + ' ' + remetente)







    def __del__(self):
        self.logger.info('Carteiro gmail {} - {} - finalizado'.format(self.remetente_nome, self.remetente))

    def pega_user_senha(self):

        if f'{self.bkp_user_senha}' == '':
            self.user_senha = self.config['log_error_gmail']['user_senha']
        else:
            self.user_senha = self.bkp_user_senha

        self.dir_emails = self.config['log_error_gmail']['dir_emails']
        self.util.criar_diretorio(self.dir_emails)
        lista_user_senha = self.user_senha.split('|')
        comp_lista_user_senha = len(lista_user_senha)
        self.logger.info(f'lista_user_senha={lista_user_senha}')
        self.logger.info(f'comp_lista_user_senha={comp_lista_user_senha}')

        try:
            self.logger.info(f'lendo verificar arquivo {self.dir_emails}/count.txt')
            leitura_count = int(self.util.somente_numeros(self.util.ler_primeira_linha_arquivo(f'{self.dir_emails}/count.txt')))
            self.logger.info(f'try leitura_count={leitura_count}')
        except Exception as e:
            self.logger.error(f'ERROr ao verificar arquivo {self.dir_emails}/count.txt :   {e}')
            self.util.sobrescrever_arquivo(f'{self.dir_emails}/count.txt', '0')
            leitura_count = 0
            self.logger.info(f'except leitura_count={leitura_count}')

        if leitura_count >= comp_lista_user_senha:
            self.util.sobrescrever_arquivo(f'{self.dir_emails}/count.txt', '0')
            leitura_count = 0
            self.logger.info(f'if leitura_count={leitura_count} ZERO')

        self.logger.info(f'fora leitura_count={leitura_count}')

        print('\n\n-------------------\n\n')

        if self.erros_envios_usuario_exclusivo > 1 or  f'{self.usuario_exclusivo}' == '' or f'{self.senha_exclusivo}' == '' :

            self.username = lista_user_senha[leitura_count].split(';')[0]
            self.logger.debug(f'self.username = {self.username}')
            self.password = lista_user_senha[leitura_count].split(';')[1]
            self.logger.debug(f'self.password = {self.password}')
            self.logger.info(f'atual leitura_count={leitura_count}')
            leitura_count += 1
            self.util.sobrescrever_arquivo(f'{self.dir_emails}/count.txt', f'{leitura_count}')
            self.logger.info(f'+1 fim leitura_count={leitura_count}')
            self.logger.warning(f' fazendo envio com user e senha de rodizio: {self.username} e {self.password}')
            self.logger.info(f'self.erros_envios_usuario_exclusivo = {self.erros_envios_usuario_exclusivo}')

        else:
            self.logger.warning(f' tentando envio com usuer e senha exclusivos: {self.usuario_exclusivo} e {self.senha_exclusivo}')
            self.logger.info(f'self.erros_envios_usuario_exclusivo = {self.erros_envios_usuario_exclusivo}')
            self.username = self.usuario_exclusivo
            self.password = self.senha_exclusivo


        print('\n\n-------------------\n\n')

        time.sleep(7)


    def template_html(self, titulo, corpo, assinatura):  # todos os campos aceitam tags htmls

        #titulo = titulo.replace('\n', '<br>')  # titulo do header do body
        #corpo = corpo.replace('\n', '<br>')  # o conteudo do body
        #assinatura = assinatura.replace('\n', '<br>')  # assintura
        self.logger.info('criando template {} - {}'.format(titulo, assinatura))
        self.html = '''
            <!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN" "http://www.w3.org/TR/REC-html40/loose.dtd">
            <html>
            <head><meta name="viewport" content="width=device-width, initial-scale=1.0"><meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                <title>Retentiva</title>
                <style type="text/css">.ak-content { margin: auto; background-color: #FFFFFF; }
            .ak-content a { color: #22224D; }
            .ak-container { width: 100%; }
            .ak-content table tr td { font-family: arial, helvetica, sans-serif; font-size: 16px; color: #4A423C; }
            .ak-button { border-radius: 3px; background-color: #6DC6DD; border-collapse: separate !important; }
            .ak-button tr td { padding: 10px; }
            .ak-button a { text-decoration: none; color: #FFFFFF; font-size: 18px; }
            .ak-line { border-top: 1px solid #CCCCCC; }
            .ak-box { border: 1px solid #CCCCCC; }
            img { border: 0px none; }
            .ak-content-assinatura { padding: 0px 25px 25px; background-color: #FFFFFF; }
            .ak-footer { color: #4A423C; font-size: 13px; border-top: 1px solid #DADADA; }
            .ak-footer td { padding: 20px 25px; }
            .ak-product h5 { margin: 0px; font-weight: normal; }
            .ak-product h2 { margin: 0px; }
            .ak-column-left img { max-width: 100% !important; }
            .ak-column-right img { max-width: 100% !important; }
            @media only screen and (max-width: 750px) {
              .ak-content { width: 100% !important; min-width: 100% !important; }
            }
            @media only screen and (max-width: 450px) {
              body, table, td, a, li, blockquote { margin: 0px; }
              table { border-collapse: collapse; table-layout: fixed; min-width: 100% !important; }
              .layout-email { width: 100% !important; }
              .ak-content { font-size: 18px; }
              .ak-button { max-width: 100% !important; min-width: auto !important; }
              .ak-button a { font-size: 18px; display: block !important; }
              .ak-image { max-width: 100% !important; }
              #ak-columns { width: 100% !important; min-width: 100% !important; }
              .ak-column-container { clear: both; margin-bottom: 30px; width: 100% !important; min-width: 100% !important; margin-left: 0px !important; }
              .ak-column-container:last-child { margin-bottom: 0px; }
              .ak-column-left { line-height: 100% !important; }
              .ak-column-right { line-height: 100% !important; }
              .ak-product td { height: auto; }
              .ak-logo { height: auto; max-width: 100% !important; width: 100% !important; }
              .ak-logo td { padding: 25px; }
              .ak-footer td { font-size: 16px !important; }
              .ak-email-button { width: 100%; }
            }
            .my-content td { padding: 20px; }
            .my-content-assinatura td { padding: 20px; }
                </style>
            </head>
            <body tcap-name="framey0">
            <table cellpadding="0" cellspacing="0" class="ak-container" style="width: 100%;" width="100%">
                <tbody>
                    <tr>
                        <td>
                        <table align="center" cellpadding="0" cellspacing="0" class="ak-content" style="background-color: #FFFFFF; margin: auto;-moz-border-radius: 10px 10px 0 0;-moz-border-radius: 10px 10px 0 0;border-radius: 10px 10px 0 0;" widthxx="900">
                            <tbody>
                                <tr>
                                    <td>
                                    <table border="0" cellpadding="0" cellspacing="0" style="background-color: #51596B;" width="100%">
                                        <tbody>
                                            <tr>
                                                <td style="color: #4A423C; font-family: arial, helvetica, sans-serif; font-size: 16px; padding: 10px 0px;">
                                                <div style="color:#ffffff;text-shadow:2px 1px #4a5f7c;text-align: center;font-size:calc(18px + 0.8vw);"><span style="color:#ffffff;"><span style="font-size:22px;font-size:calc(18px + 0.8vw);"><span style="font-family:Tahoma,Geneva,sans-serif;"><strong>
                                                <!-- titulo -->''' + titulo + '''</strong></span></span></span></div>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>

                                    <table border="0" cellpadding="0" cellspacing="0" style="background-color: #EBF0F5;" width="100%">
                                        <tbody>
                                            <tr>
                                                <td style="color: #4A423C; font-family: arial, helvetica, sans-serif; font-size: 16px; padding: 30px 20px;">
                                                <div style="color:#2F3958;">
                                                    <!-- corpo -->''' + corpo + '''</div>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>

                                    <!--<table border="0" cellpadding="0" cellspacing="0" style="background-color: #A7B5C4;" width="100%">-->
                                    <table border="0" cellpadding="0" cellspacing="0" style="background-color: #6b7887;" width="100%">
                                        <tbody>
                                            <tr>
                                                <td style="color: #4A423C; font-family: arial, helvetica, sans-serif; font-size: 16px; padding: 5px 20px;">
                                                <div style="color: white; text-align: center;">
                                                    <!-- assinatura -->''' + assinatura + '''</div>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>

                                    <table border="0" cellpadding="0" cellspacing="0" style="background-color: #f7f8f9;" width="100%">
                                        <tbody>
                                            <tr>
                                                <td style="color: #4A423C; font-family: arial, helvetica, sans-serif; font-size: 0px; text-align: center; padding: 20px;"><img ak:edit="image" alt="Retentiva" class="ak-image" src="https://fontespromotora.com.br/EMPRESA/retentiva.com.br/img/retentiva.png" style="border: 0px none; width: 160px; max-width: 160px;" width="160" /></td>
                                            </tr>
                                        </tbody>
                                    </table>

                                    <table border="0" cellpadding="0" cellspacing="0" style="background-color: #51596B;" width="100%">
                                        <tbody>
                                            <tr>
                                                <td style="color: #4A423C; font-family: arial, helvetica, sans-serif; font-size: 16px; padding: 5px 2px;-moz-border-radius:  0 0 10px 10px;-moz-border-radius:  0 0 10px 10px;border-radius:  0 0 10px 10px;">
                                                <center>&nbsp; <a href="https://retentiva.com.br/" style="color: #22224D; padding: 10px;" target="_blank" title=""><img alt="" border="0" src="https://fontespromotora.com.br/marketing/emkt/informativos/etc/logo/site.png" style="border: 0px none; max-width: 20px;" /></a> &nbsp; <a href="https://www.instagram.com/retentivacontactcenter/" style="color: #22224D; padding: 10px;" target="_blank" title=""><img alt="" border="0" src="https://fontespromotora.com.br/marketing/emkt/informativos/etc/logo/instagram.png" style="border: 0px none; max-width: 20px;" /></a> &nbsp; <a href="https://www.facebook.com/retentivacontactcenter/" style="color: #22224D; padding: 10px;" target="_blank" title=""><img alt="" border="0" src="https://fontespromotora.com.br/marketing/emkt/informativos/etc/logo/facebook.png" style="border: 0px none; max-width: 20px;" /></a> &nbsp;</center>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        </td>
                    </tr>
                </tbody>
            </table><div style="font-size: 8px;">'''+socket.gethostname()+'''</div>
            </body>
            </html>
        '''


        return self.html

    def template_html_fontes(self, titulo, corpo, assinatura):  # todos os campos aceitam tags htmls

        # titulo = titulo.replace('\n', '<br>')  # titulo do header do body
        # corpo = corpo.replace('\n', '<br>')  # o conteudo do body
        # assinatura = assinatura.replace('\n', '<br>')  # assintura
        self.logger.info('criando template {} - {}'.format(titulo, assinatura))
        self.html = '''
             <!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN" "http://www.w3.org/TR/REC-html40/loose.dtd">
             <html>
             <head><meta name="viewport" content="width=device-width, initial-scale=1.0"><meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                 <title>Retentiva</title>
                 <style type="text/css">.ak-content { margin: auto; background-color: #FFFFFF; }
             .ak-content a { color: #22224D; }
             .ak-container { width: 100%; }
             .ak-content table tr td { font-family: arial, helvetica, sans-serif; font-size: 16px; color: #4A423C; }
             .ak-button { border-radius: 3px; background-color: #6DC6DD; border-collapse: separate !important; }
             .ak-button tr td { padding: 10px; }
             .ak-button a { text-decoration: none; color: #FFFFFF; font-size: 18px; }
             .ak-line { border-top: 1px solid #CCCCCC; }
             .ak-box { border: 1px solid #CCCCCC; }
             img { border: 0px none; }
             .ak-content-assinatura { padding: 0px 25px 25px; background-color: #FFFFFF; }
             .ak-footer { color: #4A423C; font-size: 13px; border-top: 1px solid #DADADA; }
             .ak-footer td { padding: 20px 25px; }
             .ak-product h5 { margin: 0px; font-weight: normal; }
             .ak-product h2 { margin: 0px; }
             .ak-column-left img { max-width: 100% !important; }
             .ak-column-right img { max-width: 100% !important; }
             @media only screen and (max-width: 750px) {
               .ak-content { width: 100% !important; min-width: 100% !important; }
             }
             @media only screen and (max-width: 450px) {
               body, table, td, a, li, blockquote { margin: 0px; }
               table { border-collapse: collapse; table-layout: fixed; min-width: 100% !important; }
               .layout-email { width: 100% !important; }
               .ak-content { font-size: 18px; }
               .ak-button { max-width: 100% !important; min-width: auto !important; }
               .ak-button a { font-size: 18px; display: block !important; }
               .ak-image { max-width: 100% !important; }
               #ak-columns { width: 100% !important; min-width: 100% !important; }
               .ak-column-container { clear: both; margin-bottom: 30px; width: 100% !important; min-width: 100% !important; margin-left: 0px !important; }
               .ak-column-container:last-child { margin-bottom: 0px; }
               .ak-column-left { line-height: 100% !important; }
               .ak-column-right { line-height: 100% !important; }
               .ak-product td { height: auto; }
               .ak-logo { height: auto; max-width: 100% !important; width: 100% !important; }
               .ak-logo td { padding: 25px; }
               .ak-footer td { font-size: 16px !important; }
               .ak-email-button { width: 100%; }
             }
             .my-content td { padding: 20px; }
             .my-content-assinatura td { padding: 20px; }
                 </style>
             </head>
             <body tcap-name="framey0">
             <table cellpadding="0" cellspacing="0" class="ak-container" style="width: 100%;" width="100%">
                 <tbody>
                     <tr>
                         <td>
                         <table align="center" cellpadding="0" cellspacing="0" class="ak-content" style="background-color: #FFFFFF; margin: auto;-moz-border-radius: 10px 10px 0 0;-moz-border-radius: 10px 10px 0 0;border-radius: 10px 10px 0 0;" widthxx="900">
                             <tbody>
                                 <tr>
                                     <td>
                                     <table border="0" cellpadding="0" cellspacing="0" style="background-color: #34495E;" width="100%">
                                         <tbody>
                                             <tr>
                                                 <td style="color: #4A423C; font-family: arial, helvetica, sans-serif; font-size: 16px; padding: 10px 0px;">
                                                 <div style="color:#ffffff;text-shadow:2px 1px #4a5f7c;text-align: center;font-size:calc(18px + 0.8vw);"><span style="color:#ffffff;"><span style="font-size:22px;font-size:calc(18px + 0.8vw);"><span style="font-family:Tahoma,Geneva,sans-serif;"><strong>
                                                 <!-- titulo -->''' + titulo + '''</strong></span></span></span></div>
                                                 </td>
                                             </tr>
                                         </tbody>
                                     </table>

                                     <!--<table border="0" cellpadding="0" cellspacing="0" style="background-color: #EBF0F5;" width="100%">-->
                                     <table border="0" cellpadding="0" cellspacing="0" style="background-color: #fff;" width="100%">
                                         <tbody>
                                             <tr>
                                                 <td style="color: #4A423C; font-family: arial, helvetica, sans-serif; font-size: 16px; padding: 30px 20px;">
                                                 <div style="color:#2F3958;">
                                                     <!-- corpo -->''' + corpo + '''</div>
                                                 </td>
                                             </tr>
                                         </tbody>
                                     </table>

                                     <!--<table border="0" cellpadding="0" cellspacing="0" style="background-color: #A7B5C4;" width="100%">-->
                                     <table border="0" cellpadding="0" cellspacing="0" style="background-color: #6b7887;" width="100%">
                                         <tbody>
                                             <tr>
                                                 <td style="color: #4A423C; font-family: arial, helvetica, sans-serif; font-size: 16px; padding: 5px 20px;">
                                                 <div style="color: white; text-align: center;">
                                                     <!-- assinatura -->''' + assinatura + '''</div>
                                                 </td>
                                             </tr>
                                         </tbody>
                                     </table>

                                     <table border="0" cellpadding="0" cellspacing="0" style="background-color: #f7f8f9;" width="100%">
                                         <tbody>
                                             <tr>
                                                 <td style="color: #4A423C; font-family: arial, helvetica, sans-serif; font-size: 0px; text-align: center; padding: 20px;"><img ak:edit="image" alt="Fontes" class="ak-image" src="https://fontespromotora.com.br/wp-content/uploads/2019/09/logo-fontes-menor.png" style="border: 0px none; width: 160px; max-width: 160px;" width="160" /></td>
                                             </tr>
                                         </tbody>
                                     </table>

                                     <table border="0" cellpadding="0" cellspacing="0" style="background-color: #34495E;" width="100%">
                                         <tbody>
                                             <tr>
                                                 <td style="color: #4A423C; font-family: arial, helvetica, sans-serif; font-size: 16px; padding: 5px 2px;-moz-border-radius:  0 0 10px 10px;-moz-border-radius:  0 0 10px 10px;border-radius:  0 0 10px 10px;">
                                                 <center>&nbsp; <a href="https://fontespromotora.com.br/" style="color: #22224D; padding: 10px;" target="_blank" title=""><img alt="" border="0" src="https://fontespromotora.com.br/marketing/emkt/informativos/etc/logo/site.png" style="border: 0px none; max-width: 20px;" /></a> &nbsp; <a href="https://www.instagram.com/fontespromotora" style="color: #22224D; padding: 10px;" target="_blank" title=""><img alt="" border="0" src="https://fontespromotora.com.br/marketing/emkt/informativos/etc/logo/instagram.png" style="border: 0px none; max-width: 20px;" /></a> &nbsp; <a href="https://www.facebook.com/Fontes-Promotora-2279931192295265/" style="color: #22224D; padding: 10px;" target="_blank" title=""><img alt="" border="0" src="https://fontespromotora.com.br/marketing/emkt/informativos/etc/logo/facebook.png" style="border: 0px none; max-width: 20px;" /></a> &nbsp;</center>
                                                 </td>
                                             </tr>
                                         </tbody>
                                     </table>
                                     </td>
                                 </tr>
                             </tbody>
                         </table>
                         </td>
                     </tr>
                 </tbody>
             </table><div style="font-size: 8px;">'''+socket.gethostname()+'''</div>
             </body>
             </html>

         '''

        return self.html






    def template_html_sem_logo(self, titulo, corpo, assinatura):  # todos os campos aceitam tags htmls

        #titulo = titulo.replace('\n', '<br>')  # titulo do header do body
        #corpo = corpo.replace('\n', '<br>')  # o conteudo do body
        #assinatura = assinatura.replace('\n', '<br>')  # assintura
        self.logger.info('criando template {} - {}'.format(titulo, assinatura))
        self.html = '''
            <!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN" "http://www.w3.org/TR/REC-html40/loose.dtd">
            <html>
            <head><meta name="viewport" content="width=device-width, initial-scale=1.0"><meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                <title>Email</title>
                <style type="text/css">.ak-content { margin: auto; background-color: #FFFFFF; }
            .ak-content a { color: #22224D; }
            .ak-container { width: 100%; }
            .ak-content table tr td { font-family: arial, helvetica, sans-serif; font-size: 16px; color: #4A423C; }
            .ak-button { border-radius: 3px; background-color: #6DC6DD; border-collapse: separate !important; }
            .ak-button tr td { padding: 10px; }
            .ak-button a { text-decoration: none; color: #FFFFFF; font-size: 18px; }
            .ak-line { border-top: 1px solid #CCCCCC; }
            .ak-box { border: 1px solid #CCCCCC; }
            img { border: 0px none; }
            .ak-content-assinatura { padding: 0px 25px 25px; background-color: #FFFFFF; }
            .ak-footer { color: #4A423C; font-size: 13px; border-top: 1px solid #DADADA; }
            .ak-footer td { padding: 20px 25px; }
            .ak-product h5 { margin: 0px; font-weight: normal; }
            .ak-product h2 { margin: 0px; }
            .ak-column-left img { max-width: 100% !important; }
            .ak-column-right img { max-width: 100% !important; }
            @media only screen and (max-width: 750px) {
              .ak-content { width: 100% !important; min-width: 100% !important; }
            }
            @media only screen and (max-width: 450px) {
              body, table, td, a, li, blockquote { margin: 0px; }
              table { border-collapse: collapse; table-layout: fixed; min-width: 100% !important; }
              .layout-email { width: 100% !important; }
              .ak-content { font-size: 18px; }
              .ak-button { max-width: 100% !important; min-width: auto !important; }
              .ak-button a { font-size: 18px; display: block !important; }
              .ak-image { max-width: 100% !important; }
              #ak-columns { width: 100% !important; min-width: 100% !important; }
              .ak-column-container { clear: both; margin-bottom: 30px; width: 100% !important; min-width: 100% !important; margin-left: 0px !important; }
              .ak-column-container:last-child { margin-bottom: 0px; }
              .ak-column-left { line-height: 100% !important; }
              .ak-column-right { line-height: 100% !important; }
              .ak-product td { height: auto; }
              .ak-logo { height: auto; max-width: 100% !important; width: 100% !important; }
              .ak-logo td { padding: 25px; }
              .ak-footer td { font-size: 16px !important; }
              .ak-email-button { width: 100%; }
            }
            .my-content td { padding: 20px; }
            .my-content-assinatura td { padding: 20px; }
                </style>
            </head>
            <body tcap-name="framey0">
            <table cellpadding="0" cellspacing="0" class="ak-container" style="width: 100%;" width="100%">
                <tbody>
                    <tr>
                        <td>
                        <table align="center" cellpadding="0" cellspacing="0" class="ak-content" style="background-color: #FFFFFF; margin: auto;-moz-border-radius: 10px 10px 0 0;-moz-border-radius: 10px 10px 0 0;border-radius: 10px 10px 0 0;" widthxx="900">
                            <tbody>
                                <tr>
                                    <td>
                                    <table border="0" cellpadding="0" cellspacing="0" style="background-color: #51596B;" width="100%">
                                        <tbody>
                                            <tr>
                                                <td style="color: #4A423C; font-family: arial, helvetica, sans-serif; font-size: 16px; padding: 10px 0px;">
                                                <div style="color:#ffffff;text-shadow:2px 1px #4a5f7c;text-align: center;font-size:calc(18px + 0.8vw);"><span style="color:#ffffff;"><span style="font-size:22px;font-size:calc(18px + 0.8vw);"><span style="font-family:Tahoma,Geneva,sans-serif;"><strong>
                                                <!-- titulo -->''' + titulo + '''</strong></span></span></span></div>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>

                                    <table border="0" cellpadding="0" cellspacing="0" style="background-color: #EBF0F5;" width="100%">
                                        <tbody>
                                            <tr>
                                                <td style="color: #4A423C; font-family: arial, helvetica, sans-serif; font-size: 16px; padding: 30px 20px;">
                                                <div style="color:#2F3958;">
                                                    <!-- corpo -->''' + corpo + '''</div>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>

                                    <!--<table border="0" cellpadding="0" cellspacing="0" style="background-color: #A7B5C4;" width="100%">-->
                                    <table border="0" cellpadding="0" cellspacing="0" style="background-color: #6b7887;" width="100%">
                                        <tbody>
                                            <tr>
                                                <td style="color: #4A423C; font-family: arial, helvetica, sans-serif; font-size: 16px; padding: 5px 20px;">
                                                <div style="color: white; text-align: center;">
                                                    <!-- assinatura -->''' + assinatura + '''</div>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>

                                    <table border="0" cellpadding="0" cellspacing="0" style="background-color: #f7f8f9;" width="100%">
                                        <tbody>
                                            <tr>
                                                <!--<td style="color: #4A423C; font-family: arial, helvetica, sans-serif; font-size: 0px; text-align: center; padding: 20px;">-->
                                                <td style="color: #4A423C; font-family: arial, helvetica, sans-serif; font-size: 0px; text-align: center; padding: 10px;">
                                                
                                                <!--<img ak:edit="image" alt="Retentiva" class="ak-image" src="https://fontespromotora.com.br/EMPRESA/retentiva.com.br/img/retentiva.png" style="border: 0px none; width: 160px; max-width: 160px;" width="160" />-->
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>

                                    <table border="0" cellpadding="0" cellspacing="0" style="background-color: #51596B;" width="100%">
                                        <tbody>
                                            <tr>
                                                <!--<td style="color: #4A423C; font-family: arial, helvetica, sans-serif; font-size: 16px; padding: 5px 2px;-moz-border-radius:  0 0 10px 10px;-moz-border-radius:  0 0 10px 10px;border-radius:  0 0 10px 10px;">-->
                                                <td style="color: #4A423C; font-family: arial, helvetica, sans-serif; font-size: 16px; padding: 10px;-moz-border-radius:  0 0 10px 10px;-moz-border-radius:  0 0 10px 10px;border-radius:  0 0 10px 10px;">
                                                <!--
                                                <center>&nbsp; <a href="https://retentiva.com.br/" style="color: #22224D; padding: 10px;" target="_blank" title=""><img alt="" border="0" src="https://fontespromotora.com.br/marketing/emkt/informativos/etc/logo/site.png" style="border: 0px none; max-width: 20px;" /></a> &nbsp; <a href="https://www.instagram.com/retentivacontactcenter/" style="color: #22224D; padding: 10px;" target="_blank" title=""><img alt="" border="0" src="https://fontespromotora.com.br/marketing/emkt/informativos/etc/logo/instagram.png" style="border: 0px none; max-width: 20px;" /></a> &nbsp; <a href="https://www.facebook.com/retentivacontactcenter/" style="color: #22224D; padding: 10px;" target="_blank" title=""><img alt="" border="0" src="https://fontespromotora.com.br/marketing/emkt/informativos/etc/logo/facebook.png" style="border: 0px none; max-width: 20px;" /></a> &nbsp;</center>
                                                -->
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        </td>
                    </tr>
                </tbody>
            </table><div style="font-size: 8px;">'''+socket.gethostname()+'''</div>
            </body>
            </html>
        '''


        return self.html





    def enviar_email(self, destinatario, destinatario_cc, destinatario_cco_B, assunto, mensagem, file_to_attach):

        destinatario=self.util.somente_emails(destinatario)
        destinatario_cc=self.util.somente_emails(destinatario_cc)
        destinatario_cco_B=self.util.somente_emails(destinatario_cco_B)

        self.logger.info(f'tratado destinatario={destinatario}')
        self.logger.info(f'tratado destinatario_cc={destinatario_cc}')
        self.logger.info(f'tratado destinatario_cco_B={destinatario_cco_B}')



        #destinatario_cco=f'{destinatario_cco_B},enio.farias.f@gmail.com'.strip(' ,')
        #destinatario_cco=f'{destinatario_cco_B},enio.farias@retentiva.com.br,robo.retentiva@gmail.com,enio.farias.retentiva@gmail.com'.strip(' ,')

        # destinatario_cco=f'{destinatario_cco_B},robo.sistema.01@gmail.com'.strip(' ,')
        # destinatario_cco=f'{destinatario_cco_B},{self.email_cco_default}'.strip(' ,').strip(',').strip(' ')
        destinatario_cco=self.util.somente_emails(f'{destinatario_cco_B},{self.email_cco_default}')
        self.logger.info(f'tratado destinatario_cco={destinatario_cco}')
        self.logger.info(
            'Preparando envio >> to: {} | cc: {} | cco: {} | assunto {} | files: {}'.format(destinatario, destinatario_cc,
                                                                               destinatario_cco, assunto,
                                                                               file_to_attach))
        print('\n')  # mensagem é o html gerado pelo funcao template_html
        msg = MIMEMultipart()
        print('mailler001')
        msg['Subject'] = assunto
        print('mailler002')
        # msg['From'] = f'"{self.remetente_nome} <{self.remetente}>"'
        #msg['From'] = f'"{self.remetente_nome}" <{self.remetente}>'
        msg['From'] = f'{self.remetente_nome} <{self.remetente}>'
        #msg['Reply-to'] = f'"{self.remetente_nome}" <{self.remetente}>'
        print(f'mailler003 - From = {self.remetente_nome} <{self.remetente}>')
        # msg['Disposition-Notification-To'] = "{} <{}>".format(self.remetente_nome, self.remetente)
        #msg['Disposition-Notification-To'] = f'"{self.remetente_nome} <{self.remetente}>"'
        print('mailler004')

        #solicitação de leitura
        #msg['Disposition-Notification-To'] = "{}".format(self.remetente)

        print('mailler005')
        #email_remetente_de = "{} <{}>".format(self.remetente_nome, self.remetente)
        #rcpt = cc.split(",") + bcc.split(",") + [to]
        #msg['Bcc'] = destinatario_cco  # .split(",")
        msg['Bcc'] = destinatario_cco  # .split(",")
        #msg['Bcc'] = ", ".join(destinatario_cco)  # .split(",")

        if f'{destinatario}' == '':
            # msg['To'] = destinatario
            msg['To'] = self.remetente
        else:
            msg['To'] = destinatario



        msg['Cc'] = destinatario_cc    #.split(",")

        #msg.add_header('Reply-to', "{}" <{}>.format(self.remetente_nome, self.remetente))

        msg.add_header('Reply-to', "<{}>".format(self.remetente))

        # msg.add_header('From', '"{}" <{}>'.format(self.remetente_nome, self.remetente))
        msg.add_header('From', '{} <{}>'.format(self.remetente_nome, self.remetente))
        #msg.add_header('From', '<{}>'.format(self.remetente))

        msg.attach(MIMEText(mensagem.encode('utf-8'), 'html', 'UTF-8'))

        if bool(file_to_attach):  # teste para verificar se possui anexos
            self.logger.info('preparando anexos: {}'.format(file_to_attach))
            qtde_files_controle = len(file_to_attach)
            self.logger.debug(f'qtde_files_controle do anexo antes de verificar se existem: {qtde_files_controle}')
            files = []
            if qtde_files_controle > 0:
                while qtde_files_controle > 0:
                    arquivo_da_vez = file_to_attach[ qtde_files_controle - 1 ]
                    self.logger.debug(f'verificando arquivo {qtde_files_controle}: {arquivo_da_vez}')
                    if os.path.exists(f'{arquivo_da_vez}'):
                        self.logger.debug(f'verificando arquivo {qtde_files_controle}: {arquivo_da_vez} existe, adicionando na lista')
                        files.append(f'{arquivo_da_vez}')
                    else:
                        self.logger.warning(f'verificando arquivo {qtde_files_controle}: {arquivo_da_vez} NÃO existe, NÃO adiciona na lista')
                    self.logger.debug(f'{qtde_files_controle}: lista anexo: {files}')
                    qtde_files_controle -= 1
            else:
                files = []




            # files = file_to_attach

            qtde_files = len(files)
            self.logger.info('Contabilizando_anexos = {}'.format(qtde_files))
            files_count = 0
            while files_count < qtde_files:
                file = files[files_count].strip(' ')
                if os.name == 'nt':  # identifica o tipo de OS, para win=nt
                    listfiledir = file.split('\\')  # windows
                    #print('        OS windows')
                else:
                    listfiledir = file.split('/')  # linux
                    #print('        OS linux')
                self.logger.info('indexando anexo {} = {}'.format(files_count,file))
                filelen = len(listfiledir)  # pega a quantidade de diretorios que tem  no caminho do arquivo usando o separador /(unix) ou \(win)
                filename = listfiledir[filelen - 1]  # pega o nome do arquivo
                attachment = open(file, "rb")
                part = MIMEBase('application', 'octet-stream')
                part.set_payload((attachment).read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
                msg.attach(part)
                files_count += 1
        tentativa = 0
        maxtent = 10
        while tentativa < maxtent:
            self.logger.info(f'{self.username} - tentativa:{tentativa} < {maxtent}')
            try:
                self.logger.info('({})({}) - iniciando envio gmail {}: {} - {}'.format(self.username,self.password, int(tentativa), assunto, destinatario))
                socket.setdefaulttimeout(380)
                server = smtplib.SMTP_SSL(self.servidor, self.porta)
                server.ehlo()


                server.login(self.username, self.password)



                del msg['Bcc']
                #del msg['From']

                #server.sendmail(msg['From'], (msg['To'] + ',' + msg['Cc'] + ',' + msg['Bcc']).split(','),msg.as_string())
                #server.sendmail(msg['From'], (msg['To'] + ',' + msg['Bcc'] + ',' + msg['Cc']).split(','),msg.as_string())
                server.sendmail(msg['From'], (msg['To'] + ',' + destinatario_cco + ',' + msg['Cc']).split(','),msg.as_string())
                #server.sendmail(f'{email_remetente_de}', (msg['To'] + ',' + destinatario_cco + ',' + msg['Cc']).split(','),msg.as_string())
                #server.sendmail(msg['From'], (msg['To'] + ',' + msg['Cc'] + ',' + msg['Bcc']).split(','),msg.as_string())
                server.close()
                tentativa = 100
            except:
                self.logger.error('({})({}) - Tentativa {} falhou. Aguardando para tentar reenviar: {} - {}'.format(self.username,self.password,tentativa, assunto,destinatario))
                self.logger.error(str(sys.exc_info()))
                tentativa += 1
                self.erros_envios_usuario_exclusivo += 1
                time.sleep(20)

                self.pega_user_senha()

            finally:
                if tentativa == 10:
                    self.logger.error('({})({}) - Tentativas maximas {} falharam. Não foi possivel enviar :(  {} - {}'.format(self.username,self.password,tentativa, assunto,destinatario))
                    raise Exception("({})({}) - falha no envio de gmail {} - {} - tentativa {}".format(self.username,self.password,assunto, destinatario, tentativa))


                # time.sleep(1)

            self.logger.info(f'({self.username})({self.password}) - tentativa:{tentativa} < {maxtent}')

