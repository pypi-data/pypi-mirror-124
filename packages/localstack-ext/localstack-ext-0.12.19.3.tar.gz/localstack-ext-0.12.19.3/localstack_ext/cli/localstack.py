import logging
SfqJv=True
SfqJm=False
SfqJH=None
SfqJo=Exception
SfqJa=open
SfqJd=bool
SfqJP=str
SfqJi=int
SfqJI=dict
SfqJT=list
SfqJl=isinstance
SfqJx=super
import os
import sys
from typing import Any,Callable,Dict,List
import click
from localstack.cli import LocalstackCli,LocalstackCliPlugin,console
class ProCliPlugin(LocalstackCliPlugin):
 name="pro"
 def should_load(self):
  e=os.getenv("LOCALSTACK_API_KEY")
  return SfqJv if e else SfqJm
 def is_active(self):
  return self.should_load()
 def attach(self,cli:LocalstackCli)->SfqJH:
  group:click.Group=cli.group
  group.add_command(cmd_login)
  group.add_command(cmd_logout)
  group.add_command(daemons)
  group.add_command(pod)
  group.add_command(dns)
  group.add_command(cpvcs)
@click.group(name="daemons",help="Manage local daemon processes")
def daemons():
 pass
@click.command(name="login",help="Log in with your account credentials")
@click.option("--username",help="Username for login")
@click.option("--provider",default="internal",help="OAuth provider (default: localstack internal login)")
def cmd_login(username,provider):
 from localstack_ext.bootstrap import auth
 try:
  auth.login(provider,username)
  console.print("successfully logged in")
 except SfqJo as e:
  console.print("authentication error: %s"%e)
@click.command(name="logout",help="Log out and delete any session tokens")
def cmd_logout():
 from localstack_ext.bootstrap import auth
 try:
  auth.logout()
  console.print("successfully logged out")
 except SfqJo as e:
  console.print("logout error: %s"%e)
@daemons.command(name="start",help="Start local daemon processes")
def cmd_daemons_start():
 from localstack_ext.bootstrap import local_daemon
 console.log("Starting local daemons processes ...")
 local_daemon.start_in_background()
@daemons.command(name="stop",help="Stop local daemon processes")
def cmd_daemons_stop():
 from localstack_ext.bootstrap import local_daemon
 console.log("Stopping local daemons processes ...")
 local_daemon.kill_servers()
@daemons.command(name="log",help="Show log of daemon process")
def cmd_daemons_log():
 from localstack_ext.bootstrap import local_daemon
 file_path=local_daemon.get_log_file_path()
 if not os.path.isfile(file_path):
  console.print("no log found")
 else:
  with SfqJa(file_path,"r")as fd:
   for line in fd:
    sys.stdout.write(line)
    sys.stdout.flush()
@click.group(name="dns",help="Manage DNS settings of your host")
def dns():
 pass
@dns.command(name="systemd-resolved",help="Manage DNS settings of systemd-resolved (Ubuntu, Debian etc.)")
@click.option("--revert",is_flag=SfqJv,help="Revert systemd-resolved settings for the docker interface")
def cmd_dns_systemd(revert:SfqJd):
 import localstack_ext.services.dns_server
 from localstack_ext.bootstrap.dns_utils import configure_systemd
 console.print("Configuring systemd-resolved...")
 logger_name=localstack_ext.services.dns_server.LOG.name
 localstack_ext.services.dns_server.LOG=ConsoleLogger(logger_name)
 configure_systemd(revert)
def _cpvcs_initialized()->SfqJd:
 from localstack_ext.bootstrap.cpvcs.utils.common import config_context
 if not config_context.is_initialized():
  console.print("[red]Error:[/red] Could not find local CPVCS instance")
  return SfqJm
 return SfqJv
@click.group(name="cpvcs",help="Experimental Cloud Pods with elaborate versioning mechanism")
def cpvcs():
 pass
@cpvcs.command(name="init",help="Creates a new cloud pod with cpvcs enabled")
def cmd_cpvcs_init():
 from localstack_ext.bootstrap import pods_client
 from localstack_ext.bootstrap.cpvcs.utils.common import config_context
 if config_context.is_initialized():
  console.print(f"[red]Error:[/red] CPVCS already instanciated for pod at {config_context.get_cpvcs_root_dir()}")
 else:
  pods_client.init_cpvcs(pod_name="",pre_config={"backend":"cpvcs"})
  console.print("Successfully created local CPVCS instance!")
@cpvcs.command(name="commit",help="Commits the current expansion point and creates a new (empty) revision")
def cmd_cpvcs_commit():
 from localstack_ext.bootstrap import pods_client
 if _cpvcs_initialized():
  pods_client.commit_state(pod_name="",pre_config={"backend":"cpvcs"})
  console.print("Successfully commited the current state")
@cpvcs.command(name="push",help="Creates a new version by using the state files in the current expansion point (latest commit)")
@click.option("--squash",is_flag=SfqJv,help="Squashes commits together, so only the latest commit is stored in the revision graph")
@click.option("--comment",help="Add a comment describing the version")
def cmd_cpvcs_push(squash:SfqJd,comment:SfqJP):
 from localstack_ext.bootstrap import pods_client
 if _cpvcs_initialized():
  pods_client.push_state(pod_name="",pre_config={"backend":"cpvcs"},squash_commits=squash,comment=comment)
  console.print("Successfully pushed the current state")
