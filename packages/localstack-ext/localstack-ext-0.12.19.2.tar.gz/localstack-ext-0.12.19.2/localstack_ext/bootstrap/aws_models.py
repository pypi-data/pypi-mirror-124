from localstack.utils.aws import aws_models
JYyse=super
JYysN=None
JYysF=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  JYyse(LambdaLayer,self).__init__(arn)
  self.cwd=JYysN
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.JYysF.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,JYysF,env=JYysN):
  JYyse(RDSDatabase,self).__init__(JYysF,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,JYysF,env=JYysN):
  JYyse(RDSCluster,self).__init__(JYysF,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,JYysF,env=JYysN):
  JYyse(AppSyncAPI,self).__init__(JYysF,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,JYysF,env=JYysN):
  JYyse(AmplifyApp,self).__init__(JYysF,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,JYysF,env=JYysN):
  JYyse(ElastiCacheCluster,self).__init__(JYysF,env=env)
class TransferServer(BaseComponent):
 def __init__(self,JYysF,env=JYysN):
  JYyse(TransferServer,self).__init__(JYysF,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,JYysF,env=JYysN):
  JYyse(CloudFrontDistribution,self).__init__(JYysF,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,JYysF,env=JYysN):
  JYyse(CodeCommitRepository,self).__init__(JYysF,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
