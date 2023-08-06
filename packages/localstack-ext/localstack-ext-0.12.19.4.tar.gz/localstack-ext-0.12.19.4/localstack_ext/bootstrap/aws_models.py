from localstack.utils.aws import aws_models
tWoMT=super
tWoMU=None
tWoMP=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  tWoMT(LambdaLayer,self).__init__(arn)
  self.cwd=tWoMU
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.tWoMP.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,tWoMP,env=tWoMU):
  tWoMT(RDSDatabase,self).__init__(tWoMP,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,tWoMP,env=tWoMU):
  tWoMT(RDSCluster,self).__init__(tWoMP,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,tWoMP,env=tWoMU):
  tWoMT(AppSyncAPI,self).__init__(tWoMP,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,tWoMP,env=tWoMU):
  tWoMT(AmplifyApp,self).__init__(tWoMP,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,tWoMP,env=tWoMU):
  tWoMT(ElastiCacheCluster,self).__init__(tWoMP,env=env)
class TransferServer(BaseComponent):
 def __init__(self,tWoMP,env=tWoMU):
  tWoMT(TransferServer,self).__init__(tWoMP,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,tWoMP,env=tWoMU):
  tWoMT(CloudFrontDistribution,self).__init__(tWoMP,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,tWoMP,env=tWoMU):
  tWoMT(CodeCommitRepository,self).__init__(tWoMP,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
