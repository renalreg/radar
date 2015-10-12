home_path = '/home/vagrant'
venv_path = "#{home_path}/venv"
venv_python_path = "#{venv_path}/bin/python"
src_path = "#{home_path}/src"

env = {
  'HOME' => home_path,
  'PATH' => '/usr/pgsql-9.4/bin:/usr/bin:/bin'
}

package 'python-virtualenv' do
  action :install
end

directory '/root/.pip' do
  owner 'root'
  group 'root'
  mode '00755'
  action :create
end

# TODO add config option
file '/root/.pip/pip.conf' do
  content <<-EOH
[global]
index-url = http://rr-systems-live.northbristol.local:2001/root/pypi/+simple/
EOH
  owner 'root'
  group 'root'
  mode '00644'
  action :create
end

directory '/home/vagrant/.pip' do
  owner 'root'
  group 'root'
  mode '00755'
  action :create
end

file '/home/vagrant/.pip/pip.conf' do
  content <<-EOH
[global]
index-url = http://rr-systems-live.northbristol.local:2001/root/pypi/+simple/
EOH
  owner 'vagrant'
  group 'vagrant'
  mode '00644'
  action :create
end

virtualenv venv_path do
  user 'vagrant'
  group 'vagrant'
  environment env
  action :create
end

execute 'install api dev dependencies' do
  command "#{venv_python_path} -m pip install -r dev-requirements.txt"
  user 'vagrant'
  environment env
  cwd "#{src_path}/api"
  action :run
end

execute 'install api dependencies' do
  command "#{venv_python_path} -m pip install -r requirements.txt"
  user 'vagrant'
  environment env
  cwd "#{src_path}/api"
  action :run
end

execute 'install radar' do
  command "#{venv_python_path} -m pip install --editable ."
  user 'vagrant'
  environment env
  cwd "#{src_path}/radar"
  action :run
end

execute 'install api' do
  command "#{venv_python_path} -m pip install --editable ."
  user 'vagrant'
  environment env
  cwd "#{src_path}/api"
  action :run
end
