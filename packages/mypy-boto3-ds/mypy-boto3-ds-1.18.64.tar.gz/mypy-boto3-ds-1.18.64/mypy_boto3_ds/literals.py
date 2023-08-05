"""
Type annotations for ds service literal definitions.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ds/literals.html)

Usage::

    ```python
    from mypy_boto3_ds.literals import CertificateStateType

    data: CertificateStateType = "Deregistered"
    ```
"""
import sys

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = (
    "CertificateStateType",
    "CertificateTypeType",
    "ClientAuthenticationStatusType",
    "ClientAuthenticationTypeType",
    "DescribeDirectoriesPaginatorName",
    "DescribeDomainControllersPaginatorName",
    "DescribeSharedDirectoriesPaginatorName",
    "DescribeSnapshotsPaginatorName",
    "DescribeTrustsPaginatorName",
    "DirectoryEditionType",
    "DirectorySizeType",
    "DirectoryStageType",
    "DirectoryTypeType",
    "DomainControllerStatusType",
    "IpRouteStatusMsgType",
    "LDAPSStatusType",
    "LDAPSTypeType",
    "ListIpRoutesPaginatorName",
    "ListLogSubscriptionsPaginatorName",
    "ListSchemaExtensionsPaginatorName",
    "ListTagsForResourcePaginatorName",
    "RadiusAuthenticationProtocolType",
    "RadiusStatusType",
    "RegionTypeType",
    "ReplicationScopeType",
    "SchemaExtensionStatusType",
    "SelectiveAuthType",
    "ShareMethodType",
    "ShareStatusType",
    "SnapshotStatusType",
    "SnapshotTypeType",
    "TargetTypeType",
    "TopicStatusType",
    "TrustDirectionType",
    "TrustStateType",
    "TrustTypeType",
    "ServiceName",
    "PaginatorName",
)


CertificateStateType = Literal[
    "DeregisterFailed",
    "Deregistered",
    "Deregistering",
    "RegisterFailed",
    "Registered",
    "Registering",
]
CertificateTypeType = Literal["ClientCertAuth", "ClientLDAPS"]
ClientAuthenticationStatusType = Literal["Disabled", "Enabled"]
ClientAuthenticationTypeType = Literal["SmartCard"]
DescribeDirectoriesPaginatorName = Literal["describe_directories"]
DescribeDomainControllersPaginatorName = Literal["describe_domain_controllers"]
DescribeSharedDirectoriesPaginatorName = Literal["describe_shared_directories"]
DescribeSnapshotsPaginatorName = Literal["describe_snapshots"]
DescribeTrustsPaginatorName = Literal["describe_trusts"]
DirectoryEditionType = Literal["Enterprise", "Standard"]
DirectorySizeType = Literal["Large", "Small"]
DirectoryStageType = Literal[
    "Active",
    "Created",
    "Creating",
    "Deleted",
    "Deleting",
    "Failed",
    "Impaired",
    "Inoperable",
    "Requested",
    "RestoreFailed",
    "Restoring",
]
DirectoryTypeType = Literal["ADConnector", "MicrosoftAD", "SharedMicrosoftAD", "SimpleAD"]
DomainControllerStatusType = Literal[
    "Active", "Creating", "Deleted", "Deleting", "Failed", "Impaired", "Restoring"
]
IpRouteStatusMsgType = Literal[
    "AddFailed", "Added", "Adding", "RemoveFailed", "Removed", "Removing"
]
LDAPSStatusType = Literal["Disabled", "EnableFailed", "Enabled", "Enabling"]
LDAPSTypeType = Literal["Client"]
ListIpRoutesPaginatorName = Literal["list_ip_routes"]
ListLogSubscriptionsPaginatorName = Literal["list_log_subscriptions"]
ListSchemaExtensionsPaginatorName = Literal["list_schema_extensions"]
ListTagsForResourcePaginatorName = Literal["list_tags_for_resource"]
RadiusAuthenticationProtocolType = Literal["CHAP", "MS-CHAPv1", "MS-CHAPv2", "PAP"]
RadiusStatusType = Literal["Completed", "Creating", "Failed"]
RegionTypeType = Literal["Additional", "Primary"]
ReplicationScopeType = Literal["Domain"]
SchemaExtensionStatusType = Literal[
    "CancelInProgress",
    "Cancelled",
    "Completed",
    "CreatingSnapshot",
    "Failed",
    "Initializing",
    "Replicating",
    "RollbackInProgress",
    "UpdatingSchema",
]
SelectiveAuthType = Literal["Disabled", "Enabled"]
ShareMethodType = Literal["HANDSHAKE", "ORGANIZATIONS"]
ShareStatusType = Literal[
    "Deleted",
    "Deleting",
    "PendingAcceptance",
    "RejectFailed",
    "Rejected",
    "Rejecting",
    "ShareFailed",
    "Shared",
    "Sharing",
]
SnapshotStatusType = Literal["Completed", "Creating", "Failed"]
SnapshotTypeType = Literal["Auto", "Manual"]
TargetTypeType = Literal["ACCOUNT"]
TopicStatusType = Literal["Deleted", "Failed", "Registered", "Topic not found"]
TrustDirectionType = Literal["One-Way: Incoming", "One-Way: Outgoing", "Two-Way"]
TrustStateType = Literal[
    "Created",
    "Creating",
    "Deleted",
    "Deleting",
    "Failed",
    "UpdateFailed",
    "Updated",
    "Updating",
    "Verified",
    "VerifyFailed",
    "Verifying",
]
TrustTypeType = Literal["External", "Forest"]
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
    "describe_directories",
    "describe_domain_controllers",
    "describe_shared_directories",
    "describe_snapshots",
    "describe_trusts",
    "list_ip_routes",
    "list_log_subscriptions",
    "list_schema_extensions",
    "list_tags_for_resource",
]
