home_path = '/home/vagrant'

directory home_path do
  owner 'vagrant'
  group 'vagrant'
  mode '00755'
  action :create
end

template "#{home_path}/.bashrc" do
  source 'bashrc.erb'
  owner 'vagrant'
  group 'vagrant'
  mode '00644'
  action :create
end

template "#{home_path}/.bash_profile" do
  source 'bash_profile.erb'
  owner 'vagrant'
  group 'vagrant'
  mode '00644'
  action :create
end
