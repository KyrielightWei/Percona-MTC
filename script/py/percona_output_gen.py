'''
@Author: wei
@Date: 2020-06-23 19:04:40
@LastEditors: Do not edit
@LastEditTime: 2020-06-29 22:04:45
@Description: file content
@FilePath: /Percona-Share-Storage/script/py/percona_output_gen.py
'''

import os
import sys
from configparser import ConfigParser
import subprocess

# @param config_path
config_path = "./config.ini" # sys.argv[1]


cfg = ConfigParser()
cfg.read(config_path)

build_path = cfg.get("build_env","build_dir")
out_dir = cfg.get("build_env","out_dir")
port = int(cfg.get("build_env","port"))
xcom_port = int(cfg.get("build_env","xcom_port"))
#user = cfg.get("build","user")
mysqld_path=build_path+"/bin/mysqld"

node_count = int(cfg.get("run_env","node_count")) #sys.argv[2]
group_name = cfg.get("run_env","group_name")#"mmlp_group"
local_ip = cfg.get("run_env","local_ip")#"10.11.6.120"
remote_peer_nodes = cfg.get("run_env","remote_peer_nodes")

if(remote_peer_nodes == ""):
    peer_nodes_str = ""
else:
    peer_nodes_str = remote_peer_nodes + ","

for j in range(0,node_count):
    peer_nodes_str = peer_nodes_str + local_ip + ":" + str(xcom_port+j)
    if(j < node_count - 1 and node_count > 1):
        peer_nodes_str += ","

print("Peer_Node_String = " + peer_nodes_str)

if(os.path.exists(out_dir) == False):
    os.mkdir(out_dir)

for i in range(0,node_count):
    out_dir_i = out_dir + "/percona_" + str(port+i)
    if(os.path.exists(out_dir_i) == False):
        os.mkdir(out_dir_i)
    config_i = out_dir+"/percona_" + str(port+i) + ".conf"
    if(os.path.exists(config_i) == False):
        #print("create mysql config file")
        mysql_config_i = ConfigParser()
        mysql_config_i["client"] = {
            "port":str(port+i),
            "socket":out_dir_i + "/data/percona.sock",
            "user" : "root",
            "password": "123"
        }
        # peer_nodes_str_i = peer_nodes_str.replace(local_ip+":"+str(xcom_port+i)+",","")
        # peer_nodes_str_i = peer_nodes_str_i.rstrip(",")
        #print(peer_nodes_str_i)
        mysql_config_i["mysqld"] = {
            "port":str(port+i),
            "socket":out_dir_i + "/data/percona.sock",
            "basedir": build_path,
            "datadir": out_dir_i + "/data/",
            "log-error": out_dir_i + "/percona_error.log",
            "pid-file" : out_dir_i + "/data/percona.pid",
            "multi_master_log_plugin_group_name": group_name,
            "multi_master_log_plugin_local_node": local_ip + ":" + str(xcom_port+i),
            "multi_master_log_plugin_peer_nodes": peer_nodes_str,
            "innodb_buffer_pool_size":"69793218560",
            "symbolic-links":"0",
            "innodb_thread_concurrency":"0",
            "thread_cache_size":"4096",
            "general_log":"0",
            "max_connections":"4096",
            "table_open_cache":"8192",
            "max_connect_errors":"200000",
            "innodb_read_io_threads":"16",
            "innodb_write_io_threads":"16",
            "innodb_table_locks":"OFF",
            "innodb_thread_sleep_delay":"0",
            "innodb_flush_method":"O_DIRECT",
            "innodb_flush_log_at_trx_commit":"0"
        }
        with open(config_i,'w') as configfile:
            mysql_config_i.write(configfile)
        a,b = subprocess.getstatusoutput(mysqld_path + " --defaults-file="+config_i + "  --initialize --multi_master_log_plugin=OFF")
        print("result["+str(i)+"] = " + str(a))
        print(b)
