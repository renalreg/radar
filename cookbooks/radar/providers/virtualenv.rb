use_inline_resources

provides :virtualenv

action :create do
  venv_python_path = "#{new_resource.path}/bin/python"

  directory new_resource.path do
    owner new_resource.user
    group new_resource.group
    mode '00755'
    action :create
  end

  execute "create virtualenv at #{new_resource.path}" do
    command "#{new_resource.python_path} -m virtualenv --quiet #{new_resource.path}"
    user new_resource.user
    environment new_resource.environment
    not_if "test -f #{venv_python_path}"
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
