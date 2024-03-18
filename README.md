## AWS Deployment Steps
1. Login to AWS console 
2. Launch EC2 instance of Ubuntu, t2.large with http and https. 
3. Open terminal and run below commands for machine update and deployment
```bash
sudo apt update
sudo apt-get update
sudo apt upgrade -y
sudo apt install git curl unzip tar make sudo vim wget -y
sudo apt install python3-pip
```
4. git clone [this repo]
5. vi .env
6. Paste [openai key] Esc :wq
7. pip3 install -r requirements.txt
8. From Instance Summary Page > Security > click sg- under Security Groups
9. Inbound rules > Edit Inbound rules > Scroll down > Add rule 
10. Type: Custom TCP, Port range: 8501; Source: Anywhere IPv4 - 0.0.0.0/0; Save rules
11. From EC2 terminal - 
```bash
python3 -m streamlit run StreamlitAPP.py
```
14. Open  - http://public_url:8501/ 
