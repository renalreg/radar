include_recipe 'radar::python'

name = 'radar-api'
conf_path = "/etc/#{name}"

directory conf_path do
  owner 'radar'
  group 'radar'
  mode '00755'
  action :create
end

template "#{conf_path}/settings.py" do
  source 'api/settings.py.erb'
  user 'radar'
  group 'radar'
  mode '00644'
  action :create
end

template "#{conf_path}/supervisord.conf" do
  source 'api/supervisord.conf.erb'
  user 'root'
  group 'root'
  mode '00644'
  notifies :restart, "service[#{name}]"
  action :create
end

template "#{conf_path}/gunicorn.py" do
  source 'api/gunicorn.py.erb'
  user 'root'
  group 'root'
  mode '00644'
  notifies :restart, "service[#{name}]"
  action :create
end

template "/etc/init.d/#{name}" do
  source 'api/init.erb'
  user 'root'
  group 'root'
  mode '00755'
  notifies :restart, "service[#{name}]"
  action :create
end

service name do
  action [:enable, :start]
end
