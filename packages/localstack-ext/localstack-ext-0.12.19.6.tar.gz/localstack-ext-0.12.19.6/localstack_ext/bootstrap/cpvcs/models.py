from datetime import datetime
hnsJy=str
hnsJk=int
hnsJw=super
hnsJR=False
hnsJE=isinstance
hnsJS=hash
hnsJN=True
hnsJP=list
hnsJc=map
hnsJd=None
from typing import Set
from localstack_ext.bootstrap.cpvcs.constants import(COMMIT_TXT_LAYOUT,REV_TXT_LAYOUT,STATE_TXT_LAYOUT,STATE_TXT_METADATA,VER_TXT_LAYOUT)
class CPVCSObj:
 def __init__(self,hash_ref:hnsJy):
  self.hash_ref:hnsJy=hash_ref
class StateFileRef(CPVCSObj):
 txt_layout=STATE_TXT_LAYOUT
 metadata_layout=STATE_TXT_METADATA
 def __init__(self,hash_ref:hnsJy,rel_path:hnsJy,file_name:hnsJy,size:hnsJk,service:hnsJy,region:hnsJy):
  hnsJw().__init__(hash_ref)
  self.rel_path:hnsJy=rel_path
  self.file_name:hnsJy=file_name
  self.size:hnsJk=size
  self.service:hnsJy=service
  self.region:hnsJy=region
 def __str__(self):
  return self.txt_layout.format(size=self.size,service=self.service,region=self.region,hnsJS=self.hash_ref,file_name=self.file_name,rel_path=self.rel_path)
 def __eq__(self,other):
  if not other:
   return hnsJR
  if not hnsJE(other,StateFileRef):
   return hnsJR
  return(self.hash_ref==other.hash_ref and self.region==other.region and self.service==self.service and self.file_name==other.file_name and self.size==other.size)
 def __hash__(self):
  return hnsJS((self.hash_ref,self.region,self.service,self.file_name,self.size))
 def congruent(self,other):
  if not other:
   return hnsJR
  if not hnsJE(other,StateFileRef):
   return hnsJR
  return(self.region==other.region and self.service==other.service and self.file_name==other.file_name and self.rel_path==other.rel_path)
 def any_congruence(self,others):
  for other in others:
   if self.congruent(other):
    return hnsJN
  return hnsJR
 def metadata(self)->hnsJy:
  return self.metadata_layout.format(size=self.size,service=self.service,region=self.region)
class CPVCSNode(CPVCSObj):
 def __init__(self,hash_ref:hnsJy,state_files:Set[StateFileRef],parent_ptr:hnsJy):
  hnsJw().__init__(hash_ref)
  self.state_files:Set[StateFileRef]=state_files
  self.parent_ptr:hnsJy=parent_ptr
 def state_files_info(self)->hnsJy:
  return "\n".join(hnsJP(hnsJc(lambda state_file:hnsJy(state_file),self.state_files)))
class Commit:
 txt_layout=COMMIT_TXT_LAYOUT
 def __init__(self,tail_ptr:hnsJy,head_ptr:hnsJy,message:hnsJy,timestamp:hnsJy=hnsJy(datetime.now().timestamp()),delta_log_ptr:hnsJy=hnsJd):
  self.tail_ptr:hnsJy=tail_ptr
  self.head_ptr:hnsJy=head_ptr
  self.message:hnsJy=message
  self.timestamp:hnsJy=timestamp
  self.delta_log_ptr:hnsJy=delta_log_ptr
 def __str__(self):
  return self.txt_layout.format(tail_ptr=self.tail_ptr,head_ptr=self.head_ptr,message=self.message,timestamp=self.timestamp,log_hash=self.delta_log_ptr)
 def info_str(self,from_node:hnsJy,to_node:hnsJy)->hnsJy:
  return f"from: {from_node}, to: {to_node}, message: {self.message}, time: {datetime.fromtimestamp(float(self.timestamp))}"
class Revision(CPVCSNode):
 txt_layout=REV_TXT_LAYOUT
 def __init__(self,hash_ref:hnsJy,state_files:Set[StateFileRef],parent_ptr:hnsJy,creator:hnsJy,rid:hnsJy,revision_number:hnsJk,assoc_commit:Commit=hnsJd):
  hnsJw().__init__(hash_ref,state_files,parent_ptr)
  self.creator:hnsJy=creator
  self.rid:hnsJy=rid
  self.revision_number:hnsJk=revision_number
  self.assoc_commit=assoc_commit
 def __str__(self):
  return self.txt_layout.format(hnsJS=self.hash_ref,parent=self.parent_ptr,creator=self.creator,rid=self.rid,rev_no=self.revision_number,state_files=";".join(hnsJc(lambda state_file:hnsJy(state_file),self.state_files))if self.state_files else "",assoc_commit=hnsJy(self.assoc_commit))
class Version(CPVCSNode):
 txt_layout=VER_TXT_LAYOUT
 def __init__(self,hash_ref:hnsJy,state_files:Set[StateFileRef],parent_ptr:hnsJy,creator:hnsJy,comment:hnsJy,active_revision_ptr:hnsJy,outgoing_revision_ptrs:Set[hnsJy],incoming_revision_ptr:hnsJy,version_number:hnsJk):
  hnsJw().__init__(hash_ref,state_files,parent_ptr)
  self.creator=creator
  self.comment=comment
  self.active_revision_ptr=active_revision_ptr
  self.outgoing_revision_ptrs=outgoing_revision_ptrs
  self.incoming_revision_ptr=incoming_revision_ptr
  self.version_number=version_number
 def __str__(self):
  return VER_TXT_LAYOUT.format(hnsJS=self.hash_ref,parent=self.parent_ptr,creator=self.creator,comment=self.comment,version_number=self.version_number,active_revision=self.active_revision_ptr,outgoing_revisions=";".join(self.outgoing_revision_ptrs),incoming_revision=self.incoming_revision_ptr,state_files=";".join(hnsJc(lambda stat_file:hnsJy(stat_file),self.state_files))if self.state_files else "")
 def info_str(self):
  return f"{self.version_number}, {self.creator}, {self.comment}"
# Created by pyminifier (https://github.com/liftoff/pyminifier)
