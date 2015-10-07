include_recipe 'radar::ruby'

gem_package 'fpm' do
  action :install
end
