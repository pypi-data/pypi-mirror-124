from typing import Set
DfYhP=str
DfYhr=int
DfYhp=super
DfYhw=False
DfYhl=isinstance
DfYhI=hash
DfYhF=True
DfYhi=list
DfYhE=map
DfYha=None
from localstack_ext.bootstrap.cpvcs.constants import(COMMIT_TXT_LAYOUT,REV_TXT_LAYOUT,STATE_TXT_LAYOUT,STATE_TXT_METADATA,VER_TXT_LAYOUT)
class CPVCSObj:
 def __init__(self,hash_ref:DfYhP):
  self.hash_ref:DfYhP=hash_ref
class StateFileRef(CPVCSObj):
 txt_layout=STATE_TXT_LAYOUT
 metadata_layout=STATE_TXT_METADATA
 def __init__(self,hash_ref:DfYhP,rel_path:DfYhP,file_name:DfYhP,size:DfYhr,service:DfYhP,region:DfYhP):
  DfYhp().__init__(hash_ref)
  self.rel_path:DfYhP=rel_path
  self.file_name:DfYhP=file_name
  self.size:DfYhr=size
  self.service:DfYhP=service
  self.region:DfYhP=region
 def __str__(self):
  return self.txt_layout.format(size=self.size,service=self.service,region=self.region,DfYhI=self.hash_ref,file_name=self.file_name,rel_path=self.rel_path)
 def __eq__(self,other):
  if not other:
   return DfYhw
  if not DfYhl(other,StateFileRef):
   return DfYhw
  return(self.hash_ref==other.hash_ref and self.region==other.region and self.service==self.service and self.file_name==other.file_name and self.size==other.size)
 def __hash__(self):
  return DfYhI((self.hash_ref,self.region,self.service,self.file_name,self.size))
 def congruent(self,other):
  if not other:
   return DfYhw
  if not DfYhl(other,StateFileRef):
   return DfYhw
  return(self.region==other.region and self.service==other.service and self.file_name==other.file_name and self.rel_path==other.rel_path)
 def any_congruence(self,others):
  for other in others:
   if self.congruent(other):
    return DfYhF
  return DfYhw
 def metadata(self)->DfYhP:
  return self.metadata_layout.format(size=self.size,service=self.service,region=self.region)
class CPVCSNode(CPVCSObj):
 def __init__(self,hash_ref:DfYhP,state_files:Set[StateFileRef],parent_ptr:DfYhP):
  DfYhp().__init__(hash_ref)
  self.state_files:Set[StateFileRef]=state_files
  self.parent_ptr:DfYhP=parent_ptr
 def state_files_info(self)->DfYhP:
  return "\n".join(DfYhi(DfYhE(lambda state_file:DfYhP(state_file),self.state_files)))
class Commit:
 txt_layout=COMMIT_TXT_LAYOUT
 def __init__(self,tail_ptr:DfYhP,head_ptr:DfYhP,delta_log_ptr:DfYhP=DfYha):
  self.tail_ptr:DfYhP=tail_ptr
  self.head_ptr:DfYhP=head_ptr
  self.delta_log_ptr:DfYhP=delta_log_ptr
 def __str__(self):
  return self.txt_layout.format(tail_ptr=self.tail_ptr,head_ptr=self.head_ptr,log_hash=self.delta_log_ptr)
class Revision(CPVCSNode):
 txt_layout=REV_TXT_LAYOUT
 def __init__(self,hash_ref:DfYhP,state_files:Set[StateFileRef],parent_ptr:DfYhP,creator:DfYhP,rid:DfYhP,revision_number:DfYhr,assoc_commit:Commit=DfYha):
  DfYhp().__init__(hash_ref,state_files,parent_ptr)
  self.creator:DfYhP=creator
  self.rid:DfYhP=rid
  self.revision_number:DfYhr=revision_number
  self.assoc_commit=assoc_commit
 def __str__(self):
  return self.txt_layout.format(DfYhI=self.hash_ref,parent=self.parent_ptr,creator=self.creator,rid=self.rid,rev_no=self.revision_number,state_files=";".join(DfYhE(lambda state_file:DfYhP(state_file),self.state_files))if self.state_files else "",assoc_commit=DfYhP(self.assoc_commit))
class Version(CPVCSNode):
 txt_layout=VER_TXT_LAYOUT
 def __init__(self,hash_ref:DfYhP,state_files:Set[StateFileRef],parent_ptr:DfYhP,creator:DfYhP,comment:DfYhP,active_revision_ptr:DfYhP,outgoing_revision_ptrs:Set[DfYhP],incoming_revision_ptr:DfYhP,version_number:DfYhr):
  DfYhp().__init__(hash_ref,state_files,parent_ptr)
  self.creator=creator
  self.comment=comment
  self.active_revision_ptr=active_revision_ptr
  self.outgoing_revision_ptrs=outgoing_revision_ptrs
  self.incoming_revision_ptr=incoming_revision_ptr
  self.version_number=version_number
 def __str__(self):
  return VER_TXT_LAYOUT.format(DfYhI=self.hash_ref,parent=self.parent_ptr,creator=self.creator,comment=self.comment,version_number=self.version_number,active_revision=self.active_revision_ptr,outgoing_revisions=";".join(self.outgoing_revision_ptrs),incoming_revision=self.incoming_revision_ptr,state_files=";".join(DfYhE(lambda stat_file:DfYhP(stat_file),self.state_files))if self.state_files else "")
 def info_str(self):
  return f"{self.version_number}, {self.creator}, {self.comment}"
# Created by pyminifier (https://github.com/liftoff/pyminifier)
