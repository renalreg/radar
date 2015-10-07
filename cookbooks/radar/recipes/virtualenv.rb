resource_name :virtualenv

actions :create, :delete
default_action :create

property :owner, String, default: 'root'
property :group, String, default: 'root'
property :packages, Hash, default: {}
property :python, String, default: '/usr/bin/python'

action :create do
  venv_path = params[:path] ? params[:path] : params[:name]
  python_path = params[:python]
  venv_python_path = "#{venv_path}/bin/python.sh"

  directory venv_path do
    owner params[:owner]
    group params[:group]
    mode '00755'
    action :create
  end

  execute "create virtualenv at #{venv_path}" do
    user params[:owner]
    group params[:group]
    command "#{python_path} -m virtualenv -p #{python_path} #{venv_path}"
    not_if "test -f #{venv_path}/bin/python"
    action :run
  end

  template venv_python_path do
    source 'venv_python.sh.erb'
    owner params[:owner]
    group params[:group]
    mode '00755'
    action :create
  end

  pip_wheel_path = "#{Chef::Config['file_cache_path']}/pip-7.1.2-py2.py3-none-any.whl"

  remote_file pip_wheel_path do
    source 'https://pypi.python.org/packages/py2.py3/p/pip/pip-7.1.2-py2.py3-none-any.whl'
    action :create
  end

  # Upgrade pip from 1.x which has SSL issues when using a proxy
  execute "upgrade pip in #{venv_path}" do
    command "#{venv_python_path} -m pip install #{pip_wheel_path}"
    user params[:owner]
    group params[:group]
    action :run
  end

  params[:packages].each_pair do |package, version|
    execute "install #{package}==#{version} to #{venv_path}" do
      user params[:owner]
      group params[:group]
      command "#{venv_python_path} -m pip install #{package}==#{version}"
      not_if "[ `#{venv_python_path} -m pip freeze' | grep #{package} | cut -d'=' -f3` = '#{version}' ]"
      action :run
    end
  end
end

action :delete do
  venv_path = params[:path] ? params[:path] : params[:name]

  directory venv_path do
    recursive true
    action :delete
  end
end
