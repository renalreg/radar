resource_name :npm_package

actions :install
default_action :install

attribute :package_name, :name_attribute => true, :kind_of => String, :required => true

attr_accessor :installed
