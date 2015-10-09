include_recipe 'radar::ruby'

package 'rpm-build' do
  action :install
end

gem_package 'fpm' do
  action :install
end
