# Access Shell on Colab / Kaggle Notebook server

## Installation

Installation is easy!

```
$ pip install git+https://github.com/sandyz1000/colabshell.git
```

Run ttyd server on Google Colab or Kaggle Notebooks

## Getting Started


ColabShell also has a command-line script. So you can just run `colabshell` from command line.

`colabshell -h` will give the following:

```
usage: colabshell [-h] PORT [--password PASSWORD] [--mount_drive] [--settings_ini kafka-settings.ini]

ColabShell: Run TTYD server On Colab / Kaggle Notebooks to access the GPU machine from SHELL

required arguments:
  port PORT          the port you want to run ttyd server on

optional arguments: 
  --credential CREDENTIAL  username and password to protect your shell from unauthorized access, format username:password
  --mount_drive        if you use --mount_drive, your google drive will be mounted
  --settings_ini       Settings.ini if you want to log to kafka and listen from remote workstation
```


### Your typical settings.ini file will look like this

```

[DEFAULT]
timeout = 2000000
log_level = DEBUG
log_dir = logs

; General log configuration
[LOG_FORMATTER]
to_json=True
format=%(asctime)s:%(levelname)s:%(name)s:%(message)s
; # format='%(relativeCreated)6.1f %(threadName)12s: %(levelname).1s %(module)8.8s:%(lineno)-4d %(message)s',
log_max_bytes=1024 * 1024 * 10
log_backups=5
relay_stdout=True

; # Kafka Configuration
[KAFKA]
bootstrap_servers = localhost:9094
username =
password =
topics = default,decentlog
timeout=${DEFAULT:timeout}
group_id=default-consumer
sasl_plain_username=
sasl_plain_password=
kafka_retry=5
sasl_mechanism=
security_protocol=PLAINTEXT

```
## Starting ttyd server from SHELL
```bash
colabshell 10001 interactive --credential=user:password --settings_ini=kafka-settings.ini
```

## Starting ttyd server from Notebook
```
from colabshell import ColabShell
shell = ColabShell(
  port=10001, 
  username='colabshell', password='password', 
  mount_drive=/home/gdrive, 
  settings_ini='kafka-settings.ini'
)
shell.run()
```

For more info about the shell check this link: https://github.com/tsl0922/ttyd