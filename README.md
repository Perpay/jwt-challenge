# jwt-challenge


Instructions:

1: Install Python if your machine does not have it (https://www.python.org/downloads/)
2. Depending on your Python version, you should already have Pip. If not, install Pip
   (https://pip.pypa.io/en/stable/installing/)
3: Run the following commands:
    pip install virtualenv
    pip install virtualenvwrapper
    export WORKON_HOME=~/Envs
    source /usr/local/bin/virtualenvwrapper.sh
    mkvirtualenv perpay-challenge
    workon perpay-challenge
4. The preceding commands will create a new working environment as to not interfere with your typical workspace.
   Any time that you go to run this project in a new shell, just run "workon perpay-challenge" to switch back to that
   environment.
5. Then run the following:
   git clone https://github.com/Perpay/jwt-challenge.git
6. Then cd into the jwt-challenge directory and run:
    pip install -r requirements.txt
