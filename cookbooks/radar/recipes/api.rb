package 'scl-utils' do
  action :install
end

remote_file "#{Chef::Config['file_cache_path']}/rhscl-python27-epel-6-x86_64.noarch.rpm" do
  source 'https://www.softwarecollections.org/en/scls/rhscl/python27/epel-6-x86_64/download/rhscl-python27-epel-6-x86_64.noarch.rpm'
  action :create
end

rpm_package 'rhscl-python27' do
 source "#{Chef::Config['file_cache_path']}/rhscl-python27-epel-6-x86_64.noarch.rpm"
 action :install
end

package 'python27' do
  action :install
end

python_system = '/home/radar/bin/python.sh'
python_venv = '/home/radar/venv/bin/python.sh'

template python_system do
  source 'python-system.sh.erb'
  owner 'radar'
  group 'radar'
  mode '00755'
  action :create
end

virtualenv '/home/radar/venv' do
  python python_system
  owner 'radar'
  group 'radar'
  packages 'gunicorn' => '19.3.0',
           'supervisor' => '3.1.3'
end

execute 'pip install -r requirements.txt' do
  command '#{python_venv} -m pip install -r /home/radar/src/requirements.txt'
  user 'radar'
  group 'radar'
  environment 'PATH' => '/usr/pgsql-9.4/bin:/sbin:/bin:/usr/sbin:/usr/bin:/usr/local/sbin' 
  action :run
end

execute 'pip install --editable .' do
  command '#{python_venv} -m pip install --editable /home/radar/src'
  user 'radar'
  group 'radar'
  not_if '#{python_venv} -m pip freeze | grep radar'
  action :run
end

template '/home/radar/settings.py' do
  source 'settings.py.erb'
  user 'radar'
  group 'radar'
  mode '00644'
  action :create
end

template '/etc/radar.conf' do
  source 'conf.erb' 
  user 'root'
  group 'root'
  mode '00644'
  notifies :restart, 'service[radar]'
  action :create
end

template '/etc/init.d/radar' do
  source 'init.erb' 
  user 'root'
  group 'root'
  mode '00755'
  notifies :restart, 'service[radar]'
  action :create
end

service 'radar' do
  action :start
end
