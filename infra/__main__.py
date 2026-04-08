"""An AWS Python Pulumi program that provisions an EC2 instance."""

import pulumi
import pulumi_aws as aws

config = pulumi.Config()
instance_type = config.get("instanceType") or "t3.micro"

# Create a security group that allows SSH inbound and all outbound traffic.
security_group = aws.ec2.SecurityGroup(
    "web-secgrp",
    description="Allow SSH inbound and all outbound",
    ingress=[
        {
            "protocol": "tcp",
            "from_port": 22,
            "to_port": 22,
            "cidr_blocks": ["0.0.0.0/0"],
        },
    ],
    egress=[
        {
            "protocol": "-1",
            "from_port": 0,
            "to_port": 0,
            "cidr_blocks": ["0.0.0.0/0"],
        },
    ],
)

# Create an EC2 instance using the latest Amazon Linux 2023 AMI.
server = aws.ec2.Instance(
    "web-server",
    instance_type=instance_type,
    ami="resolve:ssm:/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64",
    vpc_security_group_ids=[security_group.id],
    tags={
        "Name": "web-server",
    },
)

# Export useful outputs.
pulumi.export("instance_id", server.id)
pulumi.export("public_ip", server.public_ip)
pulumi.export("public_dns", server.public_dns)
