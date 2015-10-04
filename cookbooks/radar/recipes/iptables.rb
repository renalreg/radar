template '/etc/sysconfig/iptables' do
  source 'iptables.erb'
  owner 'root'
  group 'root'
  mode '0600'
end

service 'iptables' do
  action :restart
end
