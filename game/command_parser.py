# game/command_parser.py

from .game_state import GameState
from typing import Dict, List, Any # Add this line

class CommandParser:
    """
    Parses user input commands and simulates their execution against the GameState.
    Returns simulated output and applies necessary state changes.
    """
    def __init__(self, game_state: GameState):
        self.game_state = game_state

    def parse_and_execute(self, command_line: str) -> Dict[str, Any]:
        """
        Parses a command line string, simulates its execution, and returns results.
        Returns a dictionary with 'output', 'success', and 'state_changes' (if any).
        """
        parts = command_line.strip().split()
        if not parts:
            return {"output": "", "success": False, "message": ""}

        cmd = parts[0].lower()
        args = parts[1:]

        # --- Basic Linux Commands ---
        if cmd == "ls":
            return self._handle_ls(args)
        elif cmd == "cd":
            return self._handle_cd(args) # Not fully implemented for game progression, just simulation
        elif cmd == "cat":
            return self._handle_cat(args)
        elif cmd == "grep":
            return self._handle_grep(args)
        elif cmd == "ps":
            return self._handle_ps(args)
        elif cmd == "kill":
            return self._handle_kill(args)
        elif cmd == "du":
            return self._handle_du(args)
        elif cmd == "rm":
            return self._handle_rm(args)
        elif cmd == "mkdir":
            return self._handle_mkdir(args)
        elif cmd == "find":
            return self._handle_find(args)
        elif cmd == "head":
            return self._handle_head(args)
        elif cmd == "tail":
            return self._handle_tail(args)
        elif cmd == "chmod":
            return self._handle_chmod(args)
        elif cmd == "mv":
            return self._handle_mv(args)
        elif cmd == "cp":
            return self._handle_cp(args)
        elif cmd == "sudo":
            # For simplicity, just unwrap the next command. No actual permission check.
            if len(args) > 0:
                return self.parse_and_execute(" ".join(args))
            return {"output": "sudo: no command specified", "success": False, "message": "Specify a command after sudo."}

        # --- Systemctl Commands ---
        elif cmd == "systemctl":
            return self._handle_systemctl(args)

        # --- Docker Commands ---
        elif cmd == "docker":
            return self._handle_docker(args)

        # --- Kubernetes Commands (kubectl) ---
        elif cmd == "kubectl":
            return self._handle_kubectl(args)

        # --- Default/Unknown Command ---
        else:
            return {"output": f"bash: {cmd}: command not found", "success": False, "message": f"Unknown command: {cmd}"}

    # --- Internal Command Handlers ---

    def _get_path_parts(self, path: str) -> List[str]:
        """Helper to split a path into parts, handling leading/trailing slashes."""
        return [p for p in path.strip('/').split('/') if p]

    def _traverse_path(self, path_parts: List[str]):
        """Helper to traverse the simulated filesystem and return the target directory/file."""
        current_node = self.game_state.filesystem['/']
        for part in path_parts:
            if isinstance(current_node, dict) and part in current_node:
                current_node = current_node[part]
            else:
                return None # Path not found
        return current_node

    def _handle_ls(self, args: List[str]) -> Dict[str, Any]:
        path = args[0] if args and not args[0].startswith('-') else '/'
        target_node = self._traverse_path(self._get_path_parts(path))

        if target_node is None:
            return {"output": f"ls: cannot access '{path}': No such file or directory", "success": False}
        if not isinstance(target_node, dict): # It's a file, not a directory
             return {"output": f"{path}\n", "success": True}

        output_lines = []
        for name, content in target_node.items():
            if isinstance(content, dict):
                output_lines.append(f"[blue]{name}[/]") # Directory
            else:
                output_lines.append(name) # File
        return {"output": "\n".join(output_lines), "success": True}

    def _handle_cd(self, args: List[str]) -> Dict[str, Any]:
        # For simplicity, `cd` just checks path existence, doesn't change game_state current dir.
        # This is more for simulating output than actual in-game navigation.
        if not args:
            return {"output": "", "success": True, "message": "Changed to home directory (simulated)."}
        
        path = args[0]
        target_node = self._traverse_path(self._get_path_parts(path))

        if target_node is None:
            return {"output": f"cd: {path}: No such file or directory", "success": False}
        if not isinstance(target_node, dict):
            return {"output": f"cd: {path}: Not a directory", "success": False}
        
        return {"output": "", "success": True, "message": f"Changed directory to {path} (simulated)."}

    def _handle_cat(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return {"output": "cat: missing operand", "success": False}
        path = args[0]
        content = self.game_state.get_file_content(path)
        if content is None:
            return {"output": f"cat: {path}: No such file or directory", "success": False}
        return {"output": content, "success": True}

    def _handle_grep(self, args: List[str]) -> Dict[str, Any]:
        if len(args) < 2:
            return {"output": "grep: missing operand", "success": False}
        
        pattern = args[0]
        path = args[1]
        
        file_content = self.game_state.get_file_content(path)
        if file_content is None:
            return {"output": f"grep: {path}: No such file or directory", "success": False}
        
        matching_lines = [line for line in file_content.splitlines() if pattern in line]
        return {"output": "\n".join(matching_lines), "success": True}

    def _handle_ps(self, args: List[str]) -> Dict[str, Any]:
        output_lines = ["USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND"]
        
        # Sort by PID for consistent output
        sorted_pids = sorted(self.game_state.processes.keys())
        
        for pid in sorted_pids:
            proc_data = self.game_state.processes[pid]
            # Simplified representation, similar to actual ps aux
            state_char = proc_data['state'][0].upper() if proc_data['state'] else '?'
            output_lines.append(f"root       {pid:<5}  0.0  0.0 100000  5000 ?        {state_char}    10:00   0:00 {proc_data['command']}")
        return {"output": "\n".join(output_lines), "success": True}

    def _handle_kill(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return {"output": "kill: usage: kill [-s signal | -p] [-a] pid ...", "success": False}
        
        try:
            # Handle kill -9 <PID>
            pid_arg_index = 0
            if '-9' in args:
                pid_arg_index = args.index('-9') + 1
                if pid_arg_index >= len(args):
                    return {"output": "kill: no pid specified after -9", "success": False}
            
            pid = int(args[pid_arg_index])
            if self.game_state.update_process_state(pid, 'killed'):
                return {"output": "", "success": True, "message": f"Process {pid} killed."}
            else:
                return {"output": f"kill: ({pid}) - No such process", "success": False, "message": f"Process {pid} not found."}
        except ValueError:
            return {"output": f"kill: {args[-1]}: arguments must be process or job IDs", "success": False}
        except IndexError:
            return {"output": "kill: usage: kill [-s signal | -p] [-a] pid ...", "success": False}

    def _handle_du(self, args: List[str]) -> Dict[str, Any]:
        path = args[-1] if args and not args[0].startswith('-') else '/' # Take last arg as path if options present
        if path == "*": # Special handling for common `du -sh /*` or `du -sh /var/log/*`
            path = "/".join(self._get_path_parts(path[:-1])) # Get parent dir
        
        if not path or path == "":
             path = "/"

        # Simplified for specific levels.
        # In a real impl, you'd calculate sizes based on simulated content.
        if "/var/log" in path:
            if not self.game_state.get_file_content("/var/log/syslog"):
                return {"output": "12K    /var/log", "success": True} # After syslog deleted
            else:
                return {"output": "1.5G    /var/log", "success": True}
        
        if "/var/log/*" in path:
            if not self.game_state.get_file_content("/var/log/syslog"):
                return {"output": "8.0K    /var/log/auth.log\n4.0K    /var/log/kern.log", "success": True}
            else:
                 return {"output": "1.4G    /var/log/syslog\n8.0K    /var/log/auth.log\n4.0K    /var/log/kern.log", "success": True}

        # Fallback for other paths - very basic
        return {"output": f"4.0K    {path}", "success": True} # Default very small

    def _handle_rm(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return {"output": "rm: missing operand", "success": False}
        
        path = args[-1] # Simplistic: assume last arg is path
        
        if self.game_state.delete_file_or_dir(path):
            return {"output": "", "success": True, "message": f"Successfully removed {path}."}
        else:
            return {"output": f"rm: cannot remove '{path}': No such file or directory", "success": False, "message": "Failed to remove file/directory."}

    def _handle_mkdir(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return {"output": "mkdir: missing operand", "success": False}
        
        path_parts = self._get_path_parts(args[0])
        if not path_parts: # Root directory
            return {"output": "mkdir: cannot create directory '/': File exists", "success": False}

        parent_path = "/" + "/".join(path_parts[:-1]) # Reconstruct parent path
        new_dir_name = path_parts[-1]

        if self.game_state.add_directory(parent_path, new_dir_name):
            return {"output": "", "success": True, "message": f"Directory '{args[0]}' created."}
        else:
            return {"output": f"mkdir: cannot create directory '{args[0]}': File exists or parent path not found", "success": False}
            
    def _handle_find(self, args: List[str]) -> Dict[str, Any]:
        # Very simplified find, primarily for 'find . -name <filename>' or 'find / -name <filename>'
        if len(args) < 3 or args[1] != '-name':
            return {"output": "find: not enough arguments or unsupported syntax. Try 'find <path> -name <filename>'", "success": False}

        search_path_parts = self._get_path_parts(args[0])
        filename_pattern = args[2].lower() # Case-insensitive match for simplicity
        
        # Traverse the specified search path
        current_node = self._traverse_path(search_path_parts)
        if current_node is None or not isinstance(current_node, dict):
            return {"output": f"find: '{args[0]}': No such file or directory", "success": False}

        found_paths = []
        # Recursive search helper
        def _search_recursive(node, current_full_path):
            if isinstance(node, dict):
                for name, content in node.items():
                    full_path = f"{current_full_path}/{name}"
                    if filename_pattern in name.lower(): # Basic 'contains' match for filename
                        found_paths.append(full_path)
                    _search_recursive(content, full_path)
            # If it's a file, no further recursion needed

        _search_recursive(current_node, "/".join(search_path_parts) if search_path_parts else "")

        if not found_paths:
            return {"output": "", "success": True, "message": "No matching files found."}
        return {"output": "\n".join(found_paths), "success": True}

    def _handle_head(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return {"output": "head: missing operand", "success": False}
        
        num_lines = 10 # Default
        path_index = 0

        if args[0].startswith('-n'):
            try:
                num_lines = int(args[0][2:])
                path_index = 1
            except ValueError:
                return {"output": "head: invalid number of lines: '{}'".format(args[0][2:]), "success": False}
        elif args[0] == '-n' and len(args) > 1:
            try:
                num_lines = int(args[1])
                path_index = 2
            except ValueError:
                return {"output": "head: invalid number of lines: '{}'".format(args[1]), "success": False}
        
        if len(args) <= path_index:
            return {"output": "head: missing operand", "success": False}
            
        path = args[path_index]
        content = self.game_state.get_file_content(path)
        if content is None:
            return {"output": f"head: {path}: No such file or directory", "success": False}
        
        lines = content.splitlines()
        output_lines = lines[:num_lines]
        return {"output": "\n".join(output_lines), "success": True}

    def _handle_tail(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return {"output": "tail: missing operand", "success": False}
        
        num_lines = 10 # Default
        path_index = 0

        if args[0].startswith('-n'):
            try:
                num_lines = int(args[0][2:])
                path_index = 1
            except ValueError:
                return {"output": "tail: invalid number of lines: '{}'".format(args[0][2:]), "success": False}
        elif args[0] == '-n' and len(args) > 1:
            try:
                num_lines = int(args[1])
                path_index = 2
            except ValueError:
                return {"output": "tail: invalid number of lines: '{}'".format(args[1]), "success": False}
        
        if len(args) <= path_index:
            return {"output": "tail: missing operand", "success": False}
            
        path = args[path_index]
        content = self.game_state.get_file_content(path)
        if content is None:
            return {"output": f"tail: {path}: No such file or directory", "success": False}
        
        lines = content.splitlines()
        output_lines = lines[-num_lines:]
        return {"output": "\n".join(output_lines), "success": True}

    def _handle_chmod(self, args: List[str]) -> Dict[str, Any]:
        if len(args) < 2:
            return {"output": "chmod: missing operand", "success": False}
        
        mode = args[0]
        path = args[1]
        
        # Simple simulation: just check if file exists. No actual permission changes.
        target_node = self._traverse_path(self._get_path_parts(path))
        if target_node is None:
            return {"output": f"chmod: cannot access '{path}': No such file or directory", "success": False}
        
        return {"output": "", "success": True, "message": f"Permissions of '{path}' changed to '{mode}' (simulated)."}

    def _handle_mv(self, args: List[str]) -> Dict[str, Any]:
        if len(args) < 2:
            return {"output": "mv: missing file operand", "success": False}
        if len(args) < 3:
            return {"output": "mv: missing destination file operand after '{}'".format(args[0]), "success": False}
        
        source_path = args[0]
        dest_path = args[1]

        # Simple simulation: Check if source exists and dest parent is dir
        source_parts = self._get_path_parts(source_path)
        dest_parts = self._get_path_parts(dest_path)

        source_parent_node = self._traverse_path(source_parts[:-1])
        source_node = self._traverse_path(source_parts)
        
        if source_node is None or not isinstance(source_parent_node, dict):
            return {"output": f"mv: cannot stat '{source_path}': No such file or directory", "success": False}

        dest_parent_node = self._traverse_path(dest_parts[:-1])
        new_name = dest_parts[-1]

        if not isinstance(dest_parent_node, dict):
            return {"output": f"mv: cannot move to '{dest_path}': Not a directory or path does not exist", "success": False}

        # Simulate move by deleting from source and adding to dest
        source_parent_node.pop(source_parts[-1])
        dest_parent_node[new_name] = source_node

        return {"output": "", "success": True, "message": f"Moved '{source_path}' to '{dest_path}' (simulated)."}

    def _handle_cp(self, args: List[str]) -> Dict[str, Any]:
        if len(args) < 2:
            return {"output": "cp: missing file operand", "success": False}
        if len(args) < 3:
            return {"output": "cp: missing destination file operand after '{}'".format(args[0]), "success": False}
        
        source_path = args[0]
        dest_path = args[1]

        # Simple simulation: Check if source exists and dest parent is dir
        source_node = self._traverse_path(self._get_path_parts(source_path))
        if source_node is None:
            return {"output": f"cp: cannot stat '{source_path}': No such file or directory", "success": False}

        dest_parts = self._get_path_parts(dest_path)
        dest_parent_node = self._traverse_path(dest_parts[:-1])
        new_name = dest_parts[-1]
        
        if not isinstance(dest_parent_node, dict):
            return {"output": f"cp: cannot create '{dest_path}': Not a directory or path does not exist", "success": False}

        # Simulate copy by adding to dest (deep copy if nested dicts)
        import copy
        dest_parent_node[new_name] = copy.deepcopy(source_node) # Deep copy for nested structures

        return {"output": "", "success": True, "message": f"Copied '{source_path}' to '{dest_path}' (simulated)."}


    def _handle_systemctl(self, args: List[str]) -> Dict[str, Any]:
        if len(args) < 2:
            return {"output": "systemctl: missing verb or unit", "success": False}
        
        verb = args[0].lower()
        unit = args[1].lower()

        if verb == "restart":
            # Check for specific services we know about
            if unit == "apache2":
                # Check if apache2 is stopped (simulated issue)
                if self.game_state.processes.get(1234, {}).get('state') == 'stopped':
                    self.game_state.update_process_state(1234, 'running')
                    return {"output": "apache2.service restarted successfully.", "success": True, "state_changes": [{"type": "process_state", "pid": 1234, "new_state": "running"}]}
                else:
                    return {"output": "apache2.service is already running or not in a stopped state.", "success": True} # Still a success if it's running
            else:
                return {"output": f"systemctl: Unit {unit}.service not found or not supported in simulation.", "success": False}
        elif verb == "status":
            if unit == "apache2":
                status = self.game_state.processes.get(1234, {}).get('state', 'unknown')
                if status == 'running':
                    return {"output": "● apache2.service - The Apache HTTP Server\n     Loaded: loaded (/lib/systemd/system/apache2.service; enabled; vendor preset: enabled)\n     Active: active (running) since Thu 2024-05-23 10:00:00 UTC; 10min ago\n   Main PID: 1234 (apache2)\n      Tasks: 6 (limit: 4579)\n     Memory: 16.0M\n        CPU: 1.250s\n     CGroup: /system.slice/apache2.service\n             ├─1234 /usr/sbin/apache2 -k start", "success": True}
                elif status == 'stopped':
                    return {"output": "● apache2.service - The Apache HTTP Server\n     Loaded: loaded (/lib/systemd/system/apache2.service; enabled; vendor preset: enabled)\n     Active: inactive (dead) since Thu 2024-05-23 10:05:13 UTC; 5min ago\n       Docs: https://httpd.apache.org/docs/2.4/\n    Process: 1234 ExecStart=/usr/sbin/apache2 -k start (code=exited, status=1/FAILURE)\n   Main PID: 1234 (code=exited, status=1/FAILURE)\n      Tasks: 0 (limit: 4579)\n     Memory: 0B\n        CPU: 0\n     CGroup: /system.slice/apache2.service", "success": True}
                else:
                    return {"output": f"systemctl: Unit {unit}.service status is {status}.", "success": True}
            else:
                return {"output": f"systemctl: Unit {unit}.service not found or not supported in simulation.", "success": False}
        # Add more systemctl verbs (start, stop, enable, disable, etc.) as needed
        return {"output": f"systemctl: Unsupported verb '{verb}' or unit '{unit}'.", "success": False}

    def _handle_docker(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return {"output": "docker: missing command", "success": False}
        
        subcommand = args[0].lower()

        if subcommand == "ps":
            output_lines = ["CONTAINER ID   IMAGE           COMMAND         CREATED         STATUS          PORTS               NAMES"]
            for cid, data in self.game_state.docker_containers.items():
                status_color = "green" if data['status'] == 'running' else "red"
                output_lines.append(f"{cid[:12]}   {data['image']:<15} \"nginx -g 'dae...\"   2 days ago      [{status_color}]{data['status']}[/]       {data['ports']:<19} {data['name']}")
            return {"output": "\n".join(output_lines), "success": True}
        elif subcommand == "start":
            if len(args) < 2:
                return {"output": "docker start: missing operand", "success": False}
            container_name_or_id = args[1]
            for cid, data in self.game_state.docker_containers.items():
                if data['name'] == container_name_or_id or cid.startswith(container_name_or_id):
                    if self.game_state.update_docker_container_status(cid, 'running'):
                        return {"output": container_name_or_id, "success": True, "message": f"Container {container_name_or_id} started."}
            return {"output": f"Error: No such container: {container_name_or_id}", "success": False}
        elif subcommand == "stop":
            if len(args) < 2:
                return {"output": "docker stop: missing operand", "success": False}
            container_name_or_id = args[1]
            for cid, data in self.game_state.docker_containers.items():
                if data['name'] == container_name_or_id or cid.startswith(container_name_or_id):
                    if self.game_state.update_docker_container_status(cid, 'exited'):
                        return {"output": container_name_or_id, "success": True, "message": f"Container {container_name_or_id} stopped."}
            return {"output": f"Error: No such container: {container_name_or_id}", "success": False}
        elif subcommand == "logs":
            if len(args) < 2:
                return {"output": "docker logs: missing operand", "success": False}
            container_name_or_id = args[1]
            if container_name_or_id == "db_service":
                return {"output": "[2024-05-23 10:00:00] DB_SERVICE: Starting up...\n[2024-05-23 10:00:05] DB_SERVICE: Connection successful.", "success": True}
            elif container_name_or_id == "web_app_prod":
                 return {"output": "[2024-05-23 10:00:00] NGINX: Worker process started.\n[2024-05-23 10:00:01] NGINX: Exiting due to configuration error.", "success": True}
            return {"output": f"Error: No logs found for container: {container_name_or_id}", "success": False}
        # Add more docker subcommands (exec, rm, rmi, build, run) as needed
        return {"output": f"docker: '{subcommand}' is not a docker command. See 'docker --help'.", "success": False}

    def _handle_kubectl(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return {"output": "kubectl: missing command", "success": False}
        
        subcommand = args[0].lower()

        if subcommand == "get":
            if len(args) < 2:
                return {"output": "kubectl get: missing resource type", "success": False}
            resource_type = args[1].lower()
            
            if resource_type == "pods":
                output_lines = ["NAME                             READY   STATUS    RESTARTS   AGE"]
                for pod_name, data in self.game_state.kubernetes_pods.items():
                    status_color = "green" if data['status'] == 'Running' else "yellow" if data['status'] == 'Pending' else "red"
                    output_lines.append(f"{pod_name:<32}1/1     [{status_color}]{data['status']}[/]   0          2h")
                return {"output": "\n".join(output_lines), "success": True}
            elif resource_type == "deployments":
                output_lines = ["NAME         READY   UP-TO-DATE   AVAILABLE   AGE"]
                for dep_name, data in self.game_state.kubernetes_deployments.items():
                    output_lines.append(f"{dep_name:<11}{data['replicas']}/{data['replicas']}     {data['replicas']}            {data['replicas']}           2d")
                return {"output": "\n".join(output_lines), "success": True}
            # Add more 'kubectl get' resource types
            return {"output": f"kubectl get: unsupported resource type: {resource_type}", "success": False}

        elif subcommand == "describe":
            if len(args) < 3:
                return {"output": "kubectl describe: missing resource type or name", "success": False}
            resource_type = args[1].lower()
            resource_name = args[2]

            if resource_type == "pod":
                if resource_name == "backend-efgh-67890": # Specific pending pod
                    return {"output": "Name:         backend-efgh-67890\nNamespace:    default\nStatus:       Pending\nEvents:\n  Type     Reason            Age    From               Message\n  ----     ------            ----   ----               -------\n  Warning  FailedScheduling  5m     default-scheduler  0/1 nodes are available: 1 Insufficient cpu.", "success": True}
                elif resource_name in self.game_state.kubernetes_pods:
                    pod_data = self.game_state.kubernetes_pods[resource_name]
                    return {"output": f"Name:         {resource_name}\nNamespace:    {pod_data['namespace']}\nStatus:       {pod_data['status']}\nIP:           10.42.0.1\nEvents:\n  Type     Reason            Age    From               Message\n  ----     ------            ----   ----               -------\n  Normal   Pulled            2m     kubelet            Container image \"nginx\" already present on machine", "success": True}
                return {"output": f"Error from server (NotFound): pods \"{resource_name}\" not found", "success": False}
            # Add more 'kubectl describe' resource types
            return {"output": f"kubectl describe: unsupported resource type: {resource_type}", "success": False}
        
        elif subcommand == "scale":
            if len(args) < 4 or args[1].lower() != "deployment" or "--replicas=" not in args[3]:
                return {"output": "kubectl scale: invalid syntax. Use 'kubectl scale deployment <name> --replicas=<count>'", "success": False}
            
            deployment_name = args[2]
            try:
                replicas = int(args[3].split('=')[1])
            except ValueError:
                return {"output": "kubectl scale: invalid replicas count", "success": False}

            if self.game_state.scale_kubernetes_deployment(deployment_name, replicas):
                # Update pod status if scaling a pending deployment
                if deployment_name == "backend" and replicas > 0:
                    self.game_state.update_kubernetes_pod_status("backend-efgh-67890", "Running")

                return {"output": f"deployment.apps/{deployment_name} scaled", "success": True, "message": f"Deployment '{deployment_name}' scaled to {replicas} replicas.",
                        "state_changes": [{"type": "k8s_scale_deployment", "deployment_name": deployment_name, "replicas": replicas}]}
            else:
                return {"output": f"Error: deployment.apps/{deployment_name} not found or failed to scale.", "success": False}

        # Add more kubectl subcommands (delete, apply, logs) as needed
        return {"output": f"kubectl: '{subcommand}' is not a kubectl command. See 'kubectl --help'.", "success": False}