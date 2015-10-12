source 'https://supermarket.chef.io'

cookbook 'radar', path: 'cookbooks/radar'

# This overrides the postgresql dependency in the database cookbook
# Our version supports PostgreSQL 9.4 on CentOS 7
# FIXME https://github.com/hw-cookbooks/postgresql/pull/269
cookbook 'postgresql', git: 'https://github.com/renalreg/postgresql.git'
