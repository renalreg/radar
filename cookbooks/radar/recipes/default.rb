package 'epel-release' do
  action :install
end

package 'vim' do
  action :install
end

# Needed to pip freeze a virtualenv with packages installed from git
package 'git' do
  action :install
end

package 'htop' do
  action :install
end

package 'man' do
  action :install
end

execute 'yum groupinstall -y "Development Tools"' do
  user 'root'
  action :run
end

# NOTE selinux is enabled in production
include_recipe 'selinux::permissive'

include_recipe 'radar::user'
include_recipe 'radar::db'
include_recipe 'radar::python'
include_recipe 'radar::api'
include_recipe 'radar::client'
include_recipe 'radar::web'
include_recipe 'radar::rpm'
