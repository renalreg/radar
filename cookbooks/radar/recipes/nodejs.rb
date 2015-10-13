package 'nodejs' do
  action :install
end

# jq is used by the npm_package resource to check if a package is installed
package 'jq' do
  action :install
end

# NOTE
# Older versions of npm put each module's dependencies in a node_modules
# sub-directory which can create some very long paths.
# On Windows these paths can exceed the maximum path length.
# If you run npm install from Windows it's not a problem (it can create paths
# too long to delete from explorer though).
# If you run npm install from a VM on a Windows host you'll run into the
# maximum path length issue.
# npm 3+ will only create nested node_modules directories if the module
# requires anorther version of a library.
# The shell script from npmjs.org installs the latest version of npm
# (currently 3.x vs the packaged version of 1.x).
# FIXME https://www.virtualbox.org/ticket/11976
remote_file "#{Chef::Config['file_cache_path']}/npm.sh" do
  source 'https://www.npmjs.org/install.sh'
  owner 'root'
  group 'root'
  mode '00755'
  action :create
end

execute 'install npm' do
  command "sh #{Chef::Config['file_cache_path']}/npm.sh"
  user 'root'
  creates '/usr/bin/npm'
  action :run
end

# Use an alternative registry (e.g npm-lazy-proxy) if specified
npm_config 'registry' do
  value node['npm_registry']
  action :create
end

# NOTE the bin-links option prevents npm from symlinking any binaries.
# VirtualBox supports symlinks if the SharedFoldersEnableSymlinksCreate option
# is enabled. In Windows you need to have the SeCreateSymbolicLinkPrivilege
# privilege to create symlinks.
# http://security.stackexchange.com/questions/10194
npm_config 'bin-links' do
  value node['npm_bin_links']
  action :create
end
