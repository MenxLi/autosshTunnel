import os, json, sys, datetime, argparse
from typing import Tuple, List, Union, TypedDict
import subprocess

HOME_DIR = os.getenv("HOME")
if HOME_DIR is None:
    raise ValueError("Check $HOME has been set.")

CONF_FNAME = ".connectPorts_conf.json"
CONF_INSTALL_DIR = "/etc"

CMD_LOG_FNAME = "_CONN_PORTS_CMD.log"
CMD_LOG_PATH = os.path.join(HOME_DIR, CMD_LOG_FNAME)
LOG_FNAME = "_CONN_PORTS_LOG.log"
LOG_PATH = os.path.join(HOME_DIR, LOG_FNAME)
# CURR_DIR = os.path.dirname(__file__)
LOCAL_HOST = "127.0.0.1"
#  LOCAL_HOST = "localhost"

class PortMapType(TypedDict):
    local_port: str
    remote_port: str
    monitor_port: str
    Description: str

def _connectPort(user: str, server_addr: str, local_port: str, remote_port: str, monitor_port: str) -> str:
    log_path = os.path.join(HOME_DIR, LOG_FNAME)
    if not os.path.exists(log_path):
        os.system(f"touch {log_path}")
        print("Created log file at: ", log_path)
    cmd = f"autossh -M {monitor_port} -NR {remote_port}:{LOCAL_HOST}:{local_port} {user}@{server_addr}"
    with open(log_path, "a") as fp:
        fp.write(datetime.datetime.now().strftime("%Y-%m-%d"))
        fp.write(f"\n{local_port}->{server_addr}:{remote_port}({monitor_port})\n")
        proc = subprocess.Popen(cmd, shell = True, stderr=subprocess.STDOUT, stdout=fp)
    print(f"Started connection: {LOCAL_HOST}:{local_port}->{server_addr}:{remote_port}(monitor: {monitor_port})")
    return cmd

def _getServerUserAddrAndPorts() -> Tuple[str, str, List[PortMapType]]:
    LOCAL_CONF = os.path.join(HOME_DIR, CONF_FNAME)
    GLOBAL_CONF = os.path.join(CONF_INSTALL_DIR, CONF_FNAME)
    if os.path.exists(LOCAL_CONF):
        with open(LOCAL_CONF, "r") as fp:
            conf = json.load(fp)
    elif os.path.exists(GLOBAL_CONF):
        with open(GLOBAL_CONF, "r") as fp:
            conf = json.load(fp)
    else:
        raise Exception(f"{CONF_FNAME} not exist in either {CONF_INSTALL_DIR} or {HOME_DIR}")
    server = conf["interm_server"]
    server_addr = server["addr"]
    server_user = server["user"]
    port_maps = server["port_map"]
    # set default values
    for i in range(len(port_maps)):
        _map = port_maps[i]
        if not "description" in _map:
            _map["description"] = ""
        if not "monitor_port" in _map:
            _map["monitor_port"] = "0"
    return server_user, server_addr, port_maps

def _getPname(id) -> Union[str, None]:
    if os.path.exists(f"/proc/{id}"):
        with open(f"/proc/{id}/cmdline", "r") as fp:
            name = fp.read()
        return name
    else:
        return None

def _getpidByNameStart(name: str) -> List[str]:
    pids = []
    for pid in os.listdir("/proc"):
        comm_path = os.path.join("/proc", pid, "comm") 
        if os.path.exists(comm_path):
            with open(comm_path, "r") as fp:
                pname = fp.read()
            if pname.startswith(name):
                pids.append(pid)
    return pids

def _killPid(pid) -> bool:
    cmd = 'kill ' + str(pid)
    try:
        os.system(cmd)
        # print(pid, 'killed')
        return True
    except Exception as e:
        print(e)
        return False

def start():
    log_path = os.path.join(HOME_DIR, LOG_FNAME)
    cmd_log_path = os.path.join(HOME_DIR, CMD_LOG_FNAME)

    if os.path.exists(log_path):
        os.remove(log_path)
    user, addr, port_maps = _getServerUserAddrAndPorts()
    cmds = []
    for port_map in port_maps:
        local_port = port_map["local_port"]
        remote_port = port_map["remote_port"]
        monitor_port = port_map["monitor_port"]
        cmd = _connectPort(user, addr, local_port, remote_port, monitor_port)
        cmds.append(cmd)

    with open(cmd_log_path, "w") as fp:
        fp.write("\n".join(cmds))
    return

def stop() -> bool:
    cmd_log_path = os.path.join(HOME_DIR, CMD_LOG_FNAME)
    pids = _getpidByNameStart("autossh")
    valid_pids = []
    KILL_ALL = True
    if os.path.exists(cmd_log_path):
        with open(cmd_log_path, "r") as fp:
            valid_cmds = fp.read().split("\n")
    else:
        return False

    for _pid in pids:
        cmd = subprocess.check_output(["ps","-p", _pid, "-o", "args"])
        cmd = cmd.decode("ascii")
        for v_cmd in valid_cmds:
            if cmd.replace("\n", "").endswith(v_cmd):
                valid_pids.append(_pid)
    if len(valid_cmds) != len(valid_pids):
        print(f"Did not find all pids (find: {valid_pids}/{valid_cmds})")
        KILL_ALL = False

    for pid in valid_pids:
        pname = _getPname(pid)
        if pname is None:
            print(f"pid:{pid} not exists")
            KILL_ALL = False
        elif _killPid(pid):
            print("Stop pid: ", pid)
        else:
            print("Can't stop pid", pid)
            KILL_ALL = False

    if KILL_ALL:
        os.remove(cmd_log_path)
        print("Removed: ", cmd_log_path)
    else:
        print(f"Commend log file not remove, maybe some process were still running.")
        print(f"Check {cmd_log_path} for commends that were started.")
    return KILL_ALL


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Control autossh tunnels.")
    parser.add_argument("cmd", nargs = "?", type = str, default = "show", 
                        choices = ["start", "stop", "restart", "show"])

    args = parser.parse_args()
    if args.cmd == "start":
        start()
    if args.cmd == "stop":
        stop()
    if args.cmd == "restart":
        stop()
        start()
    if args.cmd == "show":
        if os.path.exists(CMD_LOG_PATH):
            print("Running CMDs:")
            with open(CMD_LOG_PATH, "r") as fp:
                running_cmd = fp.read()
                print(running_cmd)
        else:
            print("Not started.")
        print("for usage: -h/--help")
