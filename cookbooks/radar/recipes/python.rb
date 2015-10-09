home_path = '/home/vagrant'
venv_path = "#{home_path}/venv"
venv_python_path = "#{venv_path}/bin/python"
src_path = "#{home_path}/src/radar"

env = {
  'HOME' => home_path,
  'PATH' => '/usr/pgsql-9.4/bin:/usr/bin:/bin'
}

package 'python-virtualenv' do
  action :install
end

virtualenv venv_path do
  user 'vagrant'
  group 'vagrant'
  environment env
  packages 'gunicorn' => '19.3.0',
           'supervisor' => '3.1.3'
  action :create
end

execute "install dev_requirements.txt in #{venv_path}" do
  command "#{venv_python_path} -m pip install -r dev_requirements.txt"
  user 'vagrant'
  environment env
  cwd src_path
  action :run
end

execute "install requirements.txt in #{venv_path}" do
  command "#{venv_python_path} -m pip install -r requirements.txt"
  user 'vagrant'
  environment env
  cwd src_path
  action :run
end

execute "install radar in #{venv_python_path}" do
  command "#{venv_python_path} -m pip install --editable ."
  user 'vagrant'
  environment env
  cwd src_path
  action :run
end
