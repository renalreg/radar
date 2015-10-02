unless Vagrant.has_plugin?('vagrant-berkshelf')
  raise 'vagrant-berkshelf is not installed, run: vagrant plugin install vagrant-berkshelf'
end

Vagrant.configure(2) do |config|
  config.vm.box = 'bento/centos-6.7'

  config.vm.network 'forwarded_port', guest: 8080, host: 18080
  config.vm.network 'forwarded_port', guest: 8081, host: 18081
  config.vm.network 'forwarded_port', guest: 5432, host: 15432

  config.proxy.http = 'http://10.0.2.2:53128/'
  config.proxy.https = 'http://10.0.2.2:53128/'
  config.proxy.no_proxy = 'localhost,127.0.0.1,10.0.2.2'

  config.vm.provision 'chef_solo' do |chef|
    chef.add_recipe 'radar'
  end
end
