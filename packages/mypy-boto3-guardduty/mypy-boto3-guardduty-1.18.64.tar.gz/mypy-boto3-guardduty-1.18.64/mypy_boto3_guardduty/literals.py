"""
Type annotations for guardduty service literal definitions.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_guardduty/literals.html)

Usage::

    ```python
    from mypy_boto3_guardduty.literals import AdminStatusType

    data: AdminStatusType = "DISABLE_IN_PROGRESS"
    ```
"""
import sys

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = (
    "AdminStatusType",
    "DataSourceStatusType",
    "DataSourceType",
    "DestinationTypeType",
    "DetectorStatusType",
    "FeedbackType",
    "FilterActionType",
    "FindingPublishingFrequencyType",
    "FindingStatisticTypeType",
    "IpSetFormatType",
    "IpSetStatusType",
    "ListDetectorsPaginatorName",
    "ListFiltersPaginatorName",
    "ListFindingsPaginatorName",
    "ListIPSetsPaginatorName",
    "ListInvitationsPaginatorName",
    "ListMembersPaginatorName",
    "ListOrganizationAdminAccountsPaginatorName",
    "ListThreatIntelSetsPaginatorName",
    "OrderByType",
    "PublishingStatusType",
    "ThreatIntelSetFormatType",
    "ThreatIntelSetStatusType",
    "UsageStatisticTypeType",
    "ServiceName",
    "PaginatorName",
)


AdminStatusType = Literal["DISABLE_IN_PROGRESS", "ENABLED"]
DataSourceStatusType = Literal["DISABLED", "ENABLED"]
DataSourceType = Literal["CLOUD_TRAIL", "DNS_LOGS", "FLOW_LOGS", "S3_LOGS"]
DestinationTypeType = Literal["S3"]
DetectorStatusType = Literal["DISABLED", "ENABLED"]
FeedbackType = Literal["NOT_USEFUL", "USEFUL"]
FilterActionType = Literal["ARCHIVE", "NOOP"]
FindingPublishingFrequencyType = Literal["FIFTEEN_MINUTES", "ONE_HOUR", "SIX_HOURS"]
FindingStatisticTypeType = Literal["COUNT_BY_SEVERITY"]
IpSetFormatType = Literal["ALIEN_VAULT", "FIRE_EYE", "OTX_CSV", "PROOF_POINT", "STIX", "TXT"]
IpSetStatusType = Literal[
    "ACTIVATING", "ACTIVE", "DEACTIVATING", "DELETED", "DELETE_PENDING", "ERROR", "INACTIVE"
]
ListDetectorsPaginatorName = Literal["list_detectors"]
ListFiltersPaginatorName = Literal["list_filters"]
ListFindingsPaginatorName = Literal["list_findings"]
ListIPSetsPaginatorName = Literal["list_ip_sets"]
ListInvitationsPaginatorName = Literal["list_invitations"]
ListMembersPaginatorName = Literal["list_members"]
ListOrganizationAdminAccountsPaginatorName = Literal["list_organization_admin_accounts"]
ListThreatIntelSetsPaginatorName = Literal["list_threat_intel_sets"]
OrderByType = Literal["ASC", "DESC"]
PublishingStatusType = Literal[
    "PENDING_VERIFICATION", "PUBLISHING", "STOPPED", "UNABLE_TO_PUBLISH_FIX_DESTINATION_PROPERTY"
]
ThreatIntelSetFormatType = Literal[
    "ALIEN_VAULT", "FIRE_EYE", "OTX_CSV", "PROOF_POINT", "STIX", "TXT"
]
ThreatIntelSetStatusType = Literal[
    "ACTIVATING", "ACTIVE", "DEACTIVATING", "DELETED", "DELETE_PENDING", "ERROR", "INACTIVE"
]
UsageStatisticTypeType = Literal[
    "SUM_BY_ACCOUNT", "SUM_BY_DATA_SOURCE", "SUM_BY_RESOURCE", "TOP_RESOURCES"
]
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
    "list_detectors",
    "list_filters",
    "list_findings",
    "list_invitations",
    "list_ip_sets",
    "list_members",
    "list_organization_admin_accounts",
    "list_threat_intel_sets",
]
