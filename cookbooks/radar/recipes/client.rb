include_recipe 'radar::nodejs'

home_path = '/home/vagrant'
src_path = "#{home_path}/src/client"

env = {'HOME' => home_path}

npm_package 'gulp' do
  action :install
end

npm_package 'bower' do
  action :install
end

# XXX currently this results in https://github.com/npm/npm/issues/9224
# A workaround is to install each package separately.
execute 'npm install' do
  command 'npm install --no-bin-links'
  user 'vagrant'
  environment env
  cwd src_path
  action :run
end

execute 'bower install' do
  command 'bower install'
  user 'vagrant'
  environment env
  cwd src_path
  action :run
end

execute 'gulp build' do
  command 'gulp build'
  user 'vagrant'
  environment env
  cwd src_path
  action :run
end

execute 'gulp build:dist' do
  command 'gulp build:dist'
  user 'vagrant'
  environment env
  cwd src_path
  action :run
end
