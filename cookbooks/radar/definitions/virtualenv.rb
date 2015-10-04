define :virtualenv, :action => :create, :owner => 'root', :group => 'root', :packages => {}, :python => '/usr/bin/python' do
  python_path = params[:python]
  venv_path = params[:path] ? params[:path] : params[:name]
  venv_python_path = "#{venv_path}/bin/python.sh"

  if params[:action] == :create
    directory venv_path do
      owner params[:owner]
      group params[:group]
      mode '00755'
    end
    
    execute "create virtualenv at #{venv_path}" do
      user params[:owner]
      group params[:group]
      command "#{python_path} -m virtualenv -p #{python_path} #{venv_path}"
      not_if "test -f #{venv_path}/bin/python"
    end

    template venv_python_path do
      source 'python-venv.sh.erb'
      owner 'radar'
      group 'radar'
      mode '00755'
      action :create
    end

    params[:packages].each_pair do |package, version|
      execute "install #{package}==#{version} to #{venv_path}" do
        user params[:owner]
        group params[:group]
        command "#{venv_python_path} -m pip install #{package}==#{version}"
        not_if "[ `#{venv_python_path} -m pip freeze' | grep #{package} | cut -d'=' -f3` = '#{version}' ]"
      end
    end
  elsif params[:action] == :delete
    directory venv_path do
      action :delete
      recursive true
    end
 end
end
