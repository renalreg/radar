resource_name :virtualenv

actions :create, :delete
default_action :create

attribute :path, :name_attribute => true, :kind_of => String, :required => true
attribute :owner, :kind_of => String, :required => true, :default => 'root'
attribute :group, :kind_of => String, :required => true, :default => 'root'
attribute :packages, :kind_of => Hash, :required => true, :default => {}
attribute :python_path, :kind_of => String, :required => true, :default => '/usr/bin/python'
