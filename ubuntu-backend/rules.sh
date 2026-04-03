#!/bin/bash
# Очистка правил
iptables -F
iptables -X
iptables -t nat -F
iptables -t mangle -F

# Политики по умолчанию
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# Разрешить локальный трафик
iptables -A INPUT -i lo -j ACCEPT

# Разрешить уже установленные соединения
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Разрешить доступ к SSH (если нужно)
iptables -A INPUT -p tcp --dport 22 -j ACCEPT   # при необходимости

# Разрешить доступ к Backend API (порт 8080) только с IP прокси (192.168.56.102)
iptables -A INPUT -p tcp --dport 8080 -s 192.168.56.102 -j ACCEPT

# Разрешить доступ к PostgreSQL (порт 5432) только с localhost (т.к. бэкенд на этой же ВМ)
iptables -A INPUT -p tcp --dport 5432 -s 127.0.0.1 -j ACCEPT

# Сохранить правила (для Ubuntu 24.04)
sudo apt install iptables-persistent -y
sudo netfilter-persistent save
