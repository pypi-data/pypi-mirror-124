from localstack.utils.aws import aws_models
tnSGp=super
tnSGg=None
tnSGs=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  tnSGp(LambdaLayer,self).__init__(arn)
  self.cwd=tnSGg
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.tnSGs.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,tnSGs,env=tnSGg):
  tnSGp(RDSDatabase,self).__init__(tnSGs,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,tnSGs,env=tnSGg):
  tnSGp(RDSCluster,self).__init__(tnSGs,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,tnSGs,env=tnSGg):
  tnSGp(AppSyncAPI,self).__init__(tnSGs,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,tnSGs,env=tnSGg):
  tnSGp(AmplifyApp,self).__init__(tnSGs,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,tnSGs,env=tnSGg):
  tnSGp(ElastiCacheCluster,self).__init__(tnSGs,env=env)
class TransferServer(BaseComponent):
 def __init__(self,tnSGs,env=tnSGg):
  tnSGp(TransferServer,self).__init__(tnSGs,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,tnSGs,env=tnSGg):
  tnSGp(CloudFrontDistribution,self).__init__(tnSGs,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,tnSGs,env=tnSGg):
  tnSGp(CodeCommitRepository,self).__init__(tnSGs,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
