resource_name :ruby_gem

actions :install
default_action :install

action :install do
  execute "gem install #{name}" do
    command "gem install #{name}"
    user 'root'
    not_if "gem list | grep -q #{name}"
    action :run
  end
end