@cpvcs.command(name="inject",help="Injects the state from a version into the application runtime")
@click.option("--version",default="-1",type=SfqJi,help="Loads the state of the specified version - Most recent one by default")
@click.option("--reset",is_flag=SfqJv,default=SfqJm,help="Will reset the application state before injecting")
def cmd_cpvcs_inject(version:SfqJi,reset:SfqJd):
 from localstack_ext.bootstrap import pods_client
 if _cpvcs_initialized():
  pods_client.inject_state(pod_name="",version=version,reset_state=reset,pre_config={"backend":"cpvcs"})
@cpvcs.command(name="versions",help="Lists all available version numbers")
def cmd_cpvcs_versions():
 if _cpvcs_initialized():
  from localstack_ext.bootstrap import pods_client
  version_list=pods_client.list_versions(pod_name="",pre_config={"backend":"cpvcs"})
  result="\n".join(version_list)
  console.print(result)
@cpvcs.command(name="version-info")
@click.option("--version",required=SfqJv,type=SfqJi)
def cmd_cpvcs_version_info(version:SfqJi):
 if _cpvcs_initialized():
  from localstack_ext.bootstrap import pods_client
  info=pods_client.get_version_info(version=version,pod_name="",pre_config={"backend":"cpvcs"})
  console.print(info)
@cpvcs.command(name="set-version",help="Set HEAD to a specific version")
@click.option("--version",required=SfqJv,type=SfqJi,help="The version the state should be set to")
@click.option("--inject",is_flag=SfqJv,help="Whether the state should be directly injected into the application runtime after changing version")
@click.option("--reset/--no-reset",default=SfqJv,help="Whether the current application state should be reset before changing version")
@click.option("--commit-before",is_flag=SfqJv,help="Whether the current application state should be commited to the currently selected version before changing version")
def cmd_cpvcs_set_version(version:SfqJi,inject:SfqJd,reset:SfqJd,commit_before:SfqJd):
 if _cpvcs_initialized():
  from localstack_ext.bootstrap import pods_client
  pods_client.set_version(version=version,inject_version_state=inject,reset_state=reset,commit_before=commit_before,pod_name="",pre_config={"backend":"cpvcs"})
@click.group(name="pod",help="Manage state of local cloud pods")
def pod():
 from localstack_ext.bootstrap.licensing import is_logged_in
 if not is_logged_in():
  console.print("[red]Error:[/red] not logged in, please log in first")
  sys.exit(1)
@pod.command(name="list",help="Get a list of available local cloud pods")
def cmd_pod_list():
 status=console.status("Fetching list of pods from server ...")
 status.start()
 from localstack import config
 from localstack.utils.common import format_bytes
 from localstack_ext.bootstrap import pods_client
 try:
  result=pods_client.list_pods(SfqJH)
  status.stop()
  columns={"pod_name":"Name","backend":"Backend","url":"URL","size":"Size","state":"State"}
  print_table(columns,result,formatters={"size":format_bytes})
 except SfqJo as e:
  status.stop()
  if config.DEBUG:
   console.print_exception()
  else:
   console.print("[red]Error:[/red]",e)
@pod.command(name="create",help="Create a new local cloud pod")
def cmd_pod_create():
 msg="Please head over to https://app.localstack.cloud to create a new cloud pod. (CLI support is coming soon)"
 console.print(msg)
@pod.command(name="push",help="Push the state of the LocalStack instance to a cloud pod")
@click.argument("name")
def cmd_pod_push(name:SfqJP):
 from localstack_ext.bootstrap import pods_client
 pods_client.push_state(name)
@pod.command(name="pull",help="Pull the state of a cloud pod into the running LocalStack instance")
@click.argument("name")
def cmd_pod_pull(name:SfqJP):
 from localstack_ext.bootstrap import pods_client
 pods_client.pull_state(name)
@pod.command(name="reset",help="Reset the local state to get a fresh LocalStack instance")
def cmd_pod_reset():
 from localstack_ext.bootstrap import pods_client
 pods_client.reset_local_state()
def print_table(columns:Dict[SfqJP,SfqJP],rows:List[Dict[SfqJP,Any]],formatters:Dict[SfqJP,Callable[[Any],SfqJP]]=SfqJH):
 from rich.table import Table
 if formatters is SfqJH:
  formatters=SfqJI()
 t=Table()
 for k,name in columns.items():
  t.add_column(name)
 for row in rows:
  cells=SfqJT()
  for c in columns.keys():
   cell=row.get(c)
   if c in formatters:
    cell=formatters[c](cell)
   if cell is SfqJH:
    cell=""
   if not SfqJl(cell,SfqJP):
    cell=SfqJP(cell)
   cells.append(cell)
  t.add_row(*cells)
 console.print(t)
class ConsoleLogger(logging.Logger):
 def __init__(self,name):
  SfqJx(ConsoleLogger,self).__init__(name)
 def info(self,msg:Any,*args:Any,**kwargs:Any)->SfqJH:
  console.print(msg%args)
 def warning(self,msg:Any,*args:Any,**kwargs:Any)->SfqJH:
  console.print("[red]Warning:[/red] ",msg%args)
 def error(self,msg:Any,*args:Any,**kwargs:Any)->SfqJH:
  console.print("[red]Error:[/red] ",msg%args)
 def exception(self,msg:Any,*args:Any,**kwargs:Any)->SfqJH:
  console.print("[red]Error:[/red] ",msg%args)
  console.print_exception()
# Created by pyminifier (https://github.com/liftoff/pyminifier)
