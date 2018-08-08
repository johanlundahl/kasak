# Kasak reports

Daily and weekly reporting for the activity at Kasak. This is a set of python scripts that 
creates a summary for the activity at Kasak and post it to a Slack app.

### Prerequisites

The following modules installed

```
$ apt-get install python-requests
```

### Installing

Start by cloning the git repo
```
$ git clone https://github.com/johanlundahl/kasak_report
```

There are two parameters that need to be defined for the scripts to function properly. Create a file called kasak_params.py
```
$ touch kasak_params.py
``` 
And define URL's to a Slack app and the Kasak app that contains the data
```
slack_webhook_url = 'url-to-a-slack-app'
kasak_carstatus_url = 'url-to-the-kasak-carstatus-endpoint'
```

Set up crontab jobs to schedule the scripts. Edit crontab by
```
$ crontab -e
```

Define which time the different jobs should be run at, e.g.
```
0 * * * * python3 /home/pi/kasak_report/alive_check.py
45 7 * * 1 python3 /home/pi/kasak_report/week_plan.py
0 8 * * 1-5 python3 /home/pi/kasak_report/day_plan.py
0 16 * * 1-5 python3 /home/pi/kasak_report/day_summary.py
15 16 * * 5 python3 /home/pi/kasak_report/week_summary.py

