from aws_cdk import core
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_elasticache as cache


class RedisStack(core.NestedStack):

    def __init__(self, scope: core.Construct, id: str, env, props, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        vpc = props['vpc']
        # create subnetgroup
        subnet_ids = []
        for subnet in vpc.public_subnets:
            subnet_ids.append(subnet.subnet_id)
        subnets_group = cache.CfnSubnetGroup(self,
                                             f"{id}-subnet-group",
                                             subnet_ids=subnet_ids,
                                             description=f"{id}-subnet-group",
                                             cache_subnet_group_name=f"{id}-subnet-group")
        # create securitygroup
        sg_redis = props['sg_redis']
        #TEMP without ASG
        # sg_redis = ec2.SecurityGroup(
        #         self,
        #         id="ecs-sample-redis",
        #         vpc=props['vpc'],
        #         security_group_name="ecs-sample-redis"
        # )
        cache_parameter_group_name="default.redis5.0"

        redis = cache.CfnReplicationGroup(self,
                                              f"{id}-replication-group",
                                              replication_group_description=f"{id}-replication group",
                                              cache_node_type="cache.t3.micro",
                                              cache_parameter_group_name=cache_parameter_group_name,
                                              security_group_ids=[sg_redis.security_group_id],
                                              cache_subnet_group_name=subnets_group.cache_subnet_group_name,
                                              engine="redis",
                                              engine_version="5.0.4",
                                              # node_group_configuration
                                              num_node_groups=1, #shard
                                              replicas_per_node_group=1 #one replica
                                              )
        redis.add_depends_on(subnets_group)

        # core.CfnOutput(self, "redis_configuration_endpoint", value=redis.attr_configuration_end_point_address)

        self.output_props = props.copy()
        self.output_props['redis'] = redis

    @property
    def outputs(self):
        return self.output_props

        # core.CfnOutput(self, "REDIS_endpoint", value=redis.get_att("ElastiCacheCluster.RedisEndpoint.Address").)

#   ElastiCacheClusterArn:
#     Description: ElastiCache Cluster Arn
#     Value: !Sub arn:aws:elasticache:${AWS::Region}:${AWS::AccountId}:cluster/${ElastiCacheCluster}
#     Export:
#       Name: !Sub ${AWS::StackName}-ElastiCacheClusterArn
#
# ElastiCacheAddress:
# Description: ElastiCache
# endpoint
# address
# Value: !If[IsRedis, !GetAtt
# ElastiCacheCluster.RedisEndpoint.Address, !GetAtt
# ElastiCacheCluster.ConfigurationEndpoint.Address]
# Export:
# Name: !Sub ${AWS:: StackName}-ElastiCacheAddress