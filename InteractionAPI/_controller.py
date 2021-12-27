import daemon
import os

from pid import PidFile

from app import run
from app import app 


p = PidFile(pidname="api_flask", piddir="/home/pi/pi-automations/InteractionAPI")


with daemon.DaemonContext(pidfile=p):
	run(app)
