### Harness-Docker-Runner Setup

1. Create the service file:
```sudo vi /etc/systemd/system/harness-runner.service```

2. Paste the following configuration:
```toml
[Unit]
Description=Harness Docker Runner
After=network.target docker.service

[Service]
Type=simple
User=root
WorkingDirectory=/root
# StandardOutput routes the console output to your log file
ExecStart=/bin/bash -c './harness-docker-runner-linux-amd64 server >> /root/harness-runner.log 2>&1'
Restart=always

[Install]
WantedBy=multi-user.target
```
3. Reload and Enable:
```
sudo systemctl daemon-reload
sudo systemctl enable harness-runner.service
sudo systemctl start harness-runner.service
```
