use_inline_resources

provides :virtualenv

action :create do
  venv_python_path = "#{new_resource.path}/bin/python.sh"

  directory new_resource.path do
    owner new_resource.user
    group new_resource.group
    mode '00755'
    action :create
  end

  execute "create virtualenv at #{new_resource.path}" do
    command "#{new_resource.python_path} -m virtualenv -p #{new_resource.python_path} #{new_resource.path}"
    user new_resource.user
    environment new_resource.environment
    not_if "test -f #{new_resource.path}/bin/python"
    action :run
  end

  template venv_python_path do
    source 'venv_python.sh.erb'
    owner new_resource.user
    group new_resource.group
    mode '00755'
    action :create
  end

  pip_wheel_path = "#{Chef::Config['file_cache_path']}/pip-7.1.2-py2.py3-none-any.whl"

  remote_file pip_wheel_path do
    source 'https://pypi.python.org/packages/py2.py3/p/pip/pip-7.1.2-py2.py3-none-any.whl'
    action :create
  end

  # Upgrade pip from 1.x which has SSL issues when using a proxy
  execute "upgrade pip in #{new_resource.path}" do
    command "#{venv_python_path} -m pip install #{pip_wheel_path}"
    user new_resource.user
    environment new_resource.environment
    action :run
  end

  new_resource.packages.each_pair do |package, version|
    execute "install #{package}==#{version} to #{new_resource.path}" do
      command "#{venv_python_path} -m pip install #{package}==#{version}"
      user new_resource.user
      environment new_resource.environment
      not_if "[ `#{venv_python_path} -m pip freeze' | grep #{package} | cut -d'=' -f3` = '#{version}' ]"
      action :run
    end
  end
end

action :delete do
  directory new_resource.path do
    recursive true
    action :delete
  end
end
