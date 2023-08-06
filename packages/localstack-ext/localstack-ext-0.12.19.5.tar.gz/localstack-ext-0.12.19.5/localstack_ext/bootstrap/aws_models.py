from localstack.utils.aws import aws_models
eXTCA=super
eXTCk=None
eXTCQ=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  eXTCA(LambdaLayer,self).__init__(arn)
  self.cwd=eXTCk
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.eXTCQ.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,eXTCQ,env=eXTCk):
  eXTCA(RDSDatabase,self).__init__(eXTCQ,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,eXTCQ,env=eXTCk):
  eXTCA(RDSCluster,self).__init__(eXTCQ,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,eXTCQ,env=eXTCk):
  eXTCA(AppSyncAPI,self).__init__(eXTCQ,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,eXTCQ,env=eXTCk):
  eXTCA(AmplifyApp,self).__init__(eXTCQ,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,eXTCQ,env=eXTCk):
  eXTCA(ElastiCacheCluster,self).__init__(eXTCQ,env=env)
class TransferServer(BaseComponent):
 def __init__(self,eXTCQ,env=eXTCk):
  eXTCA(TransferServer,self).__init__(eXTCQ,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,eXTCQ,env=eXTCk):
  eXTCA(CloudFrontDistribution,self).__init__(eXTCQ,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,eXTCQ,env=eXTCk):
  eXTCA(CodeCommitRepository,self).__init__(eXTCQ,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
