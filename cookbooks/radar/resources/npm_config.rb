require 'shellwords'

resource_name :npm_config

property :key, String, name_property: true
property :value, String

action :create do
  command = 'npm config --global '
  escaped_key = key.to_s.shellescape

  if value
    escaped_value = value.to_s.shellescape
    command << "set #{escaped_key} #{escaped_value}"
  else
    command << "delete #{escaped_key}"
  end

  execute "set #{key} in npm config" do
    command command
    user 'root'
    action :run
  end
end

action :delete do
  escaped_key = key.to_s.shellescape

  execute "delete #{key} from npm config" do
    command "npm config --global delete #{escaped_key}"
    user 'root'
    action :run
  end
end
