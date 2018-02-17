# Configuration Step  

1. Install Python  
1.1. Add Python respository: `sudo add-apt-repository ppa:jonathonf/python-3.6`  
1.2. Update the O.S.: `sudo apt-get update`  
1.3. Install Python 3.6: `sudo apt install python3.6`  

2. Install Pip: `sudo apt-get install python3-pip`  

3. Install Rpyc: `sudo pip3 install rpyc`  

4. Install Sqlite 3: `sudo apt install sqlite3 libsqlite3-dev`  

# Run Step  

1. Clone the project: `git@github.com:DiegoCorrea/bottleOfMessages.git`  

2. Go to Project path: `cd bottleOfMessages/`  

3. Go to the Server path: `cd servers/`  

4. Exu:  
4.1. Go to Exu Server path: `cd Exu/`  
4.2. Create a Schema: `python3.6 schema.py`  
4.3. Run the Server: `python3.6 main.py`  

4. Hermes:  
4.1. Go to Exu Server path: `cd Hermes/`  
4.2. Create a Schema: `python3.6 schema.py`  
4.3. Run the Server: `python3.6 main.py`  

4. Thot:  
4.1. Go to Exu Server path: `cd Thot/`  
4.2. Create a Schema: `python3.6 schema.py`  
4.3. Run the Server: `python3.6 main.py`  

4. WhatsApp:  
4.1. Go to Exu Server path: `cd WhatsApp/`  
4.2. Create a Schema: `python3.6 schema.py`  
4.3. Run the Server: `python3.6 main.py`  

6. Run the Client  
4.1 Go to the Client path: `cd client/`  
4.2. Run the Client: `python3.6 client.py`  
