# Extrator de processos dos cadernos do TST


## Proposta/Briefing

Dado o link do tribunal abaixo, capture:
 - Baixar os cadernos do TST da última semana
 - Extrair os números de processo de cada caderno
 - Gerar planilhas de saída com todos os números de processos separados por dia da semana
o Ex. TST 13/10/2022.xlsx
 - Caso um processo apareça repetido em mais de um dia, gerar relatório de duplicatas com os respectivos processos e suas datas.

Link do tribunal: [https://dejt.jt.jus.br/dejt/f/n/diariocon](https://dejt.jt.jus.br/dejt/f/n/diariocon)

### Mapeamento do processo para extração

#### Input e pesquisa dos cadernos
1. abrir url [https://dejt.jt.jus.br/dejt/f/n/diariocon](https://dejt.jt.jus.br/dejt/f/n/diariocon)
2. localizar dropdown do campo "Órgão":
   1. xpath:  ```//select[@id='corpo:formulario:tribunal']```
   2. usar o id "corpo:formulario:tribunal"
3. localizar o value TST
   1. xpath: ```//*[@id="corpo:formulario:tribunal"]/option[2]```
   2. atualmente está no value="0"
      1. o melhor é mapear pela string "TST"
4. inserir a data no campo "Data de Inicio"
   1. ```//input[@id='corpo:formulario:dataIni']```
   2. usar o id 'corpo:formulario:dataIni' 
5. inserir a data no campo "Data de Fim"
   1. ```//input[@id='corpo:formulario:dataFim']```
   2. usar o id 'corpo:formulario:dataFim'
6. clicar no botão Pesquisar
   1. mapear o xpath ```//div[@class='plc-corpo-acao-t'][contains(.,'Pesquisar')]```

#### Coleta dos resultados:  

##### Em caso de erro:
1. verificar se há erro:  
   1. xpath: ```//p[contains(.,'Nenhum registro que atende aos critérios informados foi encontrado! Refine a pesquisa por outro parâmetro!')]```
         1. talvez mapear por pelo menos uma palavra chave: "Nenhum"
      2. ou ainda melhor, pegar pelo id "corpo:formulario:ajaxMensagem"
         1. xpath: ```//*[@id="corpo:formulario:ajaxMensagem"]```
            1. ⚠️Atenção: se tudo estiver ok, o conteudo está em branco sem texto

##### Em caso de Sucesso:
1. se não houver mensagem no ```id="corpo:formulario:ajaxMensagem"``` e tiver resultado para baixar:
   1. localizar quantos arquivos aparecem nas linhas tr ```//*[@id="diarioCon"]//table[contains(@class,'plc-table-tabsel plc-table-tabsel plc-table-tabsel plc-table-tabsel plc-table-tabsel delimitador tabelaSelecao')]//tr```
   2. captura as informações do primeiro td com a Data do arquivo ```//*[@id="diarioCon"]//table[contains(@class,'plc-table-tabsel plc-table-tabsel plc-table-tabsel plc-table-tabsel plc-table-tabsel delimitador tabelaSelecao')]//tr/td[1]```
   3. captura as informações do segundo td com o Nome do arquivo ```//*[@id="diarioCon"]//table[contains(@class,'plc-table-tabsel plc-table-tabsel plc-table-tabsel plc-table-tabsel plc-table-tabsel delimitador tabelaSelecao')]//tr/td[2]```
   4. captura as informações do terceiro td com o button de download do arquivo ```//*[@id="diarioCon"]//table[contains(@class,'plc-table-tabsel plc-table-tabsel plc-table-tabsel plc-table-tabsel plc-table-tabsel delimitador tabelaSelecao')]//tr/td[3]```
2. ⚠️Atenção: tem que observar que quando ultrapassa 30 arquivos, cria uma nova pagina com os proximos arquivos. Acredito que 7 dias não ultrapassará 30 arquivos, mas é bom deixar mapeado.
   1. identificar se há pelo menos um botão de proxima página ```(//span[contains(@class,'ico iNavProximo')])```
      2. enquanto houver, clica no primeiro para avançar ```(//span[contains(@class,'ico iNavProximo')])[1]```
   2. quando não tiver mais botão de avançar, é porque acabou as páginas.
3. ⚠️quando trocar de página, testar se o texto do ```//*[@id="diarioNav"]/table/tbody/tr/td[2]``` muda de uma página para outra antes de começar a baixar os arquivos.

#### Tratamento dos arquivos pdfs baixados
1. salvar os pdfs em um TMP
2. extrair os textos dos pdfs
3. fazer um parser e capturar as propostas como no exemplo ```Processo Nº CorPar-1000794-13.2022.5.00.0000```
   1. normalmente há uma quebra de linha antes
   2. a linha começa por ```Processo Nº ``` e termina com um número ```[0-9]```
   3. atenção para falso positivo do "Processo Nº" no meio de textos que não um "título"

    <picture>
      <img alt="exemplo de processo" src="img/exemplo_processo.png">
    </picture>
    <picture>
      <img alt="exemplo de processo" src="img/exemplo_processo2.png">
    </picture>
    <picture>
      <img alt="exemplo de falso positivo" src="img/exemplo_falso_positivo.png">
    </picture>
   
