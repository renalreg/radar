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

directory '/home/radar' do
  owner 'radar'
  group 'radar'
  mode '00755'
  action :create
end

directory '/home/radar/.ssh' do
  owner 'radar'
  group 'radar'
  mode '00700'
  action :create
end

template '/home/radar/.ssh/authorized_keys' do
  source 'vagrant.pub.erb'
  owner 'radar'
  group 'radar'
  mode '00600'
  action :create
end

template '/home/radar/.bashrc' do
  source 'bashrc.erb'
  owner 'radar'
  group 'radar'
  mode '00644'
  action :create
end

template '/home/radar/.bash_profile' do
  source 'bash_profile.erb'
  owner 'radar'
  group 'radar'
  mode '00644'
  action :create
end
