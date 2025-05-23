# game/game_state.py

class GameState:
    """
    Manages the current state of the simulated server environment and player progress.
    This includes the file system, running processes, Docker containers, Kubernetes pods,
    and player XP.
    """
    def __init__(self):
        self.player_xp = 0
        self.current_level_id = "level_01_web_server_down" # Starting level ID

        # --- Simulated Environment ---
        # File System (simplified: just directories and files, no content yet)
        self.filesystem = {
            '/': {
                'bin': {},
                'etc': {
                    'apache2': {'apache2.conf': 'config content'},
                    'nginx': {'nginx.conf': 'config content'},
                    'my_app_conf': {'app.conf': 'some app config'},
                    'passwd': 'root:x:0:0:root:/root:/bin/bash\nsysadmin:x:1000:1000:sysadmin:/home/sysadmin:/bin/bash'
                },
                'home': {
                    'sysadmin': {
                        'reports': {},
                        'documents': {'important_doc.txt': 'Sensitive data here.'}
                    },
                    'guest': {}
                },
                'var': {
                    'log': {
                        'syslog': 'May 22 10:00:01 server systemd[1]: Started Session 1 of user sysadmin.\nMay 22 10:05:05 server apache2[1234]: AH00558: apache2: Could not reliably determine the server\'s fully qualified domain name\nMay 22 10:05:10 server apache2[1234]: (98)Address already in use: AH00072: make_sock: could not bind to address 0.0.0.0:80\nMay 22 10:05:11 server apache2[1234]: No space left on device\nMay 22 10:05:12 server systemd[1]: apache2.service: Control process exited, code=exited status=1\nMay 22 10:05:13 server systemd[1]: apache2.service: Failed with result \'exit-code\'.\nMay 22 10:05:15 server CRON[12345]: (root) CMD (command -v dracut > /dev/null && dracut -c /etc/dracut.conf --force --kver 5.15.0-78-generic)'
                    },
                    'www': {'html': {'index.html': '<html><body><h1>It works!</h1></body></html>'}}
                },
                'tmp': {}
            }
        }
        # Processes: PID, Name, State (running, stopped, killed), Command
        self.processes = {
            1: {'name': 'systemd', 'state': 'running', 'command': '/sbin/init'},
            1234: {'name': 'apache2', 'state': 'stopped', 'command': '/usr/sbin/apache2 -k start'},
            5678: {'name': 'monitor.py', 'state': 'running', 'command': '/usr/bin/python3 /opt/monitoring/monitor.py'},
            9000: {'name': 'nginx', 'state': 'running', 'command': '/usr/sbin/nginx -g "daemon on;"'}
        }
        # Docker Containers: ID, Name, Image, Status (running, exited), Port mapping
        self.docker_containers = {
            'a1b2c3d4e5f6': {'name': 'web_app_prod', 'image': 'nginx:latest', 'status': 'exited', 'ports': '80->80/tcp'},
            'b2c3d4e5f6a7': {'name': 'db_service', 'image': 'postgres:13', 'status': 'running', 'ports': '5432->5432/tcp'}
        }
        # Kubernetes Pods (simplified: just name, status, namespace, related deployment)
        self.kubernetes_pods = {
            'frontend-abcd-12345': {'name': 'frontend-abcd-12345', 'status': 'Running', 'namespace': 'default', 'deployment': 'frontend'},
            'backend-efgh-67890': {'name': 'backend-efgh-67890', 'status': 'Pending', 'namespace': 'default', 'deployment': 'backend'},
            'nginx-app-xyz-54321': {'name': 'nginx-app-xyz-54321', 'status': 'Running', 'namespace': 'devops-tools', 'deployment': 'nginx-app'}
        }
        # Kubernetes Deployments (simplified: name, replicas)
        self.kubernetes_deployments = {
            'frontend': {'name': 'frontend', 'replicas': 1},
            'backend': {'name': 'backend', 'replicas': 1},
            'nginx-app': {'name': 'nginx-app', 'replicas': 2}
        }

    def add_xp(self, amount: int):
        """Adds XP to the player's score."""
        self.player_xp += amount

    def get_file_content(self, path: str) -> str | None:
        """Simulates getting file content."""
        parts = path.strip('/').split('/')
        current_dir = self.filesystem['/']
        for part in parts:
            if part in current_dir:
                if isinstance(current_dir[part], dict): # It's a directory
                    current_dir = current_dir[part]
                else: # It's a file
                    return current_dir[part]
            else:
                return None # File or path not found
        return None # Path ended in a directory, not a file

    def update_process_state(self, pid: int, new_state: str):
        """Updates the state of a simulated process."""
        if pid in self.processes:
            self.processes[pid]['state'] = new_state
            return True
        return False

    def update_docker_container_status(self, container_id: str, new_status: str):
        """Updates the status of a simulated Docker container."""
        if container_id in self.docker_containers:
            self.docker_containers[container_id]['status'] = new_status
            return True
        return False

    def update_kubernetes_pod_status(self, pod_name: str, new_status: str):
        """Updates the status of a simulated Kubernetes pod."""
        if pod_name in self.kubernetes_pods:
            self.kubernetes_pods[pod_name]['status'] = new_status
            return True
        return False

    def scale_kubernetes_deployment(self, deployment_name: str, replicas: int):
        """Updates the replica count for a simulated Kubernetes deployment."""
        if deployment_name in self.kubernetes_deployments:
            self.kubernetes_deployments[deployment_name]['replicas'] = replicas
            return True
        return False

    def add_directory(self, path: str, name: str):
        """Simulates creating a directory."""
        parts = path.strip('/').split('/')
        current_dir = self.filesystem['/']
        for part in parts:
            if part in current_dir and isinstance(current_dir[part], dict):
                current_dir = current_dir[part]
            else:
                return False # Path segment not found or not a directory

        if name not in current_dir:
            current_dir[name] = {}
            return True
        return False # Directory already exists or name invalid

    def delete_file_or_dir(self, path: str) -> bool:
        """Simulates deleting a file or directory."""
        parts = path.strip('/').split('/')
        if not parts or parts == ['']:
            return False # Cannot delete root

        parent_dir = self.filesystem['/']
        target_name = parts[-1]
        
        # Traverse to the parent directory
        for part in parts[:-1]:
            if part in parent_dir and isinstance(parent_dir[part], dict):
                parent_dir = parent_dir[part]
            else:
                return False # Path to parent not found or not a directory

        if target_name in parent_dir:
            del parent_dir[target_name]
            return True
        return False # Target not found