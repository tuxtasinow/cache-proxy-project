# Кеширующее приложение

## Описание
Проект состоит из двух ВМ: Ubuntu (PostgreSQL + Backend API) и CentOS (Redis + Proxy API).

## Сборка и установка
### Ubuntu
```bash
go build -o backend-api backend.go
dpkg-deb --build package_deb backend-api_1.0_amd64.deb
sudo dpkg -i backend-api_1.0_amd64.deb
```

### CentOS
```bash
rpmbuild -ba proxy-api.spec
sudo rpm -ivh --nodeps RPMs/noarch/proxy-api-1.0-1.el10.noarch.rpm
```

## Правила iptables
Запустите `rules.sh` на соответствующих ВМ.
