# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

# This is a sample for workshop - Flower Federated Learning Workshop
# https://catalog.us-east-1.prod.workshops.aws/workshops/e4bcd38f-db3f-4c56-b63a-9596dbbb2fbc
# Before actually using it in a production environment, 
# please ensure that you understand the functions, effects, and limitations of all components, 
# and adjust them to a state suitable for your environment.


#!/usr/bin/env python3
import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_sagemaker as sagemaker,
    aws_ec2 as ec2,
    aws_iam as iam   
)

from constructs import Construct

class VpcStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # create VPC environment with private subnet and S3 gateway endpoint
        self.vpc = ec2.Vpc(
            self, "vpc-fl",
            cidr=self.node.try_get_context('vpccidr'),
            max_azs=1,
            gateway_endpoints={
                "S3": cdk.aws_ec2.GatewayVpcEndpointOptions(
                    service=ec2.GatewayVpcEndpointAwsService.S3
                )
            },
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="private-subnet",
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                    cidr_mask=24
                )
            ]
        )

        subnet_id = self.vpc.select_subnets( subnet_type=ec2.SubnetType.PRIVATE_ISOLATED ).subnet_ids[0]
        sg_id = self.vpc.vpc_default_security_group
        #create sagemaker role with SageMakerFullAccess permission
        sagemaker_role = iam.Role(self, "my-sagemaker-role",
            assumed_by=iam.ServicePrincipal("sagemaker.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSageMakerFullAccess")
            ])
        
        #create sagemaker instance lifecycle config, download workshop assets when instance start
        cfn_notebook_instance_lifecycle_config = sagemaker.CfnNotebookInstanceLifecycleConfig(self, "MyCfnNotebookInstanceLifecycleConfig",
            notebook_instance_lifecycle_config_name="notebookInstanceLifecycleConfigName",
            on_start=[sagemaker.CfnNotebookInstanceLifecycleConfig.NotebookInstanceLifecycleHookProperty(
                content=cdk.Fn.base64("""
#!/bin/bash
cd /home/ec2-user/SageMaker
wget https://ws-assets-prod-iad-r-iad-ed304a55c2ca1aee.s3.us-east-1.amazonaws.com/e4bcd38f-db3f-4c56-b63a-9596dbbb2fbc/flower-on-sagemaker.zip
unzip flower-on-sagemaker.zip
                """)
            )]
        )
        
        #create notebook instance
        notebook_instance = sagemaker.CfnNotebookInstance(self, "MyCfnNotebookInstance",
            instance_type="ml.r5.xlarge",
            role_arn=sagemaker_role.role_arn,
            lifecycle_config_name = cfn_notebook_instance_lifecycle_config.notebook_instance_lifecycle_config_name,
            notebook_instance_name="my-notebook",
            volume_size_in_gb=200,
            subnet_id=subnet_id,
            security_group_ids=[sg_id]
        )

app = cdk.App()
vpc_stack = VpcStack(app, "fl-vpc-stack")
app.synth()