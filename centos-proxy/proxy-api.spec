Name:           proxy-api
Version:        1.0
Release:        1%{?dist}
Summary:        Caching proxy API

License:        MIT
URL:            http://example.com
Source0:        proxy-api-1.0.tar.gz
BuildArch:      noarch

Requires:       python3-flask python3-redis python3-requests python3-pyyaml
Requires:       systemd

%description
Proxy API with Redis cache for user data.

%prep
%setup -q

%install
mkdir -p %{buildroot}/usr/local/bin
install -m 755 cache-api.py %{buildroot}/usr/local/bin/proxy-api

mkdir -p %{buildroot}/etc/cache-api
cat > %{buildroot}/etc/cache-api/config.yaml <<'CONF'
redis:
  host: "localhost"
  port: 6379

backend:
  host: "192.168.1.10"
  port: 8080

app:
  port: 5000
CONF

mkdir -p %{buildroot}/etc/systemd/system
cat > %{buildroot}/etc/systemd/system/proxy-api.service <<'SERVICE'
[Unit]
Description=Proxy API Service
After=network.target redis.service

[Service]
ExecStart=/usr/local/bin/proxy-api
Restart=always
Environment="CONFIG_PATH=/etc/cache-api/config.yaml"
User=root
Group=root

[Install]
WantedBy=multi-user.target
SERVICE

%files
/usr/local/bin/proxy-api
/etc/cache-api/config.yaml
/etc/systemd/system/proxy-api.service

%changelog
* Fri Apr 3 2026 Your Name <you@example.com> 1.0-1
- Initial release
