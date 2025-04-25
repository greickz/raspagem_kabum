from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
import pandas as pd
import time

caminho = r"C:\Program Files\chromedriver-win64\chromedriver-win64\chromedriver.exe"

servico = Service(caminho)
controle = webdriver.ChromeOptions()
controle.add_argument('--disable-gpu')
controle.add_argument('--window-size=1920,1080')

executador = webdriver.Chrome(service=servico, options=controle)

url_site = 'https://www.kabum.com.br/busca/console'
executador.get(url_site)
time.sleep(5)

produtos = {'titulo': [], 'preco': [], 'parcela': []}
pagina_atual = 1

while True:
    print(f'\nColetando dados da página {pagina_atual}...')



    try:
        cards = WebDriverWait(executador, 10).until(
        ec.presence_of_all_elements_located((By.CLASS_NAME, 'productCard'))
    )
        print('Cards encontrados com sucesso.')
        primeiro_card = cards[0]
        executador.execute_script("arguments[0].scrollIntoView();", primeiro_card)
        time.sleep(1)
        primeiro_card.click()
        print('Clique no card realizado com sucesso.')
        time.sleep(5)
    #     armazenamento = executador.find_element(
    # By.XPATH, '//div[@class="GiPKU"]/p[starts-with(normalize-space(.), "- Memória")]'
# )
        
    except Exception as e:
        print(f'Ocorreu um erro ao tentar clicar no card: {e}')













    try:
        WebDriverWait(executador, 10).until(
            ec.presence_of_all_elements_located((By.CLASS_NAME, 'productCard'))
        )
        print('Elementos encontrados com sucesso')
    except TimeoutException:
        print('Tempo de espera excedido')
        break

    executador.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    elementos = executador.find_elements(By.CLASS_NAME, 'productCard')

    for i, produto in enumerate(elementos):
        try:
            nome = produto.find_element(By.CLASS_NAME, 'nameCard').text.strip()
            preco = produto.find_element(By.CLASS_NAME, 'priceCard').text.strip()
            parcela = produto.find_element(By.CLASS_NAME, 'priceTextCard').text.strip()
            print(f'{i + 1}. {nome} - {preco}')
            produtos['titulo'].append(nome)
            produtos['preco'].append(preco)
            produtos['parcela'].append(parcela)
        except Exception as e:
            print(f'Erro ao coletar dados do produto {i + 1}: {e}')

    try:
        proxima_pag = WebDriverWait(executador, 10).until(
            ec.element_to_be_clickable((By.CLASS_NAME, 'nextLink'))
        )
        if proxima_pag:
            executador.execute_script('arguments[0].scrollIntoView();', proxima_pag)
            time.sleep(1)
            executador.execute_script('arguments[0].click();', proxima_pag)
            print(f'Indo para a próxima página ({pagina_atual + 1})')
            pagina_atual += 1
            time.sleep(5)
        else:
            print('Você chegou na última página')
            break
    except Exception as e:
        print('Erro ao tentar avançar para a próxima página:', e)
        break
    




df = pd.DataFrame(produtos)
duplicadas = df[df.duplicated(subset=['titulo'], keep=False)]

print(f'\nTotal de produtos duplicados encontrados: {len(duplicadas)}')
if not duplicadas.empty:
    print('\nProdutos duplicados:')
    print(duplicadas[['titulo', 'preco', 'parcela']].to_string(index=False))
else:
    print('Nenhuma duplicata encontrada.')

executador.quit()

print(f'\nTotal coletado (com possíveis duplicatas): {len(df)}')

df_sem_duplicatas = df.drop_duplicates(subset=['titulo'], keep='first')
print(f'Total após remoção de duplicatas: {len(df_sem_duplicatas)}')

df_sem_duplicatas.to_excel('consoles.xlsx', index=False)
print(f'Arquivo "consoles.xlsx" salvo com sucesso! ({len(df_sem_duplicatas)} produtos únicos)')

