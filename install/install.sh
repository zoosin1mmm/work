mkdir dqa
cd dqa/
git clone  git@github.com:exosite/dqa-murano.git
git clone git@github.com:exosite-StacyChen/work.git
git clone git@github.com:exosite/dqa-env.git
git clone git@github.com:exosite/dqa-mqtt.git
sudo apt-get install python-pip
sudo  python dqa-env/exo-robot-runner setup
sudo  python dqa-env/exo-robot-runner setup
sudo pip install robotframework
sudo pip2 install --upgrade robotframework-httplibrary
python dqa-env/exo-openshift-hopper setup
python dqa-env/exo-openshift-hopper login
sudo add-apt-repository ppa:webupd8team/sublime-text-3
sudo apt-get update
sudo apt-get install sublime-text-installer
sudo apt-get update
sudo apt-get install kolourpaint4
curl -fsSL get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo apt-add-repository ppa:brightbox/ruby-ng
sudo apt-get update
sudo apt-get install ruby2.4
sudo npm install -g wscat
sudo npm cache clean -f
sudo npm install -g n
sudo n stable
sudo apt-get install jq