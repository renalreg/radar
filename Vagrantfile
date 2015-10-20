# XXX Windows hosts only
# Use Vagrant 1.7.3 (exact version) and VirtualBox 4.x (4.3.30 is known to work)
# Vagrant 1.7.3 added support for long paths. This was removed in 1.7.4 as it
# caused problems in VirtualBox 5.
# FIXME https://github.com/mitchellh/vagrant/issues/1953

provisioner_path = ENV['NBT'] == '1' ? 'ansible/bootstrap_vagrant_nbt.sh' : 'ansible/bootstrap_vagrant.sh'

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

  # FIXME https://github.com/ansible/ansible/pull/10369
  config.vm.synced_folder 'ansible', '/home/vagrant/ansible', create: true, owner: 'vagrant', group: 'vagrant', :mount_options => ["dmode=755", "fmode=644"]

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

  config.vm.provision :shell, :path => provisioner_path
end
