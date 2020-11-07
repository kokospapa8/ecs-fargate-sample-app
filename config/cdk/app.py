#!/usr/bin/env python3
import os

from aws_cdk import core
from ecs_sample_cdk.sample_stack import SampleStack

env = core.Environment(
    account=os.environ.get("CDK_DEFAULT_ACCOUNT", ""),
    region=os.environ.get("CDK_DEFAULT_REGION", "")

)

app = core.App()
SampleStack(app, "ecs-sample", env=env)

app.synth()
