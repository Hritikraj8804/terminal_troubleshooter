# game/data/levels.py

LEVELS = [
    {
        "id": "level_01_web_server_down",
        "title": "Urgent: Web Server Down!",
        "description": (
            "The corporate website is completely unreachable. Customers are furious! "
            "Your first task is to identify the web server process and restart it. "
            "Start by listing all running processes to find potential issues."
        ),
        "steps": [
            {
                "task": "Find the Apache process (PID 1234) using `ps aux` and then restart the apache2 service.",
                "expected_commands": [
                    {"command": "ps aux", "check_type": "contains"},
                    {"command": "systemctl restart apache2", "check_type": "exact"},
                    {"command": "sudo systemctl restart apache2", "check_type": "exact"}
                ],
                "on_success": {
                    "message": "You successfully restarted the Apache service! The website is back online!",
                    "xp_reward": 50,
                    "state_changes": [
                        {"type": "process_state", "pid": 1234, "new_state": "running"}
                    ],
                    "simulated_output": {
                        "ps aux": (
                            "USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND\n"
                            "root         1  0.0  0.1 106708  6908 ?        Ss   May20   0:01 /sbin/init\n"
                            "sysadmin  1234  0.5  2.0 200000 150000 ?       S    10:30   0:05 /usr/sbin/apache2 -k start\n" # Target
                            "root      5678  0.0  0.1  25000  1200 ?        S    May20   0:00 /usr/bin/python3 /opt/monitoring/monitor.py"
                        ),
                        "systemctl restart apache2": "Job for apache2.service canceled.\nFailed to restart apache2.service: Unit apache2.service not found."
                    },
                    "hint_on_fail": "Remember to use 'ps aux' to see all running processes. Then, to restart a service, you usually use 'systemctl restart <service_name>'."
                }
            }
        ]
    },
    {
        "id": "level_02_disk_space_full",
        "title": "Disk Space Crisis!",
        "description": (
            "Alert! The server's `/var/log` directory is critically full, preventing new logs from being written. "
            "This is causing other services to fail. Your mission: find the largest log file and delete it to free up space. "
            "Remember to be careful what you delete!"
        ),
        "steps": [
            {
                "task": "Identify the largest file in `/var/log` using `du -sh` and then delete it using `rm`.",
                "expected_commands": [
                    {"command": "du -sh /var/log", "check_type": "contains"}, # To see total size
                    {"command": "du -sh /var/log/*", "check_type": "contains"}, # To list file sizes
                    {"command": "rm /var/log/syslog", "check_type": "exact"} # Specific file to delete
                ],
                "on_success": {
                    "message": "Disk space cleared! The log service is now functioning normally.",
                    "xp_reward": 75,
                    "state_changes": [
                        {"type": "delete_file", "path": "/var/log/syslog"}
                    ],
                    "simulated_output": {
                        "du -sh /var/log": "1.5G    /var/log",
                        "du -sh /var/log/*": (
                            "1.4G    /var/log/syslog\n"
                            "8.0K    /var/log/auth.log\n"
                            "4.0K    /var/log/kern.log"
                        ),
                        "rm /var/log/syslog": "" # Empty string for successful deletion
                    },
                    "hint_on_fail": "To find large files, 'du -sh' is useful. To delete files, 'rm' is the command."
                }
            }
        ]
    },
    {
        "id": "level_03_kubernetes_pending_pod",
        "title": "Kubernetes Pod Stuck!",
        "description": (
            "A critical backend service pod in your Kubernetes cluster is stuck in a 'Pending' state. "
            "This is affecting user logins. Diagnose why the pod isn't starting and fix it."
        ),
        "steps": [
            {
                "task": "First, list all pods to confirm the status. Then, describe the problematic pod to find the root cause.",
                "expected_commands": [
                    {"command": "kubectl get pods", "check_type": "contains"},
                    {"command": "kubectl describe pod backend-efgh-67890", "check_type": "exact", "required_output_match": "Insufficient cpu"} # This is the key check!
                ],
                "on_success": {
                    "message": "Excellent! You found the 'Insufficient cpu' error. Now, scale up the backend deployment to add more resources.",
                    "xp_reward": 40,
                    "state_changes": [], # No state change until scaling
                    "simulated_output_overrides": {
                        "kubectl get pods": ( # Override default parser output for clarity
                            "NAME                             READY   STATUS    RESTARTS   AGE\n"
                            "frontend-abcd-12345              1/1     Running   0          2h\n"
                            "backend-efgh-67890               0/1     [yellow]Pending[/]   0          2h\n" # Highlight pending
                            "nginx-app-xyz-54321              1/1     Running   0          2d"
                        )
                    },
                    "hint_on_fail": "Use 'kubectl get pods' to see all pods, then 'kubectl describe pod <pod_name>' for details."
                }
            },
            {
                "task": "You've identified the CPU issue. Scale the 'backend' deployment to 2 replicas to resolve the resource constraint.",
                "expected_commands": [
                    {"command": "kubectl scale deployment backend --replicas=2", "check_type": "exact"}
                ],
                "on_success": {
                    "message": "Success! The backend deployment was scaled, and the pod is now running!",
                    "xp_reward": 80,
                    "state_changes": [
                        {"type": "k8s_scale_deployment", "deployment_name": "backend", "replicas": 2},
                        {"type": "k8s_pod_status", "pod_name": "backend-efgh-67890", "new_status": "Running"} # Pod should now be running
                    ],
                    "simulated_output_overrides": {
                        "kubectl scale deployment backend --replicas=2": "deployment.apps/backend scaled"
                    },
                    "hint_on_fail": "To scale a Kubernetes deployment, use 'kubectl scale deployment <name> --replicas=<count>'."
                }
            }
        ]
    }
    # Add more levels here...
]