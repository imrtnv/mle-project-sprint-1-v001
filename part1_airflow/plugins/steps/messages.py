# plugins/steps/messages.py
from airflow.providers.telegram.hooks.telegram import TelegramHook

def send_telegram_failure_message(context): # на вход принимаем словарь со контекстными переменными
    hook = TelegramHook(telegram_conn_id='test',
                        token='8124879025:AAHIUMYmjnpsmnznd7es7HYTJGG7RXX4SKs',
                        chat_id='252457155')
    dag = context['dag']
    run_id = context['run_id']
    

    
    message = f'Исполнение DAG прошла не успешно!' # определение текста сообщения
    hook.send_message({
        'chat_id': '252457155',
        'text': message
    })

def send_telegram_success_message(context): # на вход принимаем словарь со контекстными переменными
    hook = TelegramHook(telegram_conn_id='test',
                        token='8124879025:AAHIUMYmjnpsmnznd7es7HYTJGG7RXX4SKs',
                        chat_id='252457155')
    dag = context['dag']
    run_id = context['run_id']
    
    message = f'Исполнение DAG прошло успешно!' # определение текста сообщения
    hook.send_message({
        'chat_id': '252457155',
        'text': message
    }) # отправление сообщения
