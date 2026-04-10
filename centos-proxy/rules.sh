#!/bin/bash
iptables -F
iptables -X
iptables -t nat -F
iptables -t mangle -F

iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Разрешить SSH
iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# Разрешить доступ к Proxy API (порт 5000) с любых источников
iptables -A INPUT -p tcp --dport 5000 -j ACCEPT

# Разрешить доступ к Valkey(Redis) (порт 6379) только с localhost (для безопасности)
iptables -A INPUT -p tcp --dport 6379 -s 127.0.0.1 -j ACCEPT

# Сохранить правила (CentOS)
sudo dnf install iptables-services -y
sudo service iptables save
sudo systemctl enable iptables
