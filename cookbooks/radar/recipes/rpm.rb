include_recipe 'radar::ruby'

ruby_gem 'fpm' do
  action :install
end
