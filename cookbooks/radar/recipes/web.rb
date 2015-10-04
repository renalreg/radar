template '/etc/yum.repos.d/nginx.conf' do
  source 'yum-nginx.conf.erb'
  user 'root'
  group 'root'
  mode '00644'
  action :create
end

package 'nginx' do
  action :install
end

template '/etc/nginx/conf.d/radar.conf' do
  source 'nginx-radar.conf.erb' 
  user 'root'
  group 'root'
  mode '00644'
  notifies :restart, 'service[nginx]'
  action :create
end

service 'nginx' do
  action :start
end
