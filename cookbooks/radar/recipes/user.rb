home_path = '/home/radar'

group 'radar' do
  gid 501
  action :create
end

user 'radar' do
  uid 501
  gid 501
  password 'vagrant'
  action :create
end

directory home_path do
  owner 'radar'
  group 'radar'
  mode '00755'
  action :create
end

directory "#{home_path}/.ssh" do
  owner 'radar'
  group 'radar'
  mode '00700'
  action :create
end

template "#{home_path}/.ssh/authorized_keys" do
  source 'vagrant.pub.erb'
  owner 'radar'
  group 'radar'
  mode '00600'
  action :create
end

template "#{home_path}/.bashrc" do
  source 'bashrc.erb'
  owner 'radar'
  group 'radar'
  mode '00644'
  action :create
end

template "#{home_path}/.bash_profile" do
  source 'bash_profile.erb'
  owner 'radar'
  group 'radar'
  mode '00644'
  action :create
end
