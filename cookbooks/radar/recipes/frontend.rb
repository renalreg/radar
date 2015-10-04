package 'nodejs' do
  action :install
end

package 'npm' do
  action :install
end

execute 'npm install -g gulp' do
  command 'npm install -g gulp'
  user 'root'
end

execute 'npm install -g bower' do
  command 'npm install -g bower'
  user 'root'
end

execute 'npm install' do
  cwd '/home/radar/src/client'
  command 'npm install --no-bin-links'
  user 'radar'
end

execute 'bower install' do
  cwd '/home/radar/src/client'
  command 'bower install'
  user 'radar'
  environment 'HOME' => '/home/radar'
end

execute 'gulp build' do
  cwd '/home/radar/src/client'
  command 'gulp build'
  user 'radar'
  environment 'HOME' => '/home/radar'
end

execute 'gulp build:dist' do
  cwd '/home/radar/src/client'
  command 'gulp build:dist'
  user 'radar'
  environment 'HOME' => '/home/radar'
end
