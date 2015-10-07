package 'scl-utils' do
  action :install
end

remote_file "#{Chef::Config['file_cache_path']}/rhscl-python27-epel-6-x86_64.noarch.rpm" do
  source 'https://www.softwarecollections.org/en/scls/rhscl/python27/epel-6-x86_64/download/rhscl-python27-epel-6-x86_64.noarch.rpm'
  action :create
end

rpm_package 'rhscl-python27' do
 source "#{Chef::Config['file_cache_path']}/rhscl-python27-epel-6-x86_64.noarch.rpm"
 action :install
end

package 'python27' do
  action :install
end
