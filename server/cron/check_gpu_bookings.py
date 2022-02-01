import os
from datetime import datetime, timedelta
import requests
import json
from fastapi.encoders import jsonable_encoder
from sqlmodel import Field, Session, SQLModel, create_engine, select

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from api.gpus import GpuBooking
from api.notifications import post_msg_to_slack, send_email

# docker-compose exec cronjob watch cat /var/log/cron.log

print(f'🔎 Checking GPU reservations to send booking notifications')


# Connect to the SQL DB
engine = create_engine(os.getenv('SQL_URL'))
SQLModel.metadata.create_all(engine)

# Query the SQL DB to get the GPU reservations
# And send msgs if reservations starts/ends today
with Session(engine) as session:
    statement = select(GpuBooking)
    results = session.exec(statement).all()
    schedule = []
    start_msgs = []
    end_msgs = []
    for resa in results:
        resa = jsonable_encoder(resa)
        schedule.append(resa)
        if datetime.fromisoformat(resa['starting_date']).date() == datetime.today().date():
            html_msg = f'✅ <b>GPU {resa["gpu_id"]}</b> in project <b>{resa["project_id"]}</b> for {resa["user_email"]}'
            start_msgs.append(html_msg)
            text_msg = f'💽 🚀 Booking starts: *GPU {resa["gpu_id"]}* in project *{resa["project_id"]}* for {resa["user_email"]} on the {datetime.today().date()}\n'
            text_msg = text_msg + """```
oc patch resourcequota/gpu-quota --patch '{"spec":{"hard": {"requests.nvidia.com/gpu": 1}}}' -n """ + resa['project_id'] + """
oc apply -f https://raw.githubusercontent.com/MaastrichtU-IDS/dsri-documentation/master/applications/gpu/template-gpu-jupyterlab.yml -n """ + resa['project_id'] + """
```"""
            
            print(post_msg_to_slack(text_msg))
            
        if datetime.fromisoformat(resa['ending_date']).date() == datetime.today().date():
            html_msg = f'❌ <b>GPU {resa["gpu_id"]}</b> in project <b>{resa["project_id"]}</b> for {resa["user_email"]}'
            end_msgs.append(html_msg)
            text_msg = f'💽 🛬 Booking ends: *GPU {resa["gpu_id"]}* in project *{resa["project_id"]}* for {resa["user_email"]} on the {datetime.today().date()}\n'
            text_msg = text_msg + """```
oc patch resourcequota/gpu-quota --patch '{"spec":{"hard": {"requests.nvidia.com/gpu": 0}}}' -n """ + resa['project_id'] + """
```"""
            print(post_msg_to_slack(text_msg))

    send_msg = ''
    if len(start_msgs) > 0:
        send_msg = send_msg + '<h2>🚀 Reservations starting</h2>\n<p>\n' + '</p>\n<p>'.join(start_msgs) + '\n</p>\n'
    if len(end_msgs) > 0:
        send_msg = send_msg + '\n<h2>🛬 Reservations ending</h2>\n<p>\n' + '</p>\n<p>'.join(end_msgs) + '\n</p>\n'
    
    ## Send email disabled because UM smtp not reachable from IDS servers
    # if len(send_msg) > 0:
    #     send_email(send_msg)
