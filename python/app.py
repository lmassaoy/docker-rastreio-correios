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
        'lastStatus': 'show_last_status(order_tracking_code)',
        'orderHistory': 'show_order_history(order_tracking_code)',
        'trackOrder': 'order_tracking(order_tracking_code)',
        'trackOrder_v2': 'order_tracking_v2(order_tracking_code)'
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
        'delivered': f'Objeto {order_tracking_code} entregue ao destinatário! :)\nHorário da Consulta: {consult_datetime}\n{get_last_status(obj)}\n'
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


def show_last_status(order_tracking_code):
    obj = track(order_tracking_code).json
    print(f"Último Status do Objeto: {obj['objeto'][0]['numero']}")
    print(get_last_status(obj))
    return None


def get_last_status(obj):
    message = get_event_data(obj['objeto'][0]['evento'][0])
    return message

  
def get_order_history(obj):
    event_list = [get_event_data(event) for event in obj['objeto'][0]['evento']]
    return event_list


def show_order_history(order_tracking_code):
    obj = track(order_tracking_code).json
    print(f"Histórico do Objeto\nDetalhes sobre o trajeto do objeto {obj['objeto'][0]['numero']}\n")
    for message in get_order_history(obj):
        print(message)
    return None


def order_tracking(order_tracking_code):
    twitter_settings = json.load(open('settings/twitter_settings.json'))
    twitter_bot = TwitterBot(twitter_settings['api']['token'],twitter_settings['api']['token_secret'],
        twitter_settings['api']['consumer_key'],twitter_settings['api']['consumer_secret'])
    validator=0
    consult_counter=0

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
                print(f'Objeto {order_tracking_code} saiu para entrega ao destinatário! :)')
                message = get_status_message('delivery_on_going',order_tracking_code,obj)
            else:
                print(f'Objeto {order_tracking_code} entregue ao destinatário! :)')
                message = get_status_message('delivered',order_tracking_code,obj) 
            
            # Print in console
            show_last_status(order_tracking_code)
            twitter_bot.send_direct(twitter_settings['target_username'],message)
            validator = response
        else:
            consult_counter+=1
            counter_message = f'Consulta #{consult_counter} realizada\n'
            if consult_counter == 1:
                show_last_status(order_tracking_code)
                message=f'Nada ainda! :( O objeto {order_tracking_code} ainda não saiu para entrega\nHorário da Consulta: {str(datetime.datetime.now())[:19]}\n{get_last_status(obj)}\n'
                twitter_bot.send_direct(twitter_settings['target_username'],message)
                print(counter_message)
            else:
                print(counter_message)
            time.sleep(10)


def order_tracking_v2(order_tracking_code):
    twitter_settings = json.load(open('settings/twitter_settings.json'))
    twitter_bot = TwitterBot(twitter_settings['api']['token'],twitter_settings['api']['token_secret'],
        twitter_settings['api']['consumer_key'],twitter_settings['api']['consumer_secret'])

    loop_control = 1
    validator = 0

    while(validator!=1):
        obj = track(order_tracking_code).json

        # Testing ["turn on" any sample]
        # obj = json.load(open('test/sample_object_delivered.json'))
        # obj = json.load(open('test/sample_object_delivery_on_going.json'))
        # obj = json.load(open('test/sample_object_sent.json'))

        # Validate if the latest status is delivered done or on going
        response=check_order_coming(obj)
        if response == 1:
                last_status = get_last_status(obj)
                if 'Objeto saiu' in last_status:
                    message = get_status_message('delivery_on_going',order_tracking_code,obj)
                else:
                    message = get_status_message('delivered',order_tracking_code,obj)
                print(message)
                twitter_bot.send_direct(twitter_settings['target_username'],message)
                validator = response
        else:
            print(f'Ainda não foi entregue :( | Horário da Consulta: {str(datetime.datetime.now())[:19]}')
            if loop_control == 1:
                latest_event = obj['objeto'][0]['evento'][0]
                latest_event_description = latest_event['descricao']
                latest_event_date = latest_event['data']
                latest_event_time = latest_event['hora']
                latest_event_origin = latest_event['unidade']['local'] + ' - ' + latest_event['unidade']['cidade']

                message=f'Nada ainda! :( O objeto {order_tracking_code} ainda não saiu para entrega\nHorário da Consulta: {str(datetime.datetime.now())[:19]}\n{get_last_status(obj)}\n'
                twitter_bot.send_direct(twitter_settings['target_username'],message)
            else:               
                try:
                    next_to_last_event_description = latest_event_description
                    next_to_last_event_date = latest_event_date
                    next_to_last_event_time = latest_event_time
                    next_to_last_event_origin = latest_event_origin

                    latest_event = obj['objeto'][0]['evento'][0]
                    latest_event_description = latest_event['descricao']
                    latest_event_date = latest_event['data']
                    latest_event_time = latest_event['hora']
                    latest_event_origin = latest_event['unidade']['local'] + ' - ' + latest_event['unidade']['cidade']

                    last_status = f'Latest status:\nDescription: {latest_event_description}\nDate: {latest_event_date}\nTime: {latest_event_time}\nLocal: {latest_event_origin}\n'                
                    if latest_event_description != next_to_last_event_description or latest_event_date != next_to_last_event_date or latest_event_time != next_to_last_event_time or latest_event_origin != next_to_last_event_origin:
                        print('Houve uma atualização no status! :)\n')
                        print(f'Descrição anterior: {next_to_last_event_description} >> Descrição atualizada: {latest_event_description}')
                        print(f'Data anterior: {next_to_last_event_date} >> Data atualizada: {latest_event_date}')
                        print(f'Hora anterior: {next_to_last_event_time} >> Hora atualizada: {latest_event_time}')
                        print(f'Origem anterior: {next_to_last_event_origin} >> Origem atualizada: {latest_event_origin}\n')

                        message=f'Houve uma atualização no status do objeto {order_tracking_code}! :)\nHorário da Consulta: {str(datetime.datetime.now())[:19]}\n{get_last_status(obj)}\n'
                        twitter_bot.send_direct(twitter_settings['target_username'],message)
                except IndexError:
                    time.sleep(0.01)     
            
            loop_control+=1

            time.sleep(600)
    

def main():
    args = parseArgs()
    order_tracking_code = args.c
    consult_method = args.f

    if order_tracking_code:
        if is_cod(order_tracking_code):
            if(consult_method):
                eval(consult_track_mode(consult_method))
        else:
            print('Código de rastreio inválido. Favor tentar novamente')    

if __name__ == '__main__':
    main()