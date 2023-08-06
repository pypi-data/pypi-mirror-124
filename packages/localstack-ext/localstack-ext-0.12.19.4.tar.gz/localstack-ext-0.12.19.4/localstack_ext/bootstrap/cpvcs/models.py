from typing import Set
FeXAU=str
FeXAM=int
FeXAD=super
FeXAp=False
FeXAr=isinstance
FeXAh=hash
FeXAc=True
FeXAJ=list
FeXAg=map
FeXAz=None
from localstack_ext.bootstrap.cpvcs.constants import(COMMIT_TXT_LAYOUT,REV_TXT_LAYOUT,STATE_TXT_LAYOUT,STATE_TXT_METADATA,VER_TXT_LAYOUT)
class CPVCSObj:
 def __init__(self,hash_ref:FeXAU):
  self.hash_ref:FeXAU=hash_ref
class StateFileRef(CPVCSObj):
 txt_layout=STATE_TXT_LAYOUT
 metadata_layout=STATE_TXT_METADATA
 def __init__(self,hash_ref:FeXAU,rel_path:FeXAU,file_name:FeXAU,size:FeXAM,service:FeXAU,region:FeXAU):
  FeXAD().__init__(hash_ref)
  self.rel_path:FeXAU=rel_path
  self.file_name:FeXAU=file_name
  self.size:FeXAM=size
  self.service:FeXAU=service
  self.region:FeXAU=region
 def __str__(self):
  return self.txt_layout.format(size=self.size,service=self.service,region=self.region,FeXAh=self.hash_ref,file_name=self.file_name,rel_path=self.rel_path)
 def __eq__(self,other):
  if not other:
   return FeXAp
  if not FeXAr(other,StateFileRef):
   return FeXAp
  return(self.hash_ref==other.hash_ref and self.region==other.region and self.service==self.service and self.file_name==other.file_name and self.size==other.size)
 def __hash__(self):
  return FeXAh((self.hash_ref,self.region,self.service,self.file_name,self.size))
 def congruent(self,other):
  if not other:
   return FeXAp
  if not FeXAr(other,StateFileRef):
   return FeXAp
  return(self.region==other.region and self.service==other.service and self.file_name==other.file_name and self.rel_path==other.rel_path)
 def any_congruence(self,others):
  for other in others:
   if self.congruent(other):
    return FeXAc
  return FeXAp
 def metadata(self)->FeXAU:
  return self.metadata_layout.format(size=self.size,service=self.service,region=self.region)
class CPVCSNode(CPVCSObj):
 def __init__(self,hash_ref:FeXAU,state_files:Set[StateFileRef],parent_ptr:FeXAU):
  FeXAD().__init__(hash_ref)
  self.state_files:Set[StateFileRef]=state_files
  self.parent_ptr:FeXAU=parent_ptr
 def state_files_info(self)->FeXAU:
  return "\n".join(FeXAJ(FeXAg(lambda state_file:FeXAU(state_file),self.state_files)))
class Commit:
 txt_layout=COMMIT_TXT_LAYOUT
 def __init__(self,tail_ptr:FeXAU,head_ptr:FeXAU,delta_log_ptr:FeXAU=FeXAz):
  self.tail_ptr:FeXAU=tail_ptr
  self.head_ptr:FeXAU=head_ptr
  self.delta_log_ptr:FeXAU=delta_log_ptr
 def __str__(self):
  return self.txt_layout.format(tail_ptr=self.tail_ptr,head_ptr=self.head_ptr,log_hash=self.delta_log_ptr)
class Revision(CPVCSNode):
 txt_layout=REV_TXT_LAYOUT
 def __init__(self,hash_ref:FeXAU,state_files:Set[StateFileRef],parent_ptr:FeXAU,creator:FeXAU,rid:FeXAU,revision_number:FeXAM,assoc_commit:Commit=FeXAz):
  FeXAD().__init__(hash_ref,state_files,parent_ptr)
  self.creator:FeXAU=creator
  self.rid:FeXAU=rid
  self.revision_number:FeXAM=revision_number
  self.assoc_commit=assoc_commit
 def __str__(self):
  return self.txt_layout.format(FeXAh=self.hash_ref,parent=self.parent_ptr,creator=self.creator,rid=self.rid,rev_no=self.revision_number,state_files=";".join(FeXAg(lambda state_file:FeXAU(state_file),self.state_files))if self.state_files else "",assoc_commit=FeXAU(self.assoc_commit))
class Version(CPVCSNode):
 txt_layout=VER_TXT_LAYOUT
 def __init__(self,hash_ref:FeXAU,state_files:Set[StateFileRef],parent_ptr:FeXAU,creator:FeXAU,comment:FeXAU,active_revision_ptr:FeXAU,outgoing_revision_ptrs:Set[FeXAU],incoming_revision_ptr:FeXAU,version_number:FeXAM):
  FeXAD().__init__(hash_ref,state_files,parent_ptr)
  self.creator=creator
  self.comment=comment
  self.active_revision_ptr=active_revision_ptr
  self.outgoing_revision_ptrs=outgoing_revision_ptrs
  self.incoming_revision_ptr=incoming_revision_ptr
  self.version_number=version_number
 def __str__(self):
  return VER_TXT_LAYOUT.format(FeXAh=self.hash_ref,parent=self.parent_ptr,creator=self.creator,comment=self.comment,version_number=self.version_number,active_revision=self.active_revision_ptr,outgoing_revisions=";".join(self.outgoing_revision_ptrs),incoming_revision=self.incoming_revision_ptr,state_files=";".join(FeXAg(lambda stat_file:FeXAU(stat_file),self.state_files))if self.state_files else "")
 def info_str(self):
  return f"{self.version_number}, {self.creator}, {self.comment}"
# Created by pyminifier (https://github.com/liftoff/pyminifier)
