"""
Type annotations for eks service literal definitions.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_eks/literals.html)

Usage::

    ```python
    from mypy_boto3_eks.literals import AMITypesType

    data: AMITypesType = "AL2_ARM_64"
    ```
"""
import sys

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = (
    "AMITypesType",
    "AddonActiveWaiterName",
    "AddonDeletedWaiterName",
    "AddonIssueCodeType",
    "AddonStatusType",
    "CapacityTypesType",
    "ClusterActiveWaiterName",
    "ClusterDeletedWaiterName",
    "ClusterStatusType",
    "ConnectorConfigProviderType",
    "DescribeAddonVersionsPaginatorName",
    "ErrorCodeType",
    "FargateProfileActiveWaiterName",
    "FargateProfileDeletedWaiterName",
    "FargateProfileStatusType",
    "ListAddonsPaginatorName",
    "ListClustersPaginatorName",
    "ListFargateProfilesPaginatorName",
    "ListIdentityProviderConfigsPaginatorName",
    "ListNodegroupsPaginatorName",
    "ListUpdatesPaginatorName",
    "LogTypeType",
    "NodegroupActiveWaiterName",
    "NodegroupDeletedWaiterName",
    "NodegroupIssueCodeType",
    "NodegroupStatusType",
    "ResolveConflictsType",
    "TaintEffectType",
    "UpdateParamTypeType",
    "UpdateStatusType",
    "UpdateTypeType",
    "configStatusType",
    "ServiceName",
    "PaginatorName",
    "WaiterName",
)

