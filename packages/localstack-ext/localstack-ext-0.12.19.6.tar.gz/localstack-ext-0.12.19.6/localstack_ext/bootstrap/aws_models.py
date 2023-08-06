from localstack.utils.aws import aws_models
dguYO=super
dguYE=None
dguYn=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  dguYO(LambdaLayer,self).__init__(arn)
  self.cwd=dguYE
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.dguYn.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,dguYn,env=dguYE):
  dguYO(RDSDatabase,self).__init__(dguYn,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,dguYn,env=dguYE):
  dguYO(RDSCluster,self).__init__(dguYn,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,dguYn,env=dguYE):
  dguYO(AppSyncAPI,self).__init__(dguYn,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,dguYn,env=dguYE):
  dguYO(AmplifyApp,self).__init__(dguYn,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,dguYn,env=dguYE):
  dguYO(ElastiCacheCluster,self).__init__(dguYn,env=env)
class TransferServer(BaseComponent):
 def __init__(self,dguYn,env=dguYE):
  dguYO(TransferServer,self).__init__(dguYn,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,dguYn,env=dguYE):
  dguYO(CloudFrontDistribution,self).__init__(dguYn,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,dguYn,env=dguYE):
  dguYO(CodeCommitRepository,self).__init__(dguYn,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
