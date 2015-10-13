unless Vagrant.has_plugin?('vagrant-berkshelf')
  raise 'vagrant-berkshelf is not installed, run: vagrant plugin install vagrant-berkshelf'
end

# XXX Windows hosts only
# Use Vagrant 1.7.3 (exact version) and VirtualBox 4.x (4.3.30 is known to work)
# Vagrant 1.7.3 added support for long paths. This was removed in 1.7.4 as it
# caused problems in VirtualBox 5.
# FIXME https://github.com/mitchellh/vagrant/issues/1953

# TODO instructions for enabling symlinks

Vagrant.configure(2) do |config|
  config.vm.box = 'bento/centos-7.1'

  # Web interface ports
  config.vm.network 'forwarded_port', guest: 80, host: 8080
  config.vm.network 'forwarded_port', guest: 8081, host: 8081
  config.vm.network 'forwarded_port', guest: 8082, host: 8082

  # API ports
  config.vm.network 'forwarded_port', guest: 5000, host: 5000
  config.vm.network 'forwarded_port', guest: 5001, host: 5001

  # PostgreSQL port
  config.vm.network 'forwarded_port', guest: 5432, host: 5432

  config.vm.synced_folder '.', '/home/vagrant/src', create: true, owner: 'vagrant', group: 'vagrant'

  config.vm.provider 'virtualbox' do |v|
    v.memory = 1024
    v.cpus = 2
  end

  if Vagrant.has_plugin?('vagrant-proxyconf')
    # Proxies for NBT
    # Install cntlm and make sure it's running on port 3128
    config.proxy.http = 'http://10.0.2.2:3128/'
    config.proxy.https = 'http://10.0.2.2:3128/'
    config.proxy.no_proxy = 'localhost,127.0.0.1,10.0.2.2'
  end

  config.vm.provision 'chef_solo' do |chef|
    chef.add_recipe 'radar'
  end
end
