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
