# SELinux

```
# radar.te

module radar 1.0;

require {
        type commplex_main_port_t;
        type httpd_t;
        type transproxy_port_t;
        type vmblock_t;
        class tcp_socket { name_bind name_connect };
        class file { read getattr open };
        class dir read;
}

#============= httpd_t ==============
allow httpd_t commplex_main_port_t:tcp_socket name_bind;
allow httpd_t commplex_main_port_t:tcp_socket name_connect;
allow httpd_t transproxy_port_t:tcp_socket name_bind;
allow httpd_t vmblock_t:dir read;
allow httpd_t vmblock_t:file { read getattr open };
```

```bash
yum install policycoreutils-python
checkmodule -M -m -o radar.mod radar.te
semodule_package -o radar.pp -m radar.mod
semodule -i radar.pp
```
