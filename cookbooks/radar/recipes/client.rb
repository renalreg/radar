include_recipe 'radar::nodejs'

home_path = '/home/vagrant'
src_path = "#{home_path}/src/client"

env = {'HOME' => home_path}

package 'optipng' do
  action :install
end

package 'gifsicle' do
  action :install
end

package 'libjpeg-turbo-utils' do
  action :install
end

package 'libpng-devel' do
  action :install
end

package 'zlib-devel' do
  action :install
end

npm_package 'gulp' do
  action :install
end

npm_package 'bower' do
  action :install
end

# XXX currently this results in "maximum call stack size exceeded"
# A workaround is to install each package separately.
# FIXME https://github.com/npm/npm/issues/9224
# XXX imagemin will silently fail to build native binaries
# The symptom is that gulp build:dist will fail on the images step.
# The first issue is that the modules don't detect the system binaries for
# optipng, jpegtran, gifsicle etc.
# The second issue is that the module that downloads the source code doesn't
# respect proxy settings.
# So you'll need to downgrade bin-build: npm install bin-build@2.1.1
# Then run: npm rebuild
# jpegtran will still fail as it is using a https URL
# FIXME https://github.com/npm/npm/issues/8682
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
