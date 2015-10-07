package 'nodejs' do
  action :install
end

package 'npm' do
  action :install
end

# Update npm (nodejs comes with 1.x)
node_module 'npm' do
  action :install
end
