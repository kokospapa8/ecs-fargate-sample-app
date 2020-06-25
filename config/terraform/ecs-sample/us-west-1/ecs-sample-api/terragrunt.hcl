terraform {
  source = "git::git@github.com:terraform-aws-modules/terraform-aws-ec2-instance.git?ref=v2.13.0"
}

include {
  path = find_in_parent_folders()
}

dependencies {
  paths = ["../aws-data"]
}

dependency "aws-data" {
  config_path = "../aws-data"
}

###########################################################
# View all available inputs for this module:
# https://registry.terraform.io/modules/terraform-aws-modules/ec2-instance/aws/2.13.0?tab=inputs
###########################################################
inputs = {
  # ID of AMI to use for the instance
  # type: string
  ami = dependency.aws-data.outputs.amazon_linux2_aws_ami_id

  # The type of instance to start
  # type: string
  instance_type = "t2.micro"

  # Name to be used on all resources as prefix
  # type: string
  name = "ecs-sample-api"

  
}
