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

virtualenv venv_path do
  user 'vagrant'
  group 'vagrant'
  environment env
  action :create
end

execute "install api development dependencies in #{venv_path}" do
  command "#{venv_python_path} -m pip install -r requirements.txt"
  user 'vagrant'
  environment env
  cwd "#{src_path}/api"
  action :run
end

execute "install api dependencies in #{venv_path}" do
  command "#{venv_python_path} -m pip install -r requirements.txt"
  user 'vagrant'
  environment env
  cwd "#{src_path}/api"
  action :run
end

execute "install radar in #{venv_path}" do
  command "#{venv_python_path} -m pip install --editable ."
  user 'vagrant'
  environment env
  cwd "#{src_path}/radar"
  action :run
end

execute "install api in #{venv_python_path}" do
  command "#{venv_python_path} -m pip install --editable ."
  user 'vagrant'
  environment env
  cwd "#{src_path}/api"
  action :run
end
