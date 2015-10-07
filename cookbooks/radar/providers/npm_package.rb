include Chef::Mixin::ShellOut

provides :npm_package

use_inline_resources

def package_installed?(package_name)
  cmd = shell_out("npm -j -g ls | jq -r .dependencies.#{package_name}.version")
  cmd.stdout != 'null'
end

action :install do
  unless @current_resource.installed
    execute "npm install -g #{new_resource.package_name}" do
      command "npm install -g #{new_resource.package_name}"
      user 'root'
      action :run
    end
  end
end

def load_current_resource
  @current_resource = Chef::Resource::RadarNpmPackage.new(new_resource.name)
  @current_resource.package_name(new_resource.package_name)
  @current_resource.installed = package_installed?(new_resource.package_name)
  @current_resource
end
