include_recipe 'postgresql::server'
include_recipe 'database::postgresql'

postgresql_connection_info = {
  host: '127.0.0.1',
  username: 'postgres',
  password: 'vagrant'
}

postgresql_database 'radar' do
  connection postgresql_connection_info
  action :create
end

postgresql_database_user 'vagrant' do
  connection postgresql_connection_info
  password 'vagrant'
  database_name 'radar'
  privileges [:all]
  action [:create, :grant]
end

postgresql_database_user 'radar' do
  connection postgresql_connection_info
  password 'vagrant'
  database_name 'radar'
  privileges [:all]
  action :grant
end
