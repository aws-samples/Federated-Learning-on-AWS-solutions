# Introduction
The main purpose of this project is to use AWS CDK to quickly build the required environment for Federated Learning.
In the Federated Learning architecture, there are Server Side and Client Side environments. For effective and proper connectivity between these environments, their VPC IP ranges (CIDR) must not overlap.


We use the Flower framework on Amazon SageMaker because it is framework-agnostic and compatible with machine learning libraries like PyTorch and TensorFlow. 
The architecture can be summarized as follows:
* The `Flower Server` run server with `SageMaker Notebook` is located on the right-hand side of the diagram.
* The `Flower Client` train model with `SageMaker Model Training` is on the left-hand side of the diagram.

![flower-architecture](/imgs/flower-architecture.png)

Therefore, before proceeding with the implementation, please confirm the following for the account environment you plan to use:

Whether it is the Server side or the Client side in the Federated Learning architecture.
The CIDR ranges of the various environments that will be connected to your environment, and ensure they do not overlap.
Afterwards, we will use AWS CDK to automatically deploy the AWS environment and resources needed for the subsequent lessons.

# Installation
#### Install AWS CLI
  https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

#### Install AWS CDK
  https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html

#### Obtain AWS Credentials in the execution environment
  open a terminal and input your AWS account credentials

#### Setting up AWS Account CDK environment
  `cdk bootstrap`

#### Set the environment variable
  `source .venv/bin/activate`

#### Install project dependencies
  `python3 -m pip install -r requirements.txt`

#### Allocate the VPC CIDR we need. For example, if our CIDR is 192.168.1.0/24, we execute the following commands:
#### Use cdk synth to generate the CloudFormation template file.
  `cdk synth -c "vpccidr=192.168.1.0/24"`

#### Use cdk deploy to deploy the project environment.
  `cdk deploy -c "vpccidr=192.168.1.0/24"`

#### After Install 
  Then we use VPC Peering or Site-to-Site VPN to connect with the network environment you want to connect, and then you can start using Federated Learning.
  For more information, please refer to the workshop (https://catalog.us-east-1.prod.workshops.aws/workshops/e4bcd38f-db3f-4c56-b63a-9596dbbb2fbc/en-US)

## License
This library is licensed under the MIT-0 License. For more details, please take a look at the [LICENSE](LICENSE) file.

## Contributing
Please read our [contributing guidelines](CONTRIBUTING.md)
