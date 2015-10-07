resource_name :node_module

actions :install
default_action :install

action :install do
  execute "npm install -g #{name}" do
    command "npm install -g #{name}"
    user 'root'
    action :run
  end
end
