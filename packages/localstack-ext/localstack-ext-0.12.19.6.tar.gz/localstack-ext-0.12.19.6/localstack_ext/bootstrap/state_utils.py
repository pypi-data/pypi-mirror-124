import logging
KOXdA=bool
KOXdU=hasattr
KOXdW=set
KOXdp=True
KOXdo=False
KOXdE=isinstance
KOXdb=dict
KOXdw=getattr
KOXdt=None
KOXdL=str
KOXdB=Exception
KOXdJ=open
import os
from typing import Any,Callable,List,OrderedDict,Set,Tuple
from localstack.utils.common import ObjectIdHashComparator
LOG=logging.getLogger(__name__)
def check_already_visited(obj,visited:Set)->Tuple[KOXdA,Set]:
 if KOXdU(obj,"__dict__"):
  visited=visited or KOXdW()
  wrapper=ObjectIdHashComparator(obj)
  if wrapper in visited:
   return KOXdp,visited
  visited.add(wrapper)
 return KOXdo,visited
def get_object_dict(obj):
 if KOXdE(obj,KOXdb):
  return obj
 obj_dict=KOXdw(obj,"__dict__",KOXdt)
 return obj_dict
def is_composite_type(obj):
 return KOXdE(obj,(KOXdb,OrderedDict))or KOXdU(obj,"__dict__")
def api_states_traverse(api_states_path:KOXdL,side_effect:Callable[...,KOXdt],mutables:List[Any]):
 for dir_name,_,file_list in os.walk(api_states_path):
  for file_name in file_list:
   try:
    subdirs=os.path.normpath(dir_name).split(os.sep)
    region=subdirs[-1]
    service_name=subdirs[-2]
    side_effect(dir_name=dir_name,fname=file_name,region=region,service_name=service_name,mutables=mutables)
   except KOXdB as e:
    LOG.warning(f"Failed to apply {side_effect.__name__} for {file_name} in dir {dir_name}: {e}")
    continue
def load_persisted_object(state_file):
 if not os.path.isfile(state_file):
  return
 import dill
 with KOXdJ(state_file,"rb")as f:
  try:
   content=f.read()
   result=dill.loads(content)
   return result
  except KOXdB as e:
   LOG.debug("Unable to read pickled persistence file %s: %s"%(state_file,e))
# Created by pyminifier (https://github.com/liftoff/pyminifier)
