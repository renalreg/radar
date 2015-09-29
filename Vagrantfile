Vagrant.configure(2) do |config|
  config.vm.box = "centos/7"
  config.vm.network "forwarded_port", guest: 80, host: 8080
  config.proxy.http = "http://10.0.2.2:53128/"
  config.proxy.https = "http://10.0.2.2:53128/"
  config.proxy.no_proxy = "localhost,127.0.0.1"
end
