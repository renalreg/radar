template '/etc/yum.repos.d/nginx.conf' do
  source 'nginx_repo.conf.erb'
  user 'root'
  group 'root'
  mode '00644'
  action :create
end

package 'nginx' do
  action :install
end

template '/etc/nginx/conf.d/radar-web.conf' do
  source 'web/nginx.conf.erb'
  user 'root'
  group 'root'
  mode '00644'
  notifies :restart, 'service[nginx]'
  action :create
end

template '/etc/nginx/conf.d/radar-web-dev.conf' do
  source 'web/nginx-dev.conf.erb'
  user 'root'
  group 'root'
  mode '00644'
  notifies :restart, 'service[nginx]'
  action :create
end

service 'nginx' do
  action [:enable, :start]
end
