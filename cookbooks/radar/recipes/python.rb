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

home_path = '/home/radar'
bin_path = "#{home_path}/bin"
python_path = "#{bin_path}/python.sh"
src_path = "#{home_path}/src"

venv_path = '/opt/radar'
venv_python_path = "#{venv_path}/bin/python.sh"

directory bin_path do
  owner 'radar'
  group 'radar'
  mode '00755'
  action :create
end

template python_path do
  source 'python.sh.erb'
  owner 'radar'
  group 'radar'
  mode '00755'
  action :create
end

virtualenv venv_path do
  python_path python_path
  user 'radar'
  group 'radar'
  environment 'HOME' => '/home/radar'
  packages 'gunicorn' => '19.3.0',
           'supervisor' => '3.1.3'
  action :create
end

execute "install dev_requirements.txt in #{venv_path}" do
  command "#{venv_python_path} -m pip install -r dev_requirements.txt"
  user 'radar'
  environment 'HOME' => '/home/radar'
  cwd "#{src_path}/radar"
  action :run
end

execute "install requirements.txt in #{venv_path}" do
  command "#{venv_python_path} -m pip install -r requirements.txt"
  user 'radar'
  environment 'HOME' => '/home/radar',
              'PATH' => '/usr/pgsql-9.4/bin:/usr/bin:/bin'
  cwd "#{src_path}/radar"
  action :run
end

execute "install radar in #{venv_python_path}" do
  command "#{venv_python_path} -m pip install --editable ."
  user 'radar'
  environment 'HOME' => '/home/radar',
              'PATH' => '/usr/pgsql-9.4/bin:/usr/bin:/bin'
  cwd "#{src_path}/radar"
  action :run
end
