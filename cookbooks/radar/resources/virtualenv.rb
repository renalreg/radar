resource_name :virtualenv

actions :create, :delete
default_action :create

attribute :path, :name_attribute => true, :kind_of => String, :required => true
attribute :python_path, :kind_of => String, :default => '/usr/bin/python'
attribute :user, :kind_of => String, :default => 'root'
attribute :group, :kind_of => String, :default => 'root'
attribute :packages, :kind_of => Hash, :default => {}
attribute :environment, :kind_of => Hash, :default => {}
