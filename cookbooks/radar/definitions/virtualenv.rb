define :virtualenv, :action => :create, :owner => 'root', :group => 'root', :packages => {}, :python => '/usr/bin/python' do
  path = params[:path] ? params[:path] : params[:name]
  python_system = params[:python]
  python_venv = "#{path}/bin/python.sh"

  if params[:action] == :create
    directory path do
      owner params[:owner]
      group params[:group]
      mode '00755'
    end
    
    execute "create virtualenv at #{path}" do
      user params[:owner]
      group params[:group]
      command "#{python_system} -m virtualenv -p #{python_system} #{path}"
      not_if "test -f #{path}/bin/python"
    end

    template python_venv do
      source 'python-venv.sh.erb'
      owner 'radar'
      group 'radar'
      mode '00755'
      action :create
    end

    params[:packages].each_pair do |package, version|
      execute "install #{package}==#{version} to #{path}" do
        user params[:owner]
        group params[:group]
        command "#{python_venv} -m pip install #{package}==#{version}"
        not_if "[ `#{python_venv} -m pip freeze' | grep #{package} | cut -d'=' -f3` = '#{version}' ]"
      end
    end
  elsif params[:action] == :delete
    directory path do
      action :delete
      recursive true
    end
 end
end
