from typing import Set
gjMdz=str
gjMdY=int
gjMdO=super
gjMde=False
gjMdH=isinstance
gjMdp=hash
gjMdm=True
gjMdG=list
gjMdb=map
gjMds=None
from localstack_ext.bootstrap.cpvcs.constants import(COMMIT_TXT_LAYOUT,REV_TXT_LAYOUT,STATE_TXT_LAYOUT,STATE_TXT_METADATA,VER_TXT_LAYOUT)
class CPVCSObj:
 def __init__(self,hash_ref:gjMdz):
  self.hash_ref:gjMdz=hash_ref
class StateFileRef(CPVCSObj):
 txt_layout=STATE_TXT_LAYOUT
 metadata_layout=STATE_TXT_METADATA
 def __init__(self,hash_ref:gjMdz,rel_path:gjMdz,file_name:gjMdz,size:gjMdY,service:gjMdz,region:gjMdz):
  gjMdO().__init__(hash_ref)
  self.rel_path:gjMdz=rel_path
  self.file_name:gjMdz=file_name
  self.size:gjMdY=size
  self.service:gjMdz=service
  self.region:gjMdz=region
 def __str__(self):
  return self.txt_layout.format(size=self.size,service=self.service,region=self.region,gjMdp=self.hash_ref,file_name=self.file_name,rel_path=self.rel_path)
 def __eq__(self,other):
  if not other:
   return gjMde
  if not gjMdH(other,StateFileRef):
   return gjMde
  return(self.hash_ref==other.hash_ref and self.region==other.region and self.service==self.service and self.file_name==other.file_name and self.size==other.size)
 def __hash__(self):
  return gjMdp((self.hash_ref,self.region,self.service,self.file_name,self.size))
 def congruent(self,other):
  if not other:
   return gjMde
  if not gjMdH(other,StateFileRef):
   return gjMde
  return(self.region==other.region and self.service==other.service and self.file_name==other.file_name and self.rel_path==other.rel_path)
 def any_congruence(self,others):
  for other in others:
   if self.congruent(other):
    return gjMdm
  return gjMde
 def metadata(self)->gjMdz:
  return self.metadata_layout.format(size=self.size,service=self.service,region=self.region)
class CPVCSNode(CPVCSObj):
 def __init__(self,hash_ref:gjMdz,state_files:Set[StateFileRef],parent_ptr:gjMdz):
  gjMdO().__init__(hash_ref)
  self.state_files:Set[StateFileRef]=state_files
  self.parent_ptr:gjMdz=parent_ptr
 def state_files_info(self)->gjMdz:
  return "\n".join(gjMdG(gjMdb(lambda state_file:gjMdz(state_file),self.state_files)))
class Commit:
 txt_layout=COMMIT_TXT_LAYOUT
 def __init__(self,tail_ptr:gjMdz,head_ptr:gjMdz,delta_log_ptr:gjMdz=gjMds):
  self.tail_ptr:gjMdz=tail_ptr
  self.head_ptr:gjMdz=head_ptr
  self.delta_log_ptr:gjMdz=delta_log_ptr
 def __str__(self):
  return self.txt_layout.format(tail_ptr=self.tail_ptr,head_ptr=self.head_ptr,log_hash=self.delta_log_ptr)
class Revision(CPVCSNode):
 txt_layout=REV_TXT_LAYOUT
 def __init__(self,hash_ref:gjMdz,state_files:Set[StateFileRef],parent_ptr:gjMdz,creator:gjMdz,rid:gjMdz,revision_number:gjMdY,assoc_commit:Commit=gjMds):
  gjMdO().__init__(hash_ref,state_files,parent_ptr)
  self.creator:gjMdz=creator
  self.rid:gjMdz=rid
  self.revision_number:gjMdY=revision_number
  self.assoc_commit=assoc_commit
 def __str__(self):
  return self.txt_layout.format(gjMdp=self.hash_ref,parent=self.parent_ptr,creator=self.creator,rid=self.rid,rev_no=self.revision_number,state_files=";".join(gjMdb(lambda state_file:gjMdz(state_file),self.state_files))if self.state_files else "",assoc_commit=gjMdz(self.assoc_commit))
class Version(CPVCSNode):
 txt_layout=VER_TXT_LAYOUT
 def __init__(self,hash_ref:gjMdz,state_files:Set[StateFileRef],parent_ptr:gjMdz,creator:gjMdz,comment:gjMdz,active_revision_ptr:gjMdz,outgoing_revision_ptrs:Set[gjMdz],incoming_revision_ptr:gjMdz,version_number:gjMdY):
  gjMdO().__init__(hash_ref,state_files,parent_ptr)
  self.creator=creator
  self.comment=comment
  self.active_revision_ptr=active_revision_ptr
  self.outgoing_revision_ptrs=outgoing_revision_ptrs
  self.incoming_revision_ptr=incoming_revision_ptr
  self.version_number=version_number
 def __str__(self):
  return VER_TXT_LAYOUT.format(gjMdp=self.hash_ref,parent=self.parent_ptr,creator=self.creator,comment=self.comment,version_number=self.version_number,active_revision=self.active_revision_ptr,outgoing_revisions=";".join(self.outgoing_revision_ptrs),incoming_revision=self.incoming_revision_ptr,state_files=";".join(gjMdb(lambda stat_file:gjMdz(stat_file),self.state_files))if self.state_files else "")
 def info_str(self):
  return f"{self.version_number}, {self.creator}, {self.comment}"
# Created by pyminifier (https://github.com/liftoff/pyminifier)
