# -*- coding: utf-8 -*-#coding: utf-8from datetime import datetime, timedelta, dateimport time#from dateutil import rruleimport configparserimport refrom unicodedata import normalizeimport osimport zipfileimport urllib.requestimport shutilimport globimport csvimport seleniumfrom selenium import webdriverimport ftplibfrom selenium.webdriver.common.action_chains import ActionChainsfrom selenium.common.exceptions import NoSuchElementExceptionfrom selenium.webdriver.common.by import Byfrom selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0#from selenium.webdriver import ActionChainsfrom PIL import Imagefrom PIL import ImageFontfrom PIL import ImageDrawimport unicodedataimport numpy as npimport cv2class Utilities():    def create_robo_header(self, robo_codigo, robo_descricao):        print('\n\n******************************************************************')        print('*')        print('*              Robôs - Copyright (c) 2019')        print('*')        print('******************************************************************')        print('*')        print('*   Robô:   ' + robo_codigo)        print('*  <|º_º|>  ' + robo_descricao )        print('*')        print('******************************************************************')    def create_robo_footer(self, status, inicio_execucao, fim_execucao):        print('\n\n******************************************************************')        print('*')        print('* Status:  ' + status)        print('* Duração: ' + self.convert_seconds(fim_execucao - inicio_execucao))        print('*')        print('******************************************************************\n\n')    def get_config(self):        config = configparser.ConfigParser()        try:            config.read('config/config.ini', encoding='utf-8')            print("Configurações config utf8 carregadas com sucesso!")        except:            config.read('config/config.ini')            print("Configurações sem utf config carregadas com sucesso!")        return config    def obter_data_atual_sem_horas(self, mask):        now = date.today()        current_date = datetime.strptime(str(now), mask).date()        return current_date    def obter_data_atual_com_horas(self, mask):        now = date.today()        current_date = datetime.strftime(now, mask)        return current_date    def data_hora_brasil(self):        # return time.strftime("%d/%m/%Y - %H:%M:%S")        return time.strftime("%d/%m/%Y %H:%M:%S")    def data_hora_americano(self):        # return time.strftime("%Y/%m/%d - %H:%M:%S")        return time.strftime("%Y/%m/%d %H:%M:%S")    ''' Método utilizado para determinar a data limite de retenção '''    def obter_data_limite_retencao(self, data):        # Formata data        nova_data = datetime.strptime(data, "%d/%m/%Y")        holidays = [datetime.strptime('07/09/2018', "%d/%m/%Y"),                    datetime.strptime('12/10/2018', "%d/%m/%Y"),                    datetime.strptime('02/11/2018', "%d/%m/%Y"),                    datetime.strptime('15/11/2018', "%d/%m/%Y"),                    datetime.strptime('25/12/2018', "%d/%m/%Y")]        # Create a rule to recur every weekday starting today        r = rrule.rrule(rrule.DAILY,                        byweekday=[rrule.MO, rrule.TU, rrule.WE, rrule.TH, rrule.FR],                        dtstart=nova_data)        # Create a rruleset        rs = rrule.rruleset()        # Attach our rrule to it        rs.rrule(r)        # Add holidays as exclusion days        for exdate in holidays:            rs.exdate(exdate)        nova_data = rs[5]        return datetime.strftime(nova_data, "%d/%m/%Y")    def convert_seconds(self, seconds):        seconds = int(seconds)        minutes, seconds = divmod(seconds, 60)        hours, minutes = divmod(minutes, 60)        periods = [('hours', hours), ('minutes', minutes), ('seconds', seconds)]        time_string = ', '.join('{} {}'.format(value, name)                                for name, value in periods                                if value)        return time_string    def convert_millis(self, millis):        millis = int(millis)        seconds=(millis/1000)%60        seconds = int(seconds)        minutes=(millis/(1000*60))%60        minutes = int(minutes)        hours=(millis/(1000*60*60))%24        return "%d:%d:%d" % (hours, minutes, seconds)    def recupera_nome_mes(self, mes):        meses = ["Unknown",                 "JANEIRO",                 "FEVEREIRO",                 "MARÇO",                 "APRIL",                 "MAIO",                 "JUNHO",                 "JULHO",                 "AGOSTO",                 "SETEMBRO",                 "OUTUBRO",                 "NOVEMBRO",                 "DEZEMBRO"]        return meses[int(mes)]    def retorna_primeiro_dia_semana(self, mask):        day = time.strftime(mask)        dt = datetime.strptime(day, mask)        start = dt - timedelta(days=dt.weekday())        return start.strftime(mask)    def retorna_ultimo_dia_semana(self, mask):        day = time.strftime(mask)        dt = datetime.strptime(day, mask)        start = dt - timedelta(days=dt.weekday())        end = start + timedelta(days=4)        return end.strftime(mask)    def ler_arquivo(self, filename):        #print(f'ler_arquivo01 - filename {filename}')        f = open(filename)        #print('ler_arquivo02')        lines = f.read().splitlines()        #print(f'lines {lines}')        #print('ler_arquivo03')        f.close()        #print('ler_arquivo04')        return lines    def ler_primeira_linha_arquivo(self, filename):        f = open(filename)        lines = f.readlines()        # print(f'lendo lines={lines[0]}')        f.close()        # time.sleep(5)        return lines[0]    def salvar_arquivo(self, filename, valor):        with open(filename, 'w+') as f:            f.seek(0)            f.write(valor)    def sobrescrever_arquivo(self, filename, valor):        #with open(filename, 'w') as f:            #f.seek(0)            #f.write(valor)        with open(filename, 'w') as file:            file.write('{}'.format(valor))    def recriar_arquivo(self, filename):        f = open(filename, "w+")        f.close()    def agregar_arquivo(self, filename, valor):        with open(filename, 'a') as f:            f.write(valor + '\n')        f.close()    def agregar_arquivo_sem_quebra(self, filename, valor):        with open(filename, 'a') as f:            f.write(valor)        f.close()    def formatar_cpf(self, cpf):        if len(cpf) < 11:            cpf = cpf.zfill(11)        cpf = '{}.{}.{}-{}'.format(cpf[:3], cpf[3:6], cpf[6:9], cpf[9:])        return cpf    def limpar_cpf(self, cpf):        return str(cpf).replace('-','').replace('.','')    def cpf11digits(self, cpf):        return str('{:0>11}'.format(self.somente_numeros(cpf)))   #cpf com 11 digito e somente numeros (deve ser passado como string)    def convert_data_excel_humano(self, excel_data):        #excel_data = 43411 >> 07/11/2018        data_transformada = datetime.fromordinal(datetime(1900, 1, 1).toordinal() + excel_data - 2).date() #tem que ser '-2' por causa de uma contagem maluca do excel        data_formato_humano = str('{:0>2}/{:0>2}/{:0>4}'.format(data_transformada.day,data_transformada.month,data_transformada.year))        #print('{} > {} >> {}'.format(excel_data, data_transformada, data_formato_humano))        return data_formato_humano    def line_count(self, fname):        num_lines = 0        with open(fname, 'r', encoding="utf8") as f:            for line in f:                num_lines += 1        return (num_lines)    def somente_numeros(self, numerossujos):        return re.sub('[^0-9]', '', numerossujos)    def remover_acentos(self, txt):        # https://wiki.python.org.br/RemovedorDeAcentos        return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')    #enio 07/08/2019    def removedor_acentuacao(self, string_com_acentos):        #fonte da dica: https://pt.stackoverflow.com/questions/331297/como-remover-acentua%C3%A7%C3%B5es-com-express%C3%B5es-regulares-no-python        #Um modo simples que usa o módulo unicodedata, incluído no python, pra decompor cada acento unicode em seu codepoint original + codepoint de combinação, depois filtrar os codepoints de combinação para ter uma string limpa:        #import unicodedata        #string_com_acentos = "Olá você está????"        string_nova = ''.join(ch for ch in unicodedata.normalize('NFKD', string_com_acentos) if not unicodedata.combining(ch))        #print(string_nova)        return f'{string_nova}'    def numero_para_coluna_excel(self,dividendo):        # dividendo L divisor=26        # resto         quociente-1        colunas = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",                   "U", "V", "W", "X", "Y", "Z"]        if dividendo < 702:            if dividendo > 25:                resto = dividendo % 26                quociente = dividendo / 26 - 1                return '{}{}'.format(colunas[int(quociente)], colunas[int(resto)])            else:                return '{}'.format(colunas[dividendo])        else:            return 'null'    def pegar_nome_arquivo(self,diretorio_e_arquivo):        file = diretorio_e_arquivo.strip(' ')        if os.name == 'nt':                    #identifica o tipo de OS, para win=nt            listfiledir=file.split('\\')       #windows        else:            listfiledir=file.split('/')        # linux        filelen = len(listfiledir)         #pega a quantidade de diretorios que tem  no caminho do arquivo usando o separador /(unix) ou \(win)        filename = listfiledir[filelen-1]        return filename    def pegar_caminho_diretorio_do_arquivo(self, diretorio_e_arquivo):        file = diretorio_e_arquivo.strip(' ')        if os.name == 'nt':  # identifica o tipo de OS, para win=nt            listfiledir = file.split('\\')  # windows        else:            listfiledir = file.split('/')  # linux        filelen = len(            listfiledir)  # pega a quantidade de diretorios que tem  no caminho do arquivo usando o separador /(unix) ou \(win)        dirname = self.converte_lista_para_texto(listfiledir[0:filelen - 1], '/')        return dirname    def converte_lista_para_texto(self, lista, separador):        # Converting integer list to string list        list_string = [str(i) for i in lista]        # Join list items using join()        list_string = f"{separador}".join(list_string)        return list_string    # def converte_texto_para_lista(self, texto):    #     lista = f"{texto.split()}"    #     return lista    def criar_diretorio(self,dirName):        try:            os.makedirs(dirName)            print("Directory ", dirName, " Created ")        except FileExistsError:            print("Directory ", dirName, " already exists")    def limpar_diretorio(self,path):        #path = "diretorio"        dir = os.listdir(path)        os.listdir(path)        #time.sleep(0.5)        print('\n')        for file in dir:            print('deletando {}/{}'.format(path,file))            try:                os.remove(path+'/'+file)            except:                print('Deletando file {} ---> não encontrado'.format(file))            #if file == "arquivo.txt":            #    os.remove(file)        print('\n')        time.sleep(0.4)    def zipar(self, nome_do_zip, arqs_para_zipar):                               #arqs_para_zipar em forma de lista, parecido com o append do anexos do qlikview e mailler_gmail        fantasy_zip = zipfile.ZipFile('{}'.format(nome_do_zip), 'w')        files = arqs_para_zipar        #files=anexos        qtde_files = len(files)        files_count = 0        while files_count < qtde_files:            file = files[files_count].strip(' ')            if os.name == 'nt':                    #identifica o tipo de OS, para win=nt                listfiledir=file.split('\\')       #windows            else:                listfiledir=file.split('/')            filelen = len(listfiledir)         #pega a quantidade de diretorios que tem  no caminho do arquivo usando o separador /(unix) ou \(win)            filename=listfiledir[filelen-1]            print('filename {}'.format(filename))            fantasy_zip.write(file, filename, compress_type=zipfile.ZIP_DEFLATED)            #fantasy_zip.write(file, compress_type=zipfile.ZIP_DEFLATED)            files_count +=1        fantasy_zip.close()    def subir_ftp(self, host, username, password, arquivo, dir_destino):        File2Send = arquivo        filename=self.pegar_nome_arquivo(arquivo)        #print('File2Send {}'.format(File2Send))        Output_Directory = dir_destino        #print('Output_Directory {}'.format(Output_Directory))        tentativas=0        max_tentativas=3        print("\nstart ftp")        while tentativas < max_tentativas:            try:                # ftp = FTP(host)                ftp = FTP(host, timeout=600)                #ftp.connect(host='', port=0, timeout=None, source_address=None)                ftp.login(username, password)                #print('ftp: {} {} {}'.format(ftp,username,password))                file = open(File2Send, "rb")                #print('file {}'.format(file))                ftp.cwd(Output_Directory)                ftp.storbinary('STOR ' + filename, file)                print("STORing File now...")                ftp.quit()                file.close()                print("File transfered")                tentativas = 100                #status='Sucesso'            except:                print("An error occured {}".format(tentativas))                tentativas +=1                #status = 'Erro'                time.sleep(30)            finally:                if tentativas == 3:                    print('Tentativa {} falhou. Não foi possivel enviar :(  {} - {}'.format(tentativas, arquivo,host))                    raise Exception("falha em subir arquivo {} para ftp {} - tentativa {}".format(arquivo,host,tentativas))                #time.sleep(10)    def criar_dir_ftp(self, host, username, password, arquivo, dir_destino):        File2Send = arquivo        filename=self.pegar_nome_arquivo(arquivo)        #print('File2Send {}'.format(File2Send))        Output_Directory = dir_destino        #print('Output_Directory {}'.format(Output_Directory))        tentativas=0        max_tentativas=3        print("\nstart ftp")        while tentativas < max_tentativas:            try:                ftp = FTP(host, timeout=600)                ftp.login(username, password)                file = open(File2Send, "rb")                ftp.cwd(Output_Directory)                ftp.storbinary('STOR ' + filename, file)                print("STORing File now...")                ftp.quit()                file.close()                print("File transfered")                tentativas = 100            except:                print("tentativas excedidas{}".format(tentativas))                tentativas +=1                time.sleep(30)            finally:                if tentativas == 3:                    print('Tentativa {} falhou. Não foi possivel enviar :(  {} - {}'.format(tentativas, arquivo,host))                    raise Exception("falha em subir arquivo {} para ftp {} - tentativa {}".format(arquivo,host,tentativas))                #time.sleep(10)    def pega_nome_robo(self, nome_robo):        nome_1ist = nome_robo.split('/')        nome_last=len(nome_1ist) - 1        nome_list2=nome_1ist[nome_last].split('.')        nome_last2=nome_list2[0]        return '{}'.format(nome_last2)    def duplica_log_robo(self,logging,logger,log_dir,robo_nome):        #print('logging {} ,logger {} ,log_dir {} ,robo_nome {}'.format(logging,logger,log_dir,robo_nome))        fh = logging.FileHandler('{}{}.log'.format(log_dir, robo_nome))        fh.setLevel(logging.DEBUG)        ch = logging.StreamHandler()        ch.setLevel(logging.ERROR)        formatter = logging.Formatter('%(asctime)s %(name)s: %(levelname)s %(message)s ')        ch.setFormatter(formatter)        fh.setFormatter(formatter)        logger.addHandler(ch)        logger.addHandler(fh)    ###############################################    def escreve_imagem_old(self, arquivo_entrada, arquivo_saida,path_font,font_ttf, size, corR, corG, corB, top, left, texto):        #exemplo de paramentros font:        #font_ttf, size, corR, corG, corB, top, left = 'Roboto-Regular.ttf', 10, 218, 220, 224, 1, 25        #exemplos robo stormtech_002        # self.util.criar_diretorio(self.util.pegar_caminho_diretorio_do_arquivo(f'{arquivo_saida}'))        self.criar_diretorio(self.pegar_caminho_diretorio_do_arquivo(f'{arquivo_saida}'))        #self.logger.info(f'abrindo imagem para editar {arquivo_entrada}')        print(f'abrindo imagem para editar {arquivo_entrada}')        #font = ImageFont.truetype(f'{self.path_font}{font_ttf}', size)        font = ImageFont.truetype(f'{path_font}{font_ttf}', size)        img_arquivo_entrada = Image.open(f'{arquivo_entrada}')        draw = ImageDraw.Draw(img_arquivo_entrada)        draw.text((left, top), f'{texto}', (corR, corG, corB), font=font)        # self.logger.info(f'salvando imagem {arquivo_saida}')        print(f'salvando imagem {arquivo_saida}')        img_arquivo_entrada.save(f'{arquivo_saida}')        print('\n')    ###############################################    def escreve_imagem(self,arquivo,path_tmp,path_font,font_ttf, size, corR, corG, corB, top, left, texto):        nome_saida = self.pegar_nome_arquivo(arquivo)        #exemplo de paramentros font:        #font_ttf, size, corR, corG, corB, top, left = 'Roboto-Regular.ttf', 10, 218, 220, 224, 1, 25        #exemplos robo stormtech_002        # self.util.criar_diretorio(self.util.pegar_caminho_diretorio_do_arquivo(f'{arquivo_saida}'))        self.criar_diretorio(self.pegar_caminho_diretorio_do_arquivo(f'{arquivo}'))        self.criar_diretorio(self.pegar_caminho_diretorio_do_arquivo(f'{path_tmp}'))        print(f'abrindo imagem para editar {arquivo}')        #font = ImageFont.truetype(f'{self.path_font}{font_ttf}', size)        font = ImageFont.truetype(f'{path_font}{font_ttf}', size)        img_arquivo_entrada = Image.open(f'{arquivo}')        draw = ImageDraw.Draw(img_arquivo_entrada)        draw.text((left, top), f'{texto}', (corR, corG, corB), font=font)        print(f'salvando imagem {path_tmp}{nome_saida}_temp.png')        img_arquivo_entrada.save(f'{path_tmp}{nome_saida}_temp.png')        #print(f'removendo imagem {arquivo}')        #os.remove(f'{arquivo}')        print(f'movendo imagem {path_tmp}{nome_saida}_temp.png >> {arquivo}')        os.rename(f"{path_tmp}{nome_saida}_temp.png", f"{arquivo}")        print('\n')    ###############################################    def cortar_imagem(self, arquivo_entrada, arquivo_saida, esquerda, superior, direita, inferior):        print(f'arquivo_entrada {arquivo_entrada}, arquivo_saida {arquivo_saida}, esquerda {esquerda}, superior {superior}, direita {direita}, inferior {inferior}')        # exemplos robo stormtech_002        #self.util.criar_diretorio(self.util.pegar_caminho_diretorio_do_arquivo(f'{arquivo_saida}'))        # print('cortando 001')        self.criar_diretorio(self.pegar_caminho_diretorio_do_arquivo(f'{arquivo_saida}'))        # print('cortando 002')        #self.logger.info(f'recortando imagem {arquivo_entrada}')        print(f'recortando imagem {arquivo_entrada}')        # print('cortando 003')        img1 = Image.open(f'{arquivo_entrada}')        # print('cortando 004')        # esquerda, superior, direita, inferior = 300, 128, 1570, 625        time.sleep(0.3)        cropped_img = img1.crop((esquerda, superior, direita, inferior))        # print('cortando 005')        # self.logger.info(f'salvando imagem cortada {arquivo_saida}')        print(f'salvando imagem cortada {arquivo_saida}')        time.sleep(0.3)        # print('cortando 006')        cropped_img.save(f'{arquivo_saida}')        # print('cortando 007')        print('\n')        # self.logger.info(f'abrindo imagem para editar {arquivo_entrada}')        # font = ImageFont.truetype(f'{self.path_font}{font_ttf}', size)        # img_arquivo_entrada = Image.open(f'{arquivo_entrada}')        # draw = ImageDraw.Draw(img_arquivo_entrada)        # draw.text((left, top), f'{texto}', (corR, corG, corB), font=font)        # self.logger.info(f'salvando imagem {arquivo_saida}')        # img_arquivo_entrada.save(f'{arquivo_saida}')    ###############################################    #tipo= xpath ou id    def screenshot_elemento(self, tipo, elemento, driver, file_saida, dir_tmp, offset_width=0, offset_height=0):    #def screenshot_elemento(self, id, driver, file_saida, dir_tmp):        nome_saida=self.pegar_nome_arquivo(file_saida)        # exemplos robo stormtech_002        # https://seleniumwithjavapython.wordpress.com/selenium-with-java/code-snippets/screenshot-of-a-specific-element/        # http://www.software-testing-tutorials-automation.com/2015/01/how-to-capture-element-screenshot-using.html        # https://stackoverflow.com/questions/15510882/selenium-get-coordinates-or-dimensions-of-element-with-python        # https://tutorial.eyehunts.com/python/python-delete-file-remove-multiple-if-exists/        print(f'\ntipo: {tipo}')        print(f'file_saida: {file_saida}')        print(f'dir_tmp: {dir_tmp}')        print(f'elemento: {elemento}\n')        if f'{tipo}' == 'id':            print(f'\nlocalizando elemento: {elemento}')            # imagem=self.driver.find_element_by_xpath("//*[@id='post-22532']/div[1]/div[2]/div/div/p[25]/a/img")            #element = driver.find_element_by_xpath(f'{xpath}')            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, f"{elemento}")))        elif f'{tipo}' == 'xpath':            print(f'\nlocalizando elemento: {elemento}')            # imagem=self.driver.find_element_by_xpath("//*[@id='post-22532']/div[1]/div[2]/div/div/p[25]/a/img")            #element = driver.find_element_by_xpath(f'{elemento}')            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f"{elemento}")))            #element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, f"{id}")))        size_elemento_a=element.size        print(f'\n\n\nsize_elemento_a {size_elemento_a}')        #time.sleep(5)        image_width = int(element.size['width'])        image_height = int(element.size['height'])        location_x = int(element.location['x'])        location_y = int(element.location['y'])        print(f'image_width {image_width + offset_width}')        print(f'image_height {image_height + offset_height}')        print(f'location_x {location_x}')        print(f'location_y {location_y}')        #time.sleep(0.5)        self.criar_diretorio(dir_tmp)        driver.save_screenshot(f'{dir_tmp}{nome_saida}_temp.png')        #time.sleep(1.0)        self.cortar_imagem(f'{dir_tmp}{nome_saida}_temp.png', f'{file_saida}',location_x,location_y,location_x + image_width,location_y + image_height)        print(f'removendo file temp: {dir_tmp}{nome_saida}_temp.png')        time.sleep(0.5)        os.remove(f'{dir_tmp}{nome_saida}_temp.png')    def saindo_driver(self,driver,logger):        print('\n\n')        logger.info('1)Encerrando webdriver! ')        time.sleep(2)        try:            logger.info('saindo quit webdriver')            driver.quit()            logger.info('OK quit webdriver')        except:            logger.warning('saindo quit webdriver')        try:            logger.info('saindo exit webdriver')            driver.exit()            logger.info('OK exit webdriver')        except:            logger.warning('saindo exit webdriver')        try:            logger.info('saindo close webdriver')            driver.close()            logger.info('OK close webdriver')        except:            logger.warning('saindo close webdriver')        try:            logger.info('saindo stop webdriver')            driver.stop()            logger.info('OK stop webdriver')        except:            logger.warning('saindo stop webdriver')        try:            logger.info('saindo dispose webdriver')            driver.dispose()            logger.info('OK dispose webdriver')        except:            logger.warning('saindo dispose webdriver')        logger.info('2)Encerrado webdriver!!! ')        print('\n\n')        print('\n\n')        time.sleep(2)    ######################################    ########### adicionar novos abaixo com marcação de data e criador:    ######################################    ### enio: 12/08/2019    # def trocacor(self,int(r_in),int(g_in),int(b_in),img_in,int(r_out),int(g_out),int(b_out),img_out):    def trocacor(self,r_in,g_in,b_in,img_in,r_out,g_out,b_out,img_out):        r_in=int(r_in)        g_in=int(g_in)        b_in=int(b_in)        r_out=int(r_out)        g_out=int(g_out)        b_out=int(b_out)        print(f'input {r_in},{g_in},{b_in},{img_in}')        print(f'ouput {r_out},{g_out},{b_out},{img_out}')        # time.sleep(2.5)        ## alterador de cor de imagem        #parametros de rgb de entrada e saida        #caminho completo do arquivo de entrata e saida        #obs: o arquivo de saida pode ser o mesmo de entrada, assim será sobrescrito a imagem        print('im')        im = cv2.imread(f'{img_in}')        #rgb é invertido nessa função: bgr, por isso o [::-1] para inverter as listas, assim podemos passar os parametros rgb de forma normal        ####                 B  G   R                     B   G  R        #im[np.where((im == [255, 135, 0][::-1]).all(axis=2))] = [201, 41, 220][::-1]        print('im np')        # im[np.where((im == [r_in, g_in, b_in][::-1]).all(axis=2))] = [r_out, g_out, b_out][::-1]        im[np.where((im == [r_in, g_in, b_in][::-1]).all(axis=2))] = [r_out, g_out, b_out][::-1]        #im[np.where((im == [f'{b_in}', f'{g_in}', f'{r_in}']).all(axis=2))] = [f'{b_out}', f'{g_out}', f'{r_out}']        # im[np.where((im == [255, 135, 0]).all(axis=2))]        = [201, 41, 220]        # im[np.where((im == [255, 135, 0][::-1]).all(axis=2))] = [201, 41, 220][::-1]        print('cv2')        # cv2.imwrite(f'{img_out}_tmp', im)        cv2.imwrite(f'{img_out}', im)        # time.sleep(0.5)        # print('os rename')        # os.rename(f'{img_out}_tmp', f'{img_out}')        # print('os remove')        # time.sleep(0.5)        # os.remove(f"{img_out}_tmp")    ######################################