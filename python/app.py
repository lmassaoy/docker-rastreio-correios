import requests
import re
import datetime
import time
import argparse
 
 
# Manual PDF: https://www.correios.com.br/a-a-z/pdf/rastreamento-de-objetos/manual_rastreamentoobjetosws.pdf
class Objeto(object):
    def __init__(self, *args, **kwargs):
        self.cepDestino = ""
        self.dataPostagem = ""
        self.eventos = list()
        self.numero = kwargs.get('numero', '')
        self.categoria = kwargs.get('categoria', '')
        self.sigla = kwargs.get('sigla', '')
        self.nome = kwargs.get('nome', '')
        self.json = ""
 
        if 'evento' in kwargs and len(kwargs.get('evento', list())) > 0:
            evento = kwargs.get('evento')[0]
            self.cepDestino = evento.get('cepDestino', '')
            self.dataPostagem = evento.get('dataPostagem', '')
 
            for evento in kwargs.get('evento', list()):
                self.eventos.append(Evento(**evento))
 
 
class Evento(object):
    def __init__(self, *args, **kwargs):
        self.tipo = kwargs.get('tipo', '')
        self.data = kwargs.get('data', '')
        self.hora = kwargs.get('hora', '')
        self.criacao = kwargs.get('criacao', '')
        self.prazoGuarda = kwargs.get('prazoGuarda', '')
        self.diasUteis = kwargs.get('diasUteis', '')
        self.descricao = kwargs.get('descricao', '')
        self.detalhe = kwargs.get('detalhe', '')
        self.status = kwargs.get('status', '')
 
        if 'unidade' in kwargs:
            self.unidade = Unidade(**kwargs.get('unidade', dict()))
 
        if 'destino' in kwargs and len(kwargs.get('destino', list())) > 0:
            self.destino = Destino(**kwargs.get('destino')[0])
 
        if 'detalheOEC' in kwargs:
            self.detalheOEC = OEC(**kwargs.get('detalheOEC', dict()))
 
 
class Unidade(object):
    def __init__(self, *args, **kwargs):
        self.tipounidade = kwargs.get('tipounidade', '')
        self.local = kwargs.get('local', '')
        self.sto = kwargs.get('sto', '')
        self.codigo = kwargs.get('codigo', '')
        self.uf = kwargs.get('uf', '')
        self.cidade = kwargs.get('cidade', '')
 
        if 'endereco' in kwargs:
            self.endereco = Endereco(**kwargs.get('endereco', dict()))
 
 
class Endereco(object):
    def __init__(self, *args, **kwargs):
        self.numero = kwargs.get('numero', '')
        self.cep = kwargs.get('cep', '')
        self.localidade = kwargs.get('localidade', '')
        self.bairro = kwargs.get('bairro', '')
        self.codigo = kwargs.get('codigo', '')
        self.logradouro = kwargs.get('logradouro', '')
        self.uf = kwargs.get('uf', '')
        self.latitude = kwargs.get('latitude', '')
        self.longitude = kwargs.get('longitude', '')
 
 
class Destino(object):
    def __init__(self, *args, **kwargs):
        self.bairro = kwargs.get('bairro', '')
        self.local = kwargs.get('local', '')
        self.cidade = kwargs.get('cidade', '')
        self.uf = kwargs.get('uf', '')
        self.codigo = kwargs.get('codigo', '')
 
        if 'endereco' in kwargs:
            self.endereco = Endereco(**kwargs.get('endereco', dict()))
 
 
class OEC(object):
    def __init__(self, *args, **kwargs):
        self.lista = kwargs.get('lista', '')
        self.longitude = kwargs.get('longitude', '')
        self.latitude = kwargs.get('latitude', '')
        self.carteiro = kwargs.get('carteiro', '')
        self.distrito = kwargs.get('distrito', '')
        self.unidade = kwargs.get('unidade', '')
 
        if 'endereco' in kwargs:
            self.endereco = Endereco(**kwargs.get('endereco', dict()))
 

def parseArgs():
    parser = argparse.ArgumentParser(
        prog='app',
        usage='%(prog)s [OPTIONS]',
        description='Script para rastrear pacotes dos correios'
    )

    parser.add_argument("-c", metavar="<codigo1[,codigo2,codigo3],...>", type=str, help="códigos para rastreio")
    parser.add_argument("-f", metavar="método de consulta", type=str, help="método de consulta desejado para rastreio")
    # parser.add_argument("-o", metavar="arquivo", type=str, help="arquivo de saida dos resultados")
    # parser.add_argument("-r", "--auto-remove", action="store_true", help="remove do arquivo objetos já entregues (apenas se usado com -f)")

    args = parser.parse_args()

    if args.c is None and args.f is None:
        parser.print_help()
        exit(1)

    return args

