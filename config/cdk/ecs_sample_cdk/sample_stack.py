from aws_cdk import core
from .vpc_stack import VPCStack
from .alb_stack import ALBStack
from .rds_stack import RDSStack
from .redis_stack import RedisStack

class SampleStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, env, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        props = {'namespace': 'sample'}
        vpc_stack = VPCStack(self, f"{id}-vpc", env=env, props=props)
        props.update(vpc_stack.output_props)

        alb_stack = ALBStack(self, f"{id}-alb", env=env, props=props)
        alb_stack.add_dependency(vpc_stack)
        props.update(alb_stack.output_props)

        rds_stack = RDSStack(self, f"{id}-rds", env=env, props=props)
        rds_stack.add_dependency(vpc_stack)
        rds_stack.add_dependency(alb_stack)
        props.update(rds_stack.output_props)

        redis_stack = RedisStack(self, f"{id}-redis", env=env, props=props)
        redis_stack.add_dependency(vpc_stack)
        redis_stack.add_dependency(alb_stack)
