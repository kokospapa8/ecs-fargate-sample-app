from aws_cdk import core
import aws_cdk.aws_ec2 as ec2


class VPCStack(core.NestedStack):

    def __init__(self, scope: core.Construct, id: str, env, props, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        subnets = []

        public_subnet = ec2.SubnetConfiguration(
                           cidr_mask=24,
                           name=f"{id}-public",
                           subnet_type=ec2.SubnetType.PUBLIC
                       )

        private_subnet = ec2.SubnetConfiguration(
                           cidr_mask=24,
                           name=f"{id}-private",
                           subnet_type=ec2.SubnetType.PRIVATE
                       )
        subnets.append(public_subnet)
        subnets.append(private_subnet)

        # The code that defines your stack goes here
        vpc = ec2.Vpc(self, f"{id}",
                           cidr="172.0.0.0/16",
                           enable_dns_hostnames=True,
                           enable_dns_support=True,
                           nat_gateways=1,
                           nat_gateway_provider=ec2.NatProvider.gateway(),
                           max_azs=2,
                           subnet_configuration=subnets
                           )
        #Be aware that environment-agnostic stacks will be created with access to only 2 AZs, so to use more than 2 AZs, be sure to specify the account and region on your stack

        core.CfnOutput(self, "vpcid",
                       value=vpc.vpc_id)

        # Prepares output attributes to be passed into other stacks
        # In this case, it is our VPC and subnets.
        self.output_props = props.copy()
        self.output_props['vpc'] = vpc
        self.output_props['public_subnets'] = vpc.public_subnets
        self.output_props['private_subnets'] = vpc.private_subnets

    @property
    def outputs(self):
        return self.output_props
