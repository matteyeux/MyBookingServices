# Ansible

### Setup

If the VMs are not deployed with Terraform, run the following commands on your hosts :
- Create ansible user `sudo adduser ansible --home /home/ansible --disabled-password --gecos ''`.
- Add the user to /etc/sudoers : `ansible ALL=(ALL) NOPASSWD:ALL`.
- Copy your SSH public key to ansible's `$HOME/.ssh/authorized_keys`

Then make sure you can access all your hosts :
```
λ ~/dev/MyBookingServices/ansible(main) » ansible -m ping all -i hosts
manager | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
worker2 | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
worker1 | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```


### Swarm

Check if VM is part of the cluster with `docker node ls` :
```
$ docker node ls
ID                            HOSTNAME   STATUS    AVAILABILITY   MANAGER STATUS   ENGINE VERSION
vphfokkobatgm3q66bldr3obq *   manager    Ready     Active         Leader           20.10.6
t4ixoau0awjykj5x2kk4d466c     worker1    Ready     Active         Reachable        20.10.6
5xg7yjq2d1heienyi0rrtxvc3     worker2    Ready     Active         Reachable        20.10.6
```

It should return the list of nodes. If not, it will return a error about Swarm.

### Docker Registry in Swarm
If `docker ps` does not return anything, make sure the service is running.

In this case running `docker service ls` says there 0/1 replicas.
```
$ docker service ls
ID             NAME       MODE         REPLICAS   IMAGE        PORTS
gogcitlcztug   registry   replicated   0/1        registry:2   *:5000->5000/tcp
```

To troubleshoot you can run `docker service ps --no-trunc gogcitlcztug` it will print the error about this service. In this case, it's a typo.
```
$ docker service ps --no-trunc gogcitlcztug
ID                          NAME             IMAGE        NODE      DESIRED STATE   CURRENT STATE                      ERROR                                                                                          PORTS
hq6ekkllvipok7froqgnxrbfb   registry.1       registry:2   manager   Ready           Preparing less than a second ago
efl6p2xwoiwu9kw7yntwtga49    \_ registry.1   registry:2   worker1   Shutdown        Rejected 3 seconds ago             "invalid mount config for type "bind": bind source path does not exist: /opt/registry/data"
9aei2gh4499m1xrf7rs1ptyw1    \_ registry.1   registry:2   manager   Shutdown        Rejected 8 seconds ago             "invalid mount config for type "bind": bind source path does not exist: /opt/registry/certa"
tao63j51y1jibzuay18ih2krf    \_ registry.1   registry:2   worker2   Shutdown        Rejected 13 seconds ago            "invalid mount config for type "bind": bind source path does not exist: /opt/registry/data"
qwwkrvekjjh255o8qm1jjuz54    \_ registry.1   registry:2   worker2   Shutdown        Rejected 19 seconds ago            "invalid mount config for type "bind": bind source path does not exist: /opt/registry/data"
```

#### Push and pull

First, tag an image, for example alpine then push it to your registry :
```
$ docker tag alpine:latest registry.mybooking.services:5000/myalpine:v2
$ docker push registry.mybooking.services:5000/myalpine:v2
The push refers to repository [registry.mybooking.services:5000/myalpine]
72e830a4dff5: Layer already exists
v2: digest: sha256:1775bebec23e1f3ce486989bfc9ff3c4e951690df84aa9f926497d82f2ffca9d size: 528
```

You can pull from another node like this :
```
$ docker pull registry.mybooking.services:5000/myalpine:v2
v2: Pulling from myalpine
Digest: sha256:1775bebec23e1f3ce486989bfc9ff3c4e951690df84aa9f926497d82f2ffca9d
Status: Downloaded newer image for registry.mybooking.services:5000/myalpine:v2
registry.mybooking.services:5000/myalpine:v2
```