AMITypesType = Literal["AL2_ARM_64", "AL2_x86_64", "AL2_x86_64_GPU", "CUSTOM"]
AddonActiveWaiterName = Literal["addon_active"]
AddonDeletedWaiterName = Literal["addon_deleted"]
AddonIssueCodeType = Literal[
    "AccessDenied",
    "AdmissionRequestDenied",
    "ClusterUnreachable",
    "ConfigurationConflict",
    "InsufficientNumberOfReplicas",
    "InternalFailure",
    "K8sResourceNotFound",
    "UnsupportedAddonModification",
]
AddonStatusType = Literal[
    "ACTIVE", "CREATE_FAILED", "CREATING", "DEGRADED", "DELETE_FAILED", "DELETING", "UPDATING"
]
CapacityTypesType = Literal["ON_DEMAND", "SPOT"]
ClusterActiveWaiterName = Literal["cluster_active"]
ClusterDeletedWaiterName = Literal["cluster_deleted"]
ClusterStatusType = Literal["ACTIVE", "CREATING", "DELETING", "FAILED", "PENDING", "UPDATING"]
ConnectorConfigProviderType = Literal[
    "AKS", "ANTHOS", "EC2", "EKS_ANYWHERE", "GKE", "OPENSHIFT", "OTHER", "RANCHER", "TANZU"
]
DescribeAddonVersionsPaginatorName = Literal["describe_addon_versions"]
ErrorCodeType = Literal[
    "AccessDenied",
    "AdmissionRequestDenied",
    "ClusterUnreachable",
    "ConfigurationConflict",
    "EniLimitReached",
    "InsufficientFreeAddresses",
    "InsufficientNumberOfReplicas",
    "IpNotAvailable",
    "K8sResourceNotFound",
    "NodeCreationFailure",
    "OperationNotPermitted",
    "PodEvictionFailure",
    "SecurityGroupNotFound",
    "SubnetNotFound",
    "Unknown",
    "UnsupportedAddonModification",
    "VpcIdNotFound",
]
FargateProfileActiveWaiterName = Literal["fargate_profile_active"]
FargateProfileDeletedWaiterName = Literal["fargate_profile_deleted"]
FargateProfileStatusType = Literal[
    "ACTIVE", "CREATE_FAILED", "CREATING", "DELETE_FAILED", "DELETING"
]
ListAddonsPaginatorName = Literal["list_addons"]
ListClustersPaginatorName = Literal["list_clusters"]
ListFargateProfilesPaginatorName = Literal["list_fargate_profiles"]
ListIdentityProviderConfigsPaginatorName = Literal["list_identity_provider_configs"]
ListNodegroupsPaginatorName = Literal["list_nodegroups"]
ListUpdatesPaginatorName = Literal["list_updates"]
LogTypeType = Literal["api", "audit", "authenticator", "controllerManager", "scheduler"]
NodegroupActiveWaiterName = Literal["nodegroup_active"]
NodegroupDeletedWaiterName = Literal["nodegroup_deleted"]
NodegroupIssueCodeType = Literal[
    "AccessDenied",
    "AsgInstanceLaunchFailures",
    "AutoScalingGroupInvalidConfiguration",
    "AutoScalingGroupNotFound",
    "ClusterUnreachable",
    "Ec2LaunchTemplateNotFound",
    "Ec2LaunchTemplateVersionMismatch",
    "Ec2SecurityGroupDeletionFailure",
    "Ec2SecurityGroupNotFound",
    "Ec2SubnetInvalidConfiguration",
    "Ec2SubnetNotFound",
    "IamInstanceProfileNotFound",
    "IamLimitExceeded",
    "IamNodeRoleNotFound",
    "InstanceLimitExceeded",
    "InsufficientFreeAddresses",
    "InternalFailure",
    "NodeCreationFailure",
]
NodegroupStatusType = Literal[
    "ACTIVE", "CREATE_FAILED", "CREATING", "DEGRADED", "DELETE_FAILED", "DELETING", "UPDATING"
]
ResolveConflictsType = Literal["NONE", "OVERWRITE"]
TaintEffectType = Literal["NO_EXECUTE", "NO_SCHEDULE", "PREFER_NO_SCHEDULE"]
UpdateParamTypeType = Literal[
    "AddonVersion",
    "ClusterLogging",
    "DesiredSize",
    "EncryptionConfig",
    "EndpointPrivateAccess",
    "EndpointPublicAccess",
    "IdentityProviderConfig",
    "LabelsToAdd",
    "LabelsToRemove",
    "LaunchTemplateName",
    "LaunchTemplateVersion",
    "MaxSize",
    "MaxUnavailable",
    "MaxUnavailablePercentage",
    "MinSize",
    "PlatformVersion",
    "PublicAccessCidrs",
    "ReleaseVersion",
    "ResolveConflicts",
    "ServiceAccountRoleArn",
    "TaintsToAdd",
    "TaintsToRemove",
    "Version",
]
UpdateStatusType = Literal["Cancelled", "Failed", "InProgress", "Successful"]
UpdateTypeType = Literal[
    "AddonUpdate",
    "AssociateEncryptionConfig",
    "AssociateIdentityProviderConfig",
    "ConfigUpdate",
    "DisassociateIdentityProviderConfig",
    "EndpointAccessUpdate",
    "LoggingUpdate",
    "VersionUpdate",
]
configStatusType = Literal["ACTIVE", "CREATING", "DELETING"]
ServiceName = Literal[
    "accessanalyzer",
    "account",
    "acm",
    "acm-pca",
    "alexaforbusiness",
    "amp",
    "amplify",
    "amplifybackend",
    "apigateway",
    "apigatewaymanagementapi",
    "apigatewayv2",
    "appconfig",
    "appflow",
    "appintegrations",
    "application-autoscaling",
    "application-insights",
    "applicationcostprofiler",
    "appmesh",
    "apprunner",
    "appstream",
    "appsync",
    "athena",
    "auditmanager",
    "autoscaling",
    "autoscaling-plans",
    "backup",
    "batch",
    "braket",
    "budgets",
    "ce",
    "chime",
    "chime-sdk-identity",
    "chime-sdk-messaging",
    "cloud9",
    "cloudcontrol",
    "clouddirectory",
    "cloudformation",
    "cloudfront",
    "cloudhsm",
    "cloudhsmv2",
    "cloudsearch",
    "cloudsearchdomain",
    "cloudtrail",
    "cloudwatch",
    "codeartifact",
    "codebuild",
    "codecommit",
    "codedeploy",
    "codeguru-reviewer",
    "codeguruprofiler",
    "codepipeline",
    "codestar",
    "codestar-connections",
    "codestar-notifications",
    "cognito-identity",
    "cognito-idp",
    "cognito-sync",
    "comprehend",
    "comprehendmedical",
    "compute-optimizer",
    "config",
    "connect",
    "connect-contact-lens",
    "connectparticipant",
    "cur",
    "customer-profiles",
    "databrew",
    "dataexchange",
    "datapipeline",
    "datasync",
    "dax",
    "detective",
    "devicefarm",
    "devops-guru",
    "directconnect",
    "discovery",
    "dlm",
    "dms",
    "docdb",
    "ds",
    "dynamodb",
    "dynamodbstreams",
    "ebs",
    "ec2",
    "ec2-instance-connect",
    "ecr",
    "ecr-public",
    "ecs",
    "efs",
    "eks",
    "elastic-inference",
    "elasticache",
    "elasticbeanstalk",
    "elastictranscoder",
    "elb",
    "elbv2",
    "emr",
    "emr-containers",
    "es",
    "events",
    "finspace",
    "finspace-data",
    "firehose",
    "fis",
    "fms",
    "forecast",
    "forecastquery",
    "frauddetector",
    "fsx",
    "gamelift",
    "glacier",
    "globalaccelerator",
    "glue",
    "grafana",
    "greengrass",
    "greengrassv2",
    "groundstation",
    "guardduty",
    "health",
    "healthlake",
    "honeycode",
    "iam",
    "identitystore",
    "imagebuilder",
    "importexport",
    "inspector",
    "iot",
    "iot-data",
    "iot-jobs-data",
    "iot1click-devices",
    "iot1click-projects",
    "iotanalytics",
    "iotdeviceadvisor",
    "iotevents",
    "iotevents-data",
    "iotfleethub",
    "iotsecuretunneling",
    "iotsitewise",
    "iotthingsgraph",
    "iotwireless",
    "ivs",
    "kafka",
    "kafkaconnect",
    "kendra",
    "kinesis",
    "kinesis-video-archived-media",
    "kinesis-video-media",
    "kinesis-video-signaling",
    "kinesisanalytics",
    "kinesisanalyticsv2",
    "kinesisvideo",
    "kms",
    "lakeformation",
    "lambda",
    "lex-models",
    "lex-runtime",
    "lexv2-models",
    "lexv2-runtime",
    "license-manager",
    "lightsail",
    "location",
    "logs",
    "lookoutequipment",
    "lookoutmetrics",
    "lookoutvision",
    "machinelearning",
    "macie",
    "macie2",
    "managedblockchain",
    "marketplace-catalog",
    "marketplace-entitlement",
    "marketplacecommerceanalytics",
    "mediaconnect",
    "mediaconvert",
    "medialive",
    "mediapackage",
    "mediapackage-vod",
    "mediastore",
    "mediastore-data",
    "mediatailor",
    "memorydb",
    "meteringmarketplace",
    "mgh",
    "mgn",
    "migrationhub-config",
    "mobile",
    "mq",
    "mturk",
    "mwaa",
    "neptune",
    "network-firewall",
    "networkmanager",
    "nimble",
    "opensearch",
    "opsworks",
    "opsworkscm",
    "organizations",
    "outposts",
    "personalize",
    "personalize-events",
    "personalize-runtime",
    "pi",
    "pinpoint",
    "pinpoint-email",
    "pinpoint-sms-voice",
    "polly",
    "pricing",
    "proton",
    "qldb",
    "qldb-session",
    "quicksight",
    "ram",
    "rds",
    "rds-data",
    "redshift",
    "redshift-data",
    "rekognition",
    "resource-groups",
    "resourcegroupstaggingapi",
    "robomaker",
    "route53",
    "route53-recovery-cluster",
    "route53-recovery-control-config",
    "route53-recovery-readiness",
    "route53domains",
    "route53resolver",
    "s3",
    "s3control",
    "s3outposts",
    "sagemaker",
    "sagemaker-a2i-runtime",
    "sagemaker-edge",
    "sagemaker-featurestore-runtime",
    "sagemaker-runtime",
    "savingsplans",
    "schemas",
    "sdb",
    "secretsmanager",
    "securityhub",
    "serverlessrepo",
    "service-quotas",
    "servicecatalog",
    "servicecatalog-appregistry",
    "servicediscovery",
    "ses",
    "sesv2",
    "shield",
    "signer",
    "sms",
    "sms-voice",
    "snow-device-management",
    "snowball",
    "sns",
    "sqs",
    "ssm",
    "ssm-contacts",
    "ssm-incidents",
    "sso",
    "sso-admin",
    "sso-oidc",
    "stepfunctions",
    "storagegateway",
    "sts",
    "support",
    "swf",
    "synthetics",
    "textract",
    "timestream-query",
    "timestream-write",
    "transcribe",
    "transfer",
    "translate",
    "voice-id",
    "waf",
    "waf-regional",
    "wafv2",
    "wellarchitected",
    "wisdom",
    "workdocs",
    "worklink",
    "workmail",
    "workmailmessageflow",
    "workspaces",
    "xray",
]
PaginatorName = Literal[
    "describe_addon_versions",
    "list_addons",
    "list_clusters",
    "list_fargate_profiles",
    "list_identity_provider_configs",
    "list_nodegroups",
    "list_updates",
]
WaiterName = Literal[
    "addon_active",
    "addon_deleted",
    "cluster_active",
    "cluster_deleted",
    "fargate_profile_active",
    "fargate_profile_deleted",
    "nodegroup_active",
    "nodegroup_deleted",
]
