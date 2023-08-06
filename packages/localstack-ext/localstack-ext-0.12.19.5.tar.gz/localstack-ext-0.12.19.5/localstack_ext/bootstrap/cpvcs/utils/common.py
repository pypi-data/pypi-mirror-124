import os
qgaTO=None
qgaTR=str
qgaTJ=int
qgaTY=open
qgaTP=bool
qgaTd=False
qgaTj=classmethod
from localstack.config import TMP_FOLDER
from localstack_ext.bootstrap.cpvcs.constants import(CPVCS_DIR,DEFAULT_POD_DIR,HEAD_FILE,KNOWN_VER_FILE,MAX_VER_FILE,OBJ_STORE_DIR,REFS_DIR,REV_SUB_DIR,VER_LOG_FILE,VER_LOG_STRUCTURE,VER_SUB_DIR)
class PodConfigContext:
 default_instance=qgaTO
 def __init__(self,pod_root_dir):
  self.pod_root_dir=pod_root_dir
 def get_cpvcs_root_dir(self)->qgaTR:
  return self.pod_root_dir
 def get_head_path(self)->qgaTR:
  return os.path.join(self.pod_root_dir,HEAD_FILE)
 def get_max_ver_path(self)->qgaTR:
  return os.path.join(self.pod_root_dir,MAX_VER_FILE)
 def get_known_ver_path(self)->qgaTR:
  return os.path.join(self.pod_root_dir,KNOWN_VER_FILE)
 def get_ver_log_path(self)->qgaTR:
  return os.path.join(self.pod_root_dir,VER_LOG_FILE)
 def get_obj_store_path(self)->qgaTR:
  return os.path.join(self.pod_root_dir,OBJ_STORE_DIR)
 def get_rev_obj_store_path(self)->qgaTR:
  return os.path.join(self.get_obj_store_path(),REV_SUB_DIR)
 def get_ver_obj_store_path(self)->qgaTR:
  return os.path.join(self.get_obj_store_path(),VER_SUB_DIR)
 def get_ver_refs_path(self)->qgaTR:
  return os.path.join(self.pod_root_dir,REFS_DIR,VER_SUB_DIR)
 def get_rev_refs_Path(self)->qgaTR:
  return os.path.join(self.pod_root_dir,REFS_DIR,REV_SUB_DIR)
 def update_ver_log(self,author:qgaTR,ver_no:qgaTJ,rev_id:qgaTR,rev_no:qgaTJ):
  with qgaTY(self.get_ver_log_path(),"a")as fp:
   fp.write(f"{VER_LOG_STRUCTURE.format(author=author, ver_no=ver_no, rev_rid_no=f'{rev_id}_{rev_no}')}\n")
 def create_version_symlink(self,name:qgaTR,key:qgaTR)->qgaTR:
  return self._create_symlink(name,key,self.get_ver_refs_path())
 def create_revision_symlink(self,name:qgaTR,key:qgaTR)->qgaTR:
  return self._create_symlink(name,key,self.get_rev_refs_Path())
 def is_initialized(self)->qgaTP:
  return self.pod_root_dir and os.path.isdir(self.pod_root_dir)
 def _create_symlink(self,name:qgaTR,key:qgaTR,path:qgaTR)->qgaTR:
  symlink=os.path.join(path,name)
  with qgaTY(symlink,"w")as fp:
   fp.write(key)
  return symlink
 def _get_head_key(self)->qgaTR:
  return self._get_key(self.get_head_path())
 def get_max_ver_key(self)->qgaTR:
  return self._get_key(self.get_max_ver_path())
 def _get_key(self,path:qgaTR)->qgaTR:
  with qgaTY(path,"r")as fp:
   key_path=fp.readline()
  with qgaTY(key_path,"r")as fp:
   key=fp.readline()
   return key
 def get_obj_file_path(self,key:qgaTR)->qgaTR:
  return os.path.join(self.get_obj_store_path(),key)
 def is_remotly_managed(self)->qgaTP:
  return qgaTd
 @qgaTj
 def get(cls):
  if not cls.default_instance:
   pod_root_dir=os.environ.get("POD_DIR")
   if not pod_root_dir:
    pod_root_dir=os.path.join(TMP_FOLDER,DEFAULT_POD_DIR)
   pod_root_dir=os.path.join(pod_root_dir,CPVCS_DIR)
   cls.default_instance=PodConfigContext(pod_root_dir)
  return cls.default_instance
config_context=PodConfigContext.get()
# Created by pyminifier (https://github.com/liftoff/pyminifier)
