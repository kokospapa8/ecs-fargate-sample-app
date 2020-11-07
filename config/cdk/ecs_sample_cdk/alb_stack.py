import os


from aws_cdk.aws_ec2 import SubnetType

from aws_cdk import core
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_autoscaling as autoscaling
import aws_cdk.aws_elasticloadbalancingv2 as elbv2
import aws_cdk.aws_iam as iam


KEY_PAIR_NAME = os.environ.get("KEY_PAIR_NAME", None)
SSH_IP = os.environ.get("SSH_IP", "0.0.0.0/0")


class ALBStack(core.NestedStack):

    def __init__(self, scope: core.Construct, id: str, env, props, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        #create ec2role
        #get from env or create
        role = iam.Role(self, "ecs-sample-ec2-role",
                        assumed_by=iam.ServicePrincipal('ec2.amazonaws.com'),
                        )
        role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEC2ContainerRegistryPowerUser")
        )

        asg_api = autoscaling.AutoScalingGroup(
            self,
            "ecs-sample-api-asg",
            vpc=props['vpc'],
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.MICRO
            ),
            machine_image=ec2.AmazonLinuxImage(),
            key_name=KEY_PAIR_NAME,
            vpc_subnets=ec2.SubnetSelection(subnet_type=SubnetType.PUBLIC),
            desired_capacity=1,
            max_capacity=1,
            min_capacity=1,
            role=role
            # userdata=userdata

        )

        asg_worker = autoscaling.AutoScalingGroup(
            self,
            "ecs-sample-worker-asg",
            vpc=props['vpc'],
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.MICRO
            ),
            machine_image=ec2.AmazonLinuxImage(),
            key_name=f"ecs-sample-key",
            vpc_subnets=ec2.SubnetSelection(subnet_type=SubnetType.PRIVATE),
            desired_capacity=1,
            max_capacity=1,
            min_capacity=1,
            role=role
            # userdata=userdata

        )

        # Creates a security group for our application
        sg_api = ec2.SecurityGroup(
                self,
                id="ecs-sample-ec2-api",
                vpc=props['vpc'],
                security_group_name="ecs-sample-ec2-api"
        )
        sg_worker = ec2.SecurityGroup(
                self,
                id="ecs-sample-ec2-worker",
                vpc=props['vpc'],
                security_group_name="ecs-sample-ec2-worker"
        )

        # to access this security group for SSH
        sg_api.add_ingress_rule(
            peer=ec2.Peer.ipv4(SSH_IP),
            connection=ec2.Port.tcp(22)
        )

        # use ec2 api as bastion
        sg_worker.connections.allow_from(
                sg_api, ec2.Port.tcp(22), "Allow from ec2 api")

        asg_api.add_security_group(sg_api)
        asg_worker.add_security_group(sg_worker)

        # Creates a security group for the application load balancer
        sg_alb = ec2.SecurityGroup(
                self,
                id="ecs-sample-loadbalancer",
                vpc=props['vpc'],
                security_group_name="ecs-sample-loadbalancer"
        )

        sg_api.connections.allow_from(
                sg_alb, ec2.Port.tcp(80), "Ingress")


        # Creates an application load balance
        lb = elbv2.ApplicationLoadBalancer(
                self,
                f"{id}-ALB",
                vpc=props['vpc'],
                security_group=sg_alb,
                internet_facing=True)

        listener = lb.add_listener("Listener", port=80)
        # Adds the autoscaling group's (asg_api) instance to be registered
        # as targets on port 8080
        listener.add_targets("Target", port=80, targets=[asg_api])
        # This creates a "0.0.0.0/0" rule to allow every one to access the
        # application
        listener.connections.allow_default_port_from_any_ipv4(
                "Open to the world"
                )

        # create RDS sg
        sg_rds = ec2.SecurityGroup(
                self,
                id="ecs-sample-mysql",
                vpc=props['vpc'],
                security_group_name="ecs-sample-mysql"
        )
        sg_api.connections.allow_from(
                sg_rds, ec2.Port.tcp(3306), "allow from rds to ec2 api")
        sg_rds.connections.allow_from(
                sg_api, ec2.Port.tcp(3306), "allow from ec2 api to rds")
        sg_worker.connections.allow_from(
                sg_rds, ec2.Port.tcp(3306), "allow from rds to ec2 worker")
        sg_rds.connections.allow_from(
                sg_worker, ec2.Port.tcp(3306), "allow from ec2 worker to rds")


        # create Redis SG
        sg_redis = ec2.SecurityGroup(
                self,
                id="ecs-sample-redis",
                vpc=props['vpc'],
                security_group_name="ecs-sample-redis"
        )
        sg_api.connections.allow_from(
                sg_rds, ec2.Port.tcp(6379), "allow from redis to ec2 api")
        sg_rds.connections.allow_from(
                sg_api, ec2.Port.tcp(6379), "allow from ec2 api to redis")
        sg_worker.connections.allow_from(
                sg_rds, ec2.Port.tcp(6379), "allow from redis to ec2 worker")
        sg_rds.connections.allow_from(
                sg_worker, ec2.Port.tcp(6379), "allow from ec2 worker to redis")

        self.output_props = props.copy()
        self.output_props['sg_api'] = sg_api
        self.output_props['sg_worker'] = sg_worker
        self.output_props['sg_rds'] = sg_rds
        self.output_props['sg_redis'] = sg_redis


    @property
    def outputs(self):
        return self.output_props
