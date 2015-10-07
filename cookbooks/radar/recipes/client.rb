include_recipe 'radar::nodejs'

node_module 'gulp' do
  action :install
end

node_module 'bower' do
  action :install
end

execute 'npm install' do
  cwd '/home/radar/src/client'
  command 'npm install --no-bin-links --loglevel verbose'
  user 'radar'
  action :run
end

execute 'bower install' do
  cwd '/home/radar/src/client'
  command 'bower install'
  user 'radar'
  environment 'HOME' => '/home/radar'
  action :run
end

execute 'gulp build' do
  cwd '/home/radar/src/client'
  command 'gulp build'
  user 'radar'
  environment 'HOME' => '/home/radar'
  action :run
end

execute 'gulp build:dist' do
  cwd '/home/radar/src/client'
  command 'gulp build:dist'
  user 'radar'
  environment 'HOME' => '/home/radar'
  action :run
end
