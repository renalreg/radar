name = 'radar-api-dev'
conf_path = "/etc/#{name}"
sysconfig_path = "/etc/sysconfig/#{name}"
systemd_path = "/etc/systemd/system/#{name}.service"
settings_path = "#{conf_path}/settings.py"
gunicorn_config_path = "#{conf_path}/gunicorn.py"

directory conf_path do
  owner 'root'
  group 'root'
  mode '00755'
  action :create
end

template sysconfig_path do
  source 'api/sysconfig.erb'
  variables :settings_path => settings_path
  owner 'root'
  group 'root'
  mode '00755'
  action :create
end

template systemd_path do
  source 'api/systemd.erb'
  variables :name => name,
            :sysconfig_path => sysconfig_path,
            :gunicorn_config_path => gunicorn_config_path
  owner 'root'
  group 'root'
  mode '00755'
  action :create
end

template settings_path do
  source 'api/settings.py.erb'
  owner 'root'
  group 'root'
  mode '00755'
  action :create
end

template gunicorn_config_path do
  source 'api/gunicorn.py.erb'
  owner 'root'
  group 'root'
  mode '00755'
  action :create
end

service name do
  action [:enable, :start]
end
