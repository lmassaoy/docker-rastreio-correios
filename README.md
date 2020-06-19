# docker-rastreio-correios

# About me!

![Luis Yamada](https://lyamada-image-repo.s3.amazonaws.com/docker-rastreio-correios.png)

### Tech stack planned for this project
    - Python 3.X
    - Twitter API
    - Correios Webservice
    - Docker
    - Kubernetes
### OK... but what do I do?
  - Capable to retrive order history maintained by Brazilian mailing service (Correios)
  - Monitor a specific order and alert sending Direct Messages on Twitter when:
    - a new status update appears;
    - when the order is on its way its owner
### How to use me

Example:
```sh
$ python3 app.py -c OJ693674304BR -f lastStatus
```
- -c = tracking code
- -f = consult method ('lastStatus'|'orderHistory')