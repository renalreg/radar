include_recipe 'radar::nodejs'

npm_package 'gulp' do
  action :install
end

npm_package 'bower' do
  action :install
end

execute 'npm install' do
  cwd '/home/radar/src/client'
  command 'npm install --no-bin-links'
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

link '/opt/radar-client' do
  to '/home/radar/src/client/dist'
  owner 'radar'
  group 'radar'
  action :create
end
