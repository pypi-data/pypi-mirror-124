"""
Type annotations for codebuild service literal definitions.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_codebuild/literals.html)

Usage::

    ```python
    from mypy_boto3_codebuild.literals import ArtifactNamespaceType

    data: ArtifactNamespaceType = "BUILD_ID"
    ```
"""
import sys

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = (
    "ArtifactNamespaceType",
    "ArtifactPackagingType",
    "ArtifactsTypeType",
    "AuthTypeType",
    "BatchReportModeTypeType",
    "BucketOwnerAccessType",
    "BuildBatchPhaseTypeType",
    "BuildPhaseTypeType",
    "CacheModeType",
    "CacheTypeType",
    "ComputeTypeType",
    "CredentialProviderTypeType",
    "DescribeCodeCoveragesPaginatorName",
    "DescribeTestCasesPaginatorName",
    "EnvironmentTypeType",
    "EnvironmentVariableTypeType",
    "FileSystemTypeType",
    "ImagePullCredentialsTypeType",
    "LanguageTypeType",
    "ListBuildBatchesForProjectPaginatorName",
    "ListBuildBatchesPaginatorName",
    "ListBuildsForProjectPaginatorName",
    "ListBuildsPaginatorName",
    "ListProjectsPaginatorName",
    "ListReportGroupsPaginatorName",
    "ListReportsForReportGroupPaginatorName",
    "ListReportsPaginatorName",
    "ListSharedProjectsPaginatorName",
    "ListSharedReportGroupsPaginatorName",
    "LogsConfigStatusTypeType",
    "PlatformTypeType",
    "ProjectSortByTypeType",
    "ProjectVisibilityTypeType",
    "ReportCodeCoverageSortByTypeType",
    "ReportExportConfigTypeType",
    "ReportGroupSortByTypeType",
    "ReportGroupStatusTypeType",
    "ReportGroupTrendFieldTypeType",
    "ReportPackagingTypeType",
    "ReportStatusTypeType",
    "ReportTypeType",
    "RetryBuildBatchTypeType",
    "ServerTypeType",
    "SharedResourceSortByTypeType",
    "SortOrderTypeType",
    "SourceAuthTypeType",
    "SourceTypeType",
    "StatusTypeType",
    "WebhookBuildTypeType",
    "WebhookFilterTypeType",
    "ServiceName",
    "PaginatorName",
)