def is_cod(cod):
    if re.match('^[a-zA-Z]{2}[0-9]{9}[a-zA-Z]{2}$', cod):
        return True
    return False


def is_valid(cod):
    return re.match('^[a-zA-Z]{2}[0-9]{9}[a-zA-Z]{2}$', cod)


def consult_track_mode(method):
    switcher = {
        'lastStatus': 'show_last_status(obj)',
        'orderHistory': 'show_order_history(obj)'
    }
    method_chosed = switcher.get(method, 'invalid_function()')
    return method_chosed


def invalid_function():
    print('Oops! :( A função de rastreio escolhida não foi encontrada')

 
def generate_valid_code(cod, with_cep=False):
    cod = cod.strip()
 
    if len(cod) < 12 or 13 < len(cod):
        return ""
 
    prefix = cod[0:2]
    number = cod[2:10]
    suffix = cod[-2:]
    multipliers = [8, 6, 4, 2, 3, 5, 9, 7]
 
    if len(number) < 8 and len(cod) == 12:
        diff = 8 - len(number)
        zeros = "0" * diff
        number = zeros + number
 
    sum_ = sum(int(number[i]) * multipliers[i] for i in range(8))
    rest = sum_ % 11
 
    if rest == 0:
        verifying_digit = "5"
    elif rest == 1:
        verifying_digit = "0"
    else:
        verifying_digit = str(11 - int(rest))
 
    valid_code = prefix + number + verifying_digit + suffix
 
    if with_cep:
        obj = track(valid_code)
        return valid_code, str(obj.cepDestino)
 
    return valid_code
 
 
def track(cod):
    if not is_valid(cod):
        return None
 
    body = '''
   <rastroObjeto>
       <usuario>MobileXect</usuario>
       <senha>DRW0#9F$@0</senha>
       <tipo>L</tipo>
       <resultado>T</resultado>
       <objetos>{obj}</objetos>
       <lingua>101</lingua>
       <token>QTXFMvu_Z-6XYezP3VbDsKBgSeljSqIysM9x</token>
   </rastroObjeto>
   '''
 
    r = requests.post('http://webservice.correios.com.br/service/rest/rastro/rastroMobile',
                      data=body.format(obj=cod),
                      headers={'Content-Type': 'application/xml'})
 
    if r.status_code == 200:
        result = r.json().get('objeto', list())
        if result:
            obj = Objeto(**result[0])
            obj.json = r.json()
            return obj
 
    return None
 

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
    last_event = obj.json['objeto'][0]['evento'][0]['descricao']
    if "Objeto saiu" in last_event:
        return 1
    return 0


def show_last_status(obj):
    print(f"Último Status do Objeto: {obj.json['objeto'][0]['numero']}")
    print(get_last_status(obj))
    return None


def get_last_status(obj):
    message = get_event_data(obj.json['objeto'][0]['evento'][0])
    return message

  
def get_order_history(obj):
    event_list = [get_event_data(event) for event in obj.json['objeto'][0]['evento']]
    return event_list


def show_order_history(obj):
    print(f"Histórico do Objeto\nDetalhes sobre o trajeto do objeto {obj.json['objeto'][0]['numero']}\n")
    for message in get_order_history(obj):
        print(message)
    return None


if __name__ == '__main__':
    args = parseArgs()
    order_tracking_code = args.c
    consult_method = args.f
    if order_tracking_code:
        if is_cod(order_tracking_code):
            if(consult_method):
                obj = track(order_tracking_code)
                # execute the method choosed
                eval(consult_track_mode(consult_method))
        else:
            print('Código de rastreio inválido. Favor tentar novamente')

    # validator=0
    # while(validator!=1):
    #     print(f'exec: {datetime.datetime.now()}')
    #     response=check_order_coming(obj)
    #     if response == 1:
    #         print(f'Objeto {cod} saiu para entrega ao destinatário! :D')
    #         show_last_status(obj)
    #     else:
    #         show_last_status(obj)
    #     time.sleep(60)