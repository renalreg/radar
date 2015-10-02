package 'vim'

user 'radar' do
  password 'vagrant'
  action :create
end

directory '/home/radar/.ssh' do
  owner 'radar'
  group 'radar'
  mode '0700'
  action :create
end

file '/home/radar/.ssh/authorized_keys' do
  content 'ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA6NF8iallvQVp22WDkTkyrtvp9eWW6A8YVr+kz4TjGYe7gHzIw+niNltGEFHzD8+v1I2YJ6oXevct1YeS0o9HZyN1Q9qgCgzUFtdOKLv6IedplqoPkcmF0aYet2PkEDo3MlTBckFXPITAMzF8dJSIFo9D8HfdOV0IAdx4O7PtixWKn5y2hMNG0zQPyUecp4pzC6kivAIhyfHilFR61RGL+GPXQ2MWZWFYbAGjyiYJnAmCP3NOTd0jMZEnDkbUvxhMmBYSdETk1rRgm+R4LOzFUGaHqHDLKLX+FIPKcF96hrucXzcWyLbIbEgE98OHlnVYCzRdK8jlqm8tehUc9c9WhQ== vagrant insecure public key'
  owner 'radar'
  group 'radar'
  mode '0600'
  action :create
end

include_recipe 'postgresql::server'
include_recipe 'database::postgresql'

postgresql_connection_info = {
  :host => '127.0.0.1',
  :username => 'postgres',
  :password => 'vagrant'
}

postgresql_database 'radar' do
  connection postgresql_connection_info
  action :create
end

postgresql_database_user 'radar' do
  connection postgresql_connection_info
  password 'vagrant'
  action :create
end

postgresql_database_user 'radar' do
  connection postgresql_connection_info
  database_name 'radar'
  privileges [:all]
  action :grant
end
