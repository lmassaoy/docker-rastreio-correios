import datetime
import time
import argparse
import json
from external_communication.twitter_agent import TwitterBot
from external_communication.correios import Objeto, track, is_cod
 
 
def parseArgs():
    parser = argparse.ArgumentParser(
        prog='app',
        usage='%(prog)s [OPTIONS]',
        description='Script para rastrear pacotes dos correios'
    )

    parser.add_argument("-c", metavar="código da remessa", type=str, help="código da remessa para rastreio")
    parser.add_argument("-f", metavar="método de consulta", type=str, help="método de consulta desejado para rastreio")

    args = parser.parse_args()

    if args.c is None or args.f is None:
        parser.print_help()
        exit(1)

    return args


def consult_track_mode(method):
    switcher = {
        'lastStatus': 'show_last_status(obj)',
        'orderHistory': 'show_order_history(obj)'
    }
    method_chosed = switcher.get(method, 'invalid_function()')
    return method_chosed


def invalid_function():
    print('Oops! :( A função de rastreio escolhida não foi encontrada')

 
def get_status_message(status,order_tracking_code,obj):
    consult_datetime = str(datetime.datetime.now())[:19]
    status_not_found = f'Desulpe! :(\nNão foi encontrado o status do objeto {order_tracking_code}.\nHorário da Consulta: {consult_datetime}\n'
    
    switcher = {
        'delivery_on_going': f'YES! Objeto {order_tracking_code} já saiu para entrega :)\nHorário da Consulta: {consult_datetime}\n{get_last_status(obj)}\n',
        'delivered': f'Objeto {order_tracking_code} entregue ao destinatário!\nHorário da Consulta: {consult_datetime}\n{get_last_status(obj)}\n'
    }
    return switcher.get(status, status_not_found)


def get_event_data(event):
    event_description = event['descricao']
    event_date = event['data']
    event_time = event['hora']
    event_origin = event['unidade']['local'] + ' - ' + event['unidade']['cidade']
    message = f'''
    Status: {event_description}
    Data: {event_date} | Hora: {event_time}
    '''

    if 'destino' in event:
        event_target = event['destino'][0]['local'] + ' - ' + event['destino'][0]['cidade']
        origin_target = f'''Origem: {event_origin}\n    Destino: {event_target}\n'''
        message+=origin_target
    else:
        local = f"Local: {event_origin}\n"
        message+=local
 
    if 'detalhe' in event:
        detalhe = f"Detalhes: {event['detalhe']}\n"
        message+=detalhe
 
    return message  
    

def check_order_coming(obj):
    last_event = obj['objeto'][0]['evento'][0]['descricao']
    if "Objeto saiu" in last_event or "Objeto entregue" in last_event:
        return 1
    return 0


def show_last_status(obj):
    print(f"Último Status do Objeto: {obj['objeto'][0]['numero']}")
    print(get_last_status(obj))
    return None


def get_last_status(obj):
    message = get_event_data(obj['objeto'][0]['evento'][0])
    return message

  
def get_order_history(obj):
    event_list = [get_event_data(event) for event in obj['objeto'][0]['evento']]
    return event_list


def show_order_history(obj):
    print(f"Histórico do Objeto\nDetalhes sobre o trajeto do objeto {obj['objeto'][0]['numero']}\n")
    for message in get_order_history(obj):
        print(message)
    return None


def main():
    twitter_settings = json.load(open('settings/twitter_settings.json'))

    args = parseArgs()
    twitter_bot = TwitterBot(twitter_settings['api']['token'],twitter_settings['api']['token_secret'],
        twitter_settings['api']['consumer_key'],twitter_settings['api']['consumer_secret'])

    order_tracking_code = args.c
    consult_method = args.f

    if order_tracking_code:
        if is_cod(order_tracking_code):
            if(consult_method):
                # eval(consult_track_mode(consult_method))
                
                validator=0
                while(validator!=1):

                    obj = track(order_tracking_code).json

                    # Testing ["turn on" any sample]
                    # obj = json.load(open('test/sample_object_delivered.json'))
                    # obj = json.load(open('test/sample_object_delivery_on_going.json'))
                    # obj = json.load(open('test/sample_object_sent.json'))

                    print(f'Horário da Consulta: {str(datetime.datetime.now())[:19]}')
                    response=check_order_coming(obj)
                    if response == 1:  
                        last_status = get_last_status(obj)
                        if 'Objeto saiu' in last_status:
                            print(f'Objeto {order_tracking_code} saiu para entrega ao destinatário! :D')
                            message = get_status_message('delivery_on_going',order_tracking_code,obj)
                        else:
                            print(f'Objeto {order_tracking_code} entregue ao destinatário! :D')
                            message = get_status_message('delivered',order_tracking_code,obj) 
                        show_last_status(obj)
                        twitter_bot.send_direct(twitter_settings['target_username'],message)
                        validator = response
                    else:
                        show_last_status(obj)
                        message=f'Nada ainda! :( O objeto {order_tracking_code} ainda não saiu para entrega\nHorário da Consulta: {str(datetime.datetime.now())[:19]}\n{get_last_status(obj)}\n'
                        twitter_bot.send_direct(twitter_settings['target_username'],message)
                        time.sleep(15)
                        
        else:
            print('Código de rastreio inválido. Favor tentar novamente')    

if __name__ == '__main__':
    main()