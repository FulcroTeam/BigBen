#start this with a crontab like
#@reboot sh /BigBen/BigBen.sh
#using crontab -e

cd BigBen

mkdir logs
chmod 777 logs

python3 server.py >> logs/server-log.txt 2>&1 &

cd api
python3 api.py >> ../logs/api-log.txt 2>&1 &


