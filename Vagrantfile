unless Vagrant.has_plugin?('vagrant-berkshelf')
  raise 'vagrant-berkshelf is not installed, run: vagrant plugin install vagrant-berkshelf'
end

Vagrant.configure(2) do |config|
  config.vm.box = 'bento/centos-7.1'

  config.vm.network 'forwarded_port', guest: 80, host: 8080
  config.vm.network 'forwarded_port', guest: 8081, host: 8081
  config.vm.network 'forwarded_port', guest: 8082, host: 8082
  config.vm.network 'forwarded_port', guest: 5432, host: 5432

  config.vm.synced_folder '.', '/home/vagrant/src', create: true, owner: 'vagrant', group: 'vagrant'

  if Vagrant.has_plugin?('vagrant-proxyconf')
    config.proxy.http = 'http://10.0.2.2:3128/'
    config.proxy.https = 'http://10.0.2.2:3128/'
    config.proxy.no_proxy = 'localhost,127.0.0.1,10.0.2.2'
  end

  config.vm.provision 'chef_solo' do |chef|
    chef.add_recipe 'radar'
  end

  config.vm.provider 'virtualbox' do |v|
    v.memory = 1024
    v.cpus = 2
  end
end
