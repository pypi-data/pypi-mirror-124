from localstack.services.cloudformation.service_models import GenericBaseModel
hbGSW=staticmethod
hbGSc=None
hbGSJ=classmethod
from localstack.utils.aws import aws_stack
class KafkaCluster(GenericBaseModel):
 @hbGSW
 def cloudformation_type():
  return "AWS::MSK::Cluster"
 def get_physical_resource_id(self,attribute=hbGSc,**kwargs):
  return self.props.get("ClusterArn")
 def fetch_state(self,stack_name,resources):
  client=aws_stack.connect_to_service("kafka")
  cluster_name=self.resolve_refs_recursively(stack_name,self.props["ClusterName"],resources)
  clusters=client.list_clusters()["ClusterInfoList"]
  clusters=[c for c in clusters if c["ClusterName"]==cluster_name]
  return(clusters or[hbGSc])[0]
 @hbGSJ
 def get_deploy_templates(cls):
  def _delete_params(params,resource_id,resources,**kwargs):
   resource=cls(resources[resource_id])
   return{"ClusterArn":resource.props.get("ClusterArn")}
  return{"create":{"function":"create_cluster"},"delete":{"function":"delete_cluster","parameters":_delete_params}}
# Created by pyminifier (https://github.com/liftoff/pyminifier)
