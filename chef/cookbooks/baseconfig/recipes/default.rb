# Make sure the Apt package lists are up to date, so we're downloading versions that exist.
cookbook_file "apt-sources.list" do
  path "/etc/apt/sources.list"
end
execute 'apt_update' do
  command 'apt-get update'
end

# Base configuration recipe in Chef.
package "python-pip"

execute 'install flask' do
	command 'pip install flask'
end

execute  'install login' do
	command 'pip install flask-login'
end

execute  'install flask-sqlalchemy' do
	command 'pip install flask-sqlalchemy'
end

execute  'install flask-sqlalchemy-migrate' do
	command 'pip install sqlalchemy-migrate'
end

execute  'install flask-whooshalc' do
	command 'pip install flask-whooshalchemy'
end

execute  'install flask-wtf' do
	command 'pip install flask-wtf'
end

execute  'install flask-babel' do
	command 'pip install flask-babel'
end

execute  'install flask-guess-language' do
	command 'pip install guess_language'
end

execute  'install flask-flip-flop' do
	command 'pip install flipflop'
end

execute  'install flask-coverage' do
	command 'pip install coverage'
end

execute  'install Rauth' do
	command 'pip install rauth'
end

execute  'run server' do
	command 'python run.py &'
	cwd '/home/vagrant/project'
end

