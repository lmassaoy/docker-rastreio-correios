# docker-rastreio-correios

# About me!
(PT-BR) Este projeto tem como objetivo criar uma aplicação python rodando dentro de um container Docker (ou container em um cluster k8s utilizando uma imagem docker), onde essa aplicação recebe como parâmetro um código de rastreio de uma encomenda dos correios e sinalizará via Twitter Direct Message a mudança de status da remessa

(English) This projects has as its goal to create a python application inside a Docker container (or a container inside a k8s cluster using a docker image), where this application receives as parameter a tracking code of an order of Brazilian mailing service and will send a Twitter Direct Message when a change of status happens

### Tech stack planned for this project
[![docker-rastreio-correios-Architecture-1.png](https://i.postimg.cc/Y0t7zPfR/docker-rastreio-correios-Architecture-1.png)](https://postimg.cc/ftq1wBPS)

#### Already implemented and working 'till QA :)
    [X] Python 3.X
    [X] Twitter API
    [X] Correios Webservice
    [X] Docker

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
- -f = consult method ('lastStatus'|'orderHistory'|'trackOrder_v2')

### Let's check the console!

[![Screen-Shot-2020-06-22-at-02-41-57.png](https://i.postimg.cc/vZ2mHGLs/Screen-Shot-2020-06-22-at-02-41-57.png)](https://postimg.cc/tsPbBQMS)

### and what happend on Twitter?

[![Screen-Shot-2020-06-20-at-03-26-28.png](https://i.postimg.cc/nhbPS564/Screen-Shot-2020-06-20-at-03-26-28.png)](https://postimg.cc/nC22CdVr)

### TIME TO DOCKERIZE

Keep in mind the trick here is the environment variables!
You gonna need to set your Twitter API token and consumer data, your Twitter username, your tracking code and finally the function you wanna to execute.

#### build the Docker image

```sh
$ docker build -t docker-rastreio-correios .
```

[![Screen-Shot-2020-06-22-at-05-26-55.png](https://i.postimg.cc/Tw3d5xTv/Screen-Shot-2020-06-22-at-05-26-55.png)](https://postimg.cc/d7gPgz75)

### now you run your Docker container

```sh
$ docker run --env-file devops/env.list docker-rastreio-correios
```

[![Screen-Shot-2020-06-22-at-05-27-35.png](https://i.postimg.cc/5t1N1vG0/Screen-Shot-2020-06-22-at-05-27-35.png)](https://postimg.cc/QF4rJBjG)

### check your Twitter :)

[![Screen-Shot-2020-06-22-at-05-27-50.png](https://i.postimg.cc/HL2WLnDt/Screen-Shot-2020-06-22-at-05-27-50.png)](https://postimg.cc/R3WxsM03)