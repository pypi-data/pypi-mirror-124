(Below in Russian)
# OneSecMail - Create a one-time mail to receive the message

## Get a list of available domains
``` Python
from onesecmail import get_domain_list

domains = get_domain_list()  # Returns a list of available domains
print(domains)
```

Returns:
- List of available domains

## Get a list of email addresses
``` Python
from onesecmail import get_random_mail

domains = get_random_mail(count=1)  # Returns a list of random emails
print(domains)
```

Accepts:
- The number of addresses to be created (by default 1)

Returns:
- List of e-mail addresses

## Create a mail
``` Python
from onesecmail import Mail

email = Mail(mail='name@domein.com')
print(email)  # Displays the created mail
```

Accepts:
- Email address or name (created automatically by default)

Returns:
- Mail Object

## Get a list of emails in the e-mail
``` Python
from onesecmail import Mail

email = Mail()
email.check()
```

Returns:
- List of dictionaries, each dictionary - information about the letter:

``` Python
{
    'id': 123454321,               # email id
    'from': 'name@domein.com',     # sender's email
    'subject': 'theme',            # Subject of the letter
    'date': '2021-10-19 17:25:38'  # Date of receipt
}
```

## Receive an e-mail
``` Python
from onesecmail import Mail

email = Mail()
letter = email.get_letter(let_id=123454321)
```

Accepts:
- id of the required email

Returns:
- Dictionary with all the information about the letter and the files attached to the letter

``` Python
{
    'id': 123454321,                # email id
    'from': 'name@domein.com',      # sender's email
    'subject': 'theme',             # Subject of the letter
    'date': '2021-10-19 17:25:38',  # Date of receipt
    'attachments':                  # List of files attached to the letter
        [
            {
                'filename': 'image.png',     # File name
                'contentType': 'image/png',  # File Type
                'size': 2048                 # File size in kilobytes
            }
        ]
    'body': '<p>Тело письма</p>',     # Message body (html if exists, text otherwise)
    'textBody': 'Тело письма'         # Message body (text)
    'htmlBody': '<p>Тело письма</p>'  # Message body (html)
}
```

## Get the files attached to the email
``` Python
from onesecmail import Mail

email = Mail()
attachment = email.get_attachment(let_id=123454321, file='image.png')
```

Accepts:
- E-mail id
- The name of the desired file

Returns:
- The contents of the file attached to the letter (bytes)

## Download the attached file
``` Python
from onesecmail import Mail

email = Mail()
email.download_attachment(let_id=123454321, file='image.png', path='C:/', new_name='img.png')
```

Accepts:
- E-mail id
- The name of the desired file
- The path to the folder where you want to download the file
- If necessary, a new file name (by default swings with the old name)

(**Can't create folders, specify the path to an existing folder**)

Downloads the file to the specified folder

---
# OneSecMail - Создайте одноразовую почту

## Получите список доступных доменов
``` Python
from onesecmail import get_domain_list

domains = get_domain_list()  # Вернет список доступных доменов
print(domains)
```

Возвращает:
- Список доступных доменов

## Получите список почтовых адресов
``` Python
from onesecmail import get_random_mail

domains = get_random_mail(count=1)  # Вернет список случайных почт
print(domains)
```

Принимает:
- Количество создаваемых адресов (по умолчанию 1)

Возвращает:
- Список e-mail адресов

## Создайте почту
``` Python
from onesecmail import Mail

email = Mail(mail='name@domein.com')
print(email) # Выведет созданную почту
```

Принимает:
- Адрес почты или название (по умолчанию создается автоматически)

Возвращает:
- Объект почты

## Получите список писем на почте
``` Python
from onesecmail import Mail

email = Mail()
email.check()
```

Возвращает:
- Список словарей, каждый словарь - информация о письме:

``` Python
{
    'id': 123454321,               # id письма
    'from': 'name@domein.com',     # email отправителя
    'subject': 'theme',            # Тема письма
    'date': '2021-10-19 17:25:38'  # Дата получения
}
```

## Получите письмо
``` Python
from onesecmail import Mail

email = Mail()
letter = email.get_letter(let_id=123454321)
```

Принимает:
- id нужного письма

Возвращает:
- Словарь со всей информацией о письме и файлах приложенных к письму

``` Python
{
    'id': 123454321,                # id письма
    'from': 'name@domein.com',      # email отправителя
    'subject': 'theme',             # Тема письма
    'date': '2021-10-19 17:25:38',  # Дата получения
    'attachments':                  # Список файлов приложенных к письму
        [
            {
                'filename': 'image.png',     # Название файла
                'contentType': 'image/png',  # Тип файла
                'size': 2048                 # Размер файла в килобайтах
            }
        ]
    'body': '<p>Тело письма</p>',     # Тело сообщения (html, если существует, текст в противном случае)
    'textBody': 'Тело письма'         # Тело сообщения (текст)
    'htmlBody': '<p>Тело письма</p>'  # Тело сообщения (html)
}
```

## Получите файлы приложенные к письму
``` Python
from onesecmail import Mail

email = Mail()
attachment = email.get_attachment(let_id=123454321, file='image.png')
```

Принимает: 
- id письма
- Название нужного файла

Возвращает:
- Содержание приложенного к письму файла (байты)

## Скачайте приложенный файл
``` Python
from onesecmail import Mail

email = Mail()
email.download_attachment(let_id=123454321, file='image.png', path='C:/', new_name='img.png')
```

Принимает:
- id письма
- Название нужного файла
- Путь к папке, куда надо скачать файл
- Если надо, новое название файла (по умолчанию скачается со старым названием)

(**Не может создавать папки, указывайте путь к существующей папке**)

Скачивает файл в указанную папку