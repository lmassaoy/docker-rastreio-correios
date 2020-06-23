# docker-rastreio-correios

# About me!
The goal of this project is to run a Python application inside a Docker container (or a container inside a k8s cluster using a docker image) to track a Brazilian post office's order.

This application receives as parameters (reading from environment variables):
- a tracking code of an order of Brazilian post offices
- a method to track or inform the order's status

Also is neeeded to provide (as environment variables) a Twitter's API credentials kit (token, token secret, consumer key and consumer key secret) and a Twitter's username who will receive the status information of the tracked order via Direct Message, informing updates about the order's status.
If you choose to monitor the order, keep in mind the last update the application will send is when the order left the post office towards your home :)

# Tech stack used in this project
[![docker-rastreio-correios-Architecture-1.png](https://i.postimg.cc/Y0t7zPfR/docker-rastreio-correios-Architecture-1.png)](https://postimg.cc/ftq1wBPS)

## Ready to use! (so far so good)
    [X] Python 3.X
    [X] Twitter API
    [X] Correios Webservice
    [X] Docker
    [X] Kubernetes

## How to use this application
### Locally
Example:
```sh
$ python3 app.py -c OJ693674304BR -f trackOrder_v2
```
- -c = tracking code
- -f = consult method
    - 'lastStatus': shows in console the latest status of the order
    - 'orderHistory': shows in console the history status the order
    - 'trackOrder_v2': starts to monitor the tracking code, sending Twitter's Direct Message everytime an update in the order's status appears

#### Console output

[![Screen-Shot-2020-06-22-at-02-41-57.png](https://i.postimg.cc/vZ2mHGLs/Screen-Shot-2020-06-22-at-02-41-57.png)](https://postimg.cc/tsPbBQMS)

#### and what happend on Twitter?

[![Screen-Shot-2020-06-20-at-03-26-28.png](https://i.postimg.cc/nhbPS564/Screen-Shot-2020-06-20-at-03-26-28.png)](https://postimg.cc/nC22CdVr)

### Docker
#### Build the Docker image
```sh
$ docker build -t docker-rastreio-correios .
```
[![Screen-Shot-2020-06-22-at-05-26-55.png](https://i.postimg.cc/Tw3d5xTv/Screen-Shot-2020-06-22-at-05-26-55.png)](https://postimg.cc/d7gPgz75)

#### now you run your Docker container!
The trick here is: the environment variables! You gonna need to set your Twitter API token and consumer data, your Twitter username (or who you want to receive the DMs), your tracking code and finally the function you wanna to execute.
Now 'env.list' will do the trick :)
```sh
$ docker run --env-file devops/env.list docker-rastreio-correios
```
#### Console output
[![Screen-Shot-2020-06-22-at-05-27-35.png](https://i.postimg.cc/5t1N1vG0/Screen-Shot-2020-06-22-at-05-27-35.png)](https://postimg.cc/QF4rJBjG)

#### Checking Twitter inbox
[![Screen-Shot-2020-06-22-at-05-27-50.png](https://i.postimg.cc/HL2WLnDt/Screen-Shot-2020-06-22-at-05-27-50.png)](https://postimg.cc/R3WxsM03)

### Kubernetes
Once the image is created in your enviroment or pushed to a repository, you'll be able to use it to create a Pod to run your application.
If you prefer, use my image persisted in Docker Hub.
```sh
$ docker pull lyamadadocker/docker-rastreio-correios:v1
```
I'm using minikube to run my k8s cluster. Feel free to do it wherever you prefer.
[![Screen-Shot-2020-06-22-at-19-26-09.png](https://i.postimg.cc/4dX2tqs6/Screen-Shot-2020-06-22-at-19-26-09.png)](https://postimg.cc/8FnbgyFc)

#### Creating the ConfigMap
This object is very important, because it contains the enviroment variables the application needs.
```sh
$ kubectl create -f k8s-config-map.yaml
```
[![Screen-Shot-2020-06-22-at-19-26-23.png](https://i.postimg.cc/8CQ0ksYn/Screen-Shot-2020-06-22-at-19-26-23.png)](https://postimg.cc/sMmcwfsp)

#### Creating your Pod
```sh
$ kubectl create -f k8s-pod.yaml
```
[![Screen-Shot-2020-06-22-at-19-26-56.png](https://i.postimg.cc/d1nH96Vz/Screen-Shot-2020-06-22-at-19-26-56.png)](https://postimg.cc/BLLBSxDg)

#### Checking what's going on
```sh
$ kubectl get pods
```
[![Screen-Shot-2020-06-22-at-19-27-23.png](https://i.postimg.cc/cCHDk3K6/Screen-Shot-2020-06-22-at-19-27-23.png)](https://postimg.cc/Q92kHHJr)

Using minikube it's easy to monitor things through the dashboard. Such as:
- Container's env vars
[![Screen-Shot-2020-06-22-at-19-35-29.png](https://i.postimg.cc/QN4Y9fP7/Screen-Shot-2020-06-22-at-19-35-29.png)](https://postimg.cc/F1SVwVhF)
- Container's log
[![Screen-Shot-2020-06-22-at-19-36-07.png](https://i.postimg.cc/D0Mx9zs6/Screen-Shot-2020-06-22-at-19-36-07.png)](https://postimg.cc/302jpYt0)

You just need to type:
```sh
$ minikube dashboard
```

#### Twitter? :)
[![Screen-Shot-2020-06-22-at-19-25-56.png](https://i.postimg.cc/pdf1mRbV/Screen-Shot-2020-06-22-at-19-25-56.png)](https://postimg.cc/kV5yZrgL)

## SAYONARA!
I'd like to get the opportunity to say my "Thank you very much" to @rennancockles  (https://github.com/rennancockles), who shared his developments about the classes used in this project to grab the data from Brazilian's post office :) You rock, Rennan!

Please feel free to reach me out to asnwer doubts you might have.
Enjoy! :)