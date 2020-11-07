from aws_cdk import core
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_rds as rds


class RDSStack(core.NestedStack):

    def __init__(self, scope: core.Construct, id: str, env, props, cluster=False, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        #TEMP without ASG
        # security_groups = [ec2.SecurityGroup(
        #         self,
        #         id="ecs-sample-mysql",
        #         vpc=props['vpc'],
        #         security_group_name="ecs-sample-mysql"
        # )]


        vpc = props['vpc']
        security_groups=[props['sg_rds']]
        credential = rds.Credentials.from_username(username="admin")
        private_subnet_selections = ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE)
        subnet_group = rds.SubnetGroup(self, "sample-rds-subnet-group",
                                       vpc=vpc,
                                       subnet_group_name="sample-rds-subnet-group",
                                       vpc_subnets=private_subnet_selections,
                                       description="sample-rds-subnet-group")
        self.output_props = props.copy()

        if not cluster:
            rds_instance = rds.DatabaseInstance(
                self, "RDS-instance",
                database_name="sample",
                engine=rds.DatabaseInstanceEngine.mysql(
                    version=rds.MysqlEngineVersion.VER_8_0_16
                ),
                credentials=credential,
                instance_identifier="ecs-sample-db",

                vpc=vpc,
                port=3306,
                instance_type=ec2.InstanceType.of(
                    ec2.InstanceClass.BURSTABLE3,
                    ec2.InstanceSize.MICRO,
                ),
                subnet_group=subnet_group,
                vpc_subnets=private_subnet_selections,
                removal_policy=core.RemovalPolicy.DESTROY,
                deletion_protection=False,
                security_groups=security_groups

            )
            core.CfnOutput(self, "RDS_instnace_endpoint", value=rds_instance.db_instance_endpoint_address)
            self.output_props['rds'] = rds_instance

        else:
            instance_props = rds.InstanceProps(
                vpc=vpc,
                security_groups=security_groups,
                vpc_subnets=private_subnet_selections
            )
            rds_cluster = rds.DatabaseCluster(
                self, "RDS-cluster",
                cluster_identifier="ecs-sample-db-cluster",
                instance_props=instance_props,
                engine=rds.DatabaseClusterEngine.aurora_mysql(
                    version=rds.AuroraMysqlEngineVersion.VER_2_07_1
                ),
                credentials=credential,
                default_database_name="sample",
                instances=1,
                subnet_group=subnet_group,
                removal_policy=core.RemovalPolicy.DESTROY,
                deletion_protection=False
            )
            core.CfnOutput(self, "RDS_cluster_endpoint", value=rds_cluster.cluster_endpoint.hostname)
            self.output_props['rds'] = rds_cluster


    @property
    def outputs(self):
        return self.output_props