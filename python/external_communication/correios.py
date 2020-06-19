import requests
import re


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

def is_cod(cod):
    if re.match('^[a-zA-Z]{2}[0-9]{9}[a-zA-Z]{2}$', cod):
        return True
    return False


def is_valid(cod):
    return re.match('^[a-zA-Z]{2}[0-9]{9}[a-zA-Z]{2}$', cod)