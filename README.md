# mirrors_checker
Checks availability of a given list of mirrors in most of the countries using SmartProxy.  
  
_Linted with flake8 and black_

# How to run
 
- download/clone project to your IDE
- install python 3+ interpreter 
- install requirements using prompt: **pip install -r requirements.txt** 
- create file configs.py and put your proxy credentials and mirrors inside it
- run proxy_connect_async.py or proxy_connect.py for async or sync respectively 

## Logging

In both use cases script saves results of its work to py_log.log


# Example of configs.py

![image](https://user-images.githubusercontent.com/100962655/221351771-36e4c872-008b-473a-a376-d31456fbc09b.png)

