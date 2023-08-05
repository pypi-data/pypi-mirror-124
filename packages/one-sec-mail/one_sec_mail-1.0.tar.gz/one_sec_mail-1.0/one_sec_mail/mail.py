import requests as rq
import json

url = "https://www.1secmail.com/api/v1/"


def get_random_mail(count=1):
    """
    Возвращает один или несколько случайных почтовых адресов
    
    Args:
        count (int, optional): Количество адресов, которые нужно вернуть
    
    Returns:
        str | list: адреса
    """
    mails = rq.get(url, params={'action': 'genRandomMailbox', 'count': count}).json()

    return mails

def get_domain_list():
    """
    Возвращает доступные почтовые домены
    
    Returns:
        list: Список доступных доменов
    """
    return rq.get(url, params={'action': 'getDomainList'}).json()




class Mail:
    """
    Класс почты
    """
    
    def __init__(self, mail=None):
        """
        Создает почту, если не передан адрес, создает случайный
        
        Args:
            mail (None, optional): Адрес почты
        """
        domains = get_domain_list()
        if not mail:
            mail = get_random_mail()[0]
        elif '@' not in mail:
            mail += '@' + domains[0]
        elif mail.split('@')[-1] not in domains:
            mail = mail.split('@')[0] + '@' + domains[0]

        self.mail = mail

    def check(self):
        """
        Возвращает список писем
        
        Returns:
            list: Каждый элемент списка - словарь

                id: id письма
                from: Почта отправителя
                subject: Тема
                date: Дата получения
        """
        mail = self.mail
        login, domain = mail.split('@')
        return rq.get(url, params={'action': 'getMessages', 'login': login, 'domain': domain}).json()

    def get_letter(self, let_id):
        """
        Получает письмо
        
        Args:
            let_id (int): id письма
        
        Returns:
            dict: Словарь, содержащий всю информацию о письме

                id: id письма
                from: Почта отправителя
                subject: Тема
                date: Дата получения
                attachments: Список приложений (словарь каждое)

                    filename: Имя приложения
                    contentType: Тип приложения
                    size: Размер приложения
                body: Тело сообщения (html, если существует, текст в противном случае)
                textBody: Тело сообщения (текст)
                htmlBody: Тело сообщения (html)
        """
        mail = self.mail
        login, domain = mail.split('@')
        return rq.get(url, params={'action': 'readMessage', 'login': login, 'domain': domain, 'id': let_id}).json()

    def get_attachment(self, let_id, file):
        """
        Возвращает файл приложенный к письму

        Args:
            let_id (type): id письма
            file (type): Название файла
        
        Returns:
            str: файл ввиде байт
        """
        mail = self.mail
        login, domain = mail.split('@')
        return rq.get(url, params={'action': 'download', 'login': login, 'domain': domain, 'id': let_id, 'file': file}).content

    def download_attachment(self, let_id, file, path, new_name=None):
        """
        Скачивает приложенный к письму файл
        
        Args:
            let_id (int): id письма
            file (str): Название файла
            path (str): Путь к папке, куда скачивать
        """
        if not new_name:
            new_name = file
        file = file.strip('/\\')
        with open(path+'/'+new_name, 'wb') as f:
            f.write(self.get_attachment(let_id, file, mail))

    def __str__(self):
        return self.mail




            
