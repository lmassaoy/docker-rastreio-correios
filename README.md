# docker-rastreio-correios

# About me!
(PT-BR) Este projeto tem como objetivo criar uma aplicação python rodando dentro de um container Docker (ou container em um cluster k8s utilizando uma imagem docker), onde essa aplicação recebe como parâmetro um código de rastreio de uma encomenda dos correios e sinalizará via Twitter Direct Message a mudança de status da remessa

### Tech stack planned for this project
[![docker-rastreio-correios-Architecture.png](https://i.postimg.cc/L5kNc6dj/docker-rastreio-correios-Architecture.png)](https://postimg.cc/jn5HNTSj)
#### Already implemented and working 'till QA :)
    [X] Python 3.X
    [X] Twitter API
    [X] Correios Webservice

### OK... but what do I do?
  - Capable to retrive the latest status or even the order history maintained by Brazilian mailing service (Correios)
  - Monitor a specific order and alert sending Direct Messages on Twitter when:
    - a new status update appears;
    - when the order is on its way its owner

### How to to use me ;)

Example:
```sh
$ python3 app.py -c OJ693674304BR -f trackOrder_v2
```
- -c = tracking code
- -f = consult method ('lastStatus'|'orderHistory'|orderTrack_v2)

Let's check the console!
[![Screen-Shot-2020-06-20-at-03-32-56.png](https://i.postimg.cc/FRYtXSG3/Screen-Shot-2020-06-20-at-03-32-56.png)](https://postimg.cc/FdXCj7MH)

and what happend on Twitter?
[![Screen-Shot-2020-06-20-at-03-26-28.png](https://i.postimg.cc/nhbPS564/Screen-Shot-2020-06-20-at-03-26-28.png)](https://postimg.cc/nC22CdVr)