ArtifactNamespaceType = Literal["BUILD_ID", "NONE"]
ArtifactPackagingType = Literal["NONE", "ZIP"]
ArtifactsTypeType = Literal["CODEPIPELINE", "NO_ARTIFACTS", "S3"]
AuthTypeType = Literal["BASIC_AUTH", "OAUTH", "PERSONAL_ACCESS_TOKEN"]
BatchReportModeTypeType = Literal["REPORT_AGGREGATED_BATCH", "REPORT_INDIVIDUAL_BUILDS"]
BucketOwnerAccessType = Literal["FULL", "NONE", "READ_ONLY"]
BuildBatchPhaseTypeType = Literal[
    "COMBINE_ARTIFACTS",
    "DOWNLOAD_BATCHSPEC",
    "FAILED",
    "IN_PROGRESS",
    "STOPPED",
    "SUBMITTED",
    "SUCCEEDED",
]
BuildPhaseTypeType = Literal[
    "BUILD",
    "COMPLETED",
    "DOWNLOAD_SOURCE",
    "FINALIZING",
    "INSTALL",
    "POST_BUILD",
    "PRE_BUILD",
    "PROVISIONING",
    "QUEUED",
    "SUBMITTED",
    "UPLOAD_ARTIFACTS",
]
CacheModeType = Literal["LOCAL_CUSTOM_CACHE", "LOCAL_DOCKER_LAYER_CACHE", "LOCAL_SOURCE_CACHE"]
CacheTypeType = Literal["LOCAL", "NO_CACHE", "S3"]
ComputeTypeType = Literal[
    "BUILD_GENERAL1_2XLARGE",
    "BUILD_GENERAL1_LARGE",
    "BUILD_GENERAL1_MEDIUM",
    "BUILD_GENERAL1_SMALL",
]
CredentialProviderTypeType = Literal["SECRETS_MANAGER"]
DescribeCodeCoveragesPaginatorName = Literal["describe_code_coverages"]
DescribeTestCasesPaginatorName = Literal["describe_test_cases"]
EnvironmentTypeType = Literal[
    "ARM_CONTAINER",
    "LINUX_CONTAINER",
    "LINUX_GPU_CONTAINER",
    "WINDOWS_CONTAINER",
    "WINDOWS_SERVER_2019_CONTAINER",
]
EnvironmentVariableTypeType = Literal["PARAMETER_STORE", "PLAINTEXT", "SECRETS_MANAGER"]
FileSystemTypeType = Literal["EFS"]
ImagePullCredentialsTypeType = Literal["CODEBUILD", "SERVICE_ROLE"]
LanguageTypeType = Literal[
    "ANDROID", "BASE", "DOCKER", "DOTNET", "GOLANG", "JAVA", "NODE_JS", "PHP", "PYTHON", "RUBY"
]
ListBuildBatchesForProjectPaginatorName = Literal["list_build_batches_for_project"]
ListBuildBatchesPaginatorName = Literal["list_build_batches"]
ListBuildsForProjectPaginatorName = Literal["list_builds_for_project"]
ListBuildsPaginatorName = Literal["list_builds"]
ListProjectsPaginatorName = Literal["list_projects"]
ListReportGroupsPaginatorName = Literal["list_report_groups"]
ListReportsForReportGroupPaginatorName = Literal["list_reports_for_report_group"]
ListReportsPaginatorName = Literal["list_reports"]
ListSharedProjectsPaginatorName = Literal["list_shared_projects"]
ListSharedReportGroupsPaginatorName = Literal["list_shared_report_groups"]
LogsConfigStatusTypeType = Literal["DISABLED", "ENABLED"]
PlatformTypeType = Literal["AMAZON_LINUX", "DEBIAN", "UBUNTU", "WINDOWS_SERVER"]
ProjectSortByTypeType = Literal["CREATED_TIME", "LAST_MODIFIED_TIME", "NAME"]
ProjectVisibilityTypeType = Literal["PRIVATE", "PUBLIC_READ"]
ReportCodeCoverageSortByTypeType = Literal["FILE_PATH", "LINE_COVERAGE_PERCENTAGE"]
ReportExportConfigTypeType = Literal["NO_EXPORT", "S3"]
ReportGroupSortByTypeType = Literal["CREATED_TIME", "LAST_MODIFIED_TIME", "NAME"]
ReportGroupStatusTypeType = Literal["ACTIVE", "DELETING"]
ReportGroupTrendFieldTypeType = Literal[
    "BRANCHES_COVERED",
    "BRANCHES_MISSED",
    "BRANCH_COVERAGE",
    "DURATION",
    "LINES_COVERED",
    "LINES_MISSED",
    "LINE_COVERAGE",
    "PASS_RATE",
    "TOTAL",
]
ReportPackagingTypeType = Literal["NONE", "ZIP"]
ReportStatusTypeType = Literal["DELETING", "FAILED", "GENERATING", "INCOMPLETE", "SUCCEEDED"]
ReportTypeType = Literal["CODE_COVERAGE", "TEST"]
RetryBuildBatchTypeType = Literal["RETRY_ALL_BUILDS", "RETRY_FAILED_BUILDS"]
ServerTypeType = Literal["BITBUCKET", "GITHUB", "GITHUB_ENTERPRISE"]
SharedResourceSortByTypeType = Literal["ARN", "MODIFIED_TIME"]
SortOrderTypeType = Literal["ASCENDING", "DESCENDING"]
SourceAuthTypeType = Literal["OAUTH"]
SourceTypeType = Literal[
    "BITBUCKET", "CODECOMMIT", "CODEPIPELINE", "GITHUB", "GITHUB_ENTERPRISE", "NO_SOURCE", "S3"
]
StatusTypeType = Literal["FAILED", "FAULT", "IN_PROGRESS", "STOPPED", "SUCCEEDED", "TIMED_OUT"]
WebhookBuildTypeType = Literal["BUILD", "BUILD_BATCH"]
WebhookFilterTypeType = Literal[
    "ACTOR_ACCOUNT_ID", "BASE_REF", "COMMIT_MESSAGE", "EVENT", "FILE_PATH", "HEAD_REF"
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
    "describe_code_coverages",
    "describe_test_cases",
    "list_build_batches",
    "list_build_batches_for_project",
    "list_builds",
    "list_builds_for_project",
    "list_projects",
    "list_report_groups",
    "list_reports",
    "list_reports_for_report_group",
    "list_shared_projects",
    "list_shared_report_groups",
]
