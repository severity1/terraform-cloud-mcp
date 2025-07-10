"""Filter configurations for Terraform Cloud MCP."""

from ..models.filters import FilterConfig, ResourceType


# Audit-safe filter configurations - conservative filtering to preserve compliance data
FILTER_CONFIGS = {
    ResourceType.WORKSPACE: FilterConfig(
        always_remove={
            # Only remove statistical aggregations - not audit-relevant
            "apply-duration-average",
            "plan-duration-average",
            "policy-check-failures",
            "run-failures",
        },
        list_remove={
            # Remove only internal system fields - preserve all user/audit tracking
            "workspace-kpis-runs-count",
            "unarchived-workspace-change-requests-count",
        },
        essential_relationships={
            "organization",
            "project",
            "current-run",
            "current-state-version",
            "current-configuration-version",
        },
    ),
    ResourceType.RUN: FilterConfig(
        # Preserve permissions, actions, source for audit trails
        always_remove=set(),  # Don't filter anything critical
        list_remove=set(),  # Preserve all data for audit context
        essential_relationships={
            "workspace",
            "plan",
            "apply",
            "cost-estimate",
        },
    ),
    ResourceType.ORGANIZATION: FilterConfig(
        always_remove={
            # Remove only internal system flags - preserve auth policy for audits
            "fair-run-queuing-enabled",
            "send-passing-statuses-for-untriggered-speculative-plans",
        },
        # Preserve created-at, trial-expires-at, permissions, saml-enabled, two-factor-conformant
        list_remove=set(),
    ),
    ResourceType.PROJECT: FilterConfig(
        # Preserve created-at, updated-at for audit trails
        list_remove=set(),
        essential_relationships={
            "organization",
        },
    ),
    ResourceType.VARIABLE: FilterConfig(
        # Preserve version-id and created-at for audit/change tracking
        always_remove=set(),
        list_remove=set(),
    ),
    ResourceType.PLAN: FilterConfig(
        # Preserve permissions for audit context
        always_remove=set(),
        read_remove={
            "resource-drift",  # Detailed drift info can be filtered in reads
        },
        list_remove={
            # Only filter detailed execution info in lists - preserve timing for audits
            "execution-details",
        },
        essential_relationships={
            "run",
            "state-versions",
        },
    ),
    ResourceType.APPLY: FilterConfig(
        # Preserve permissions and status-timestamps for audit trails
        always_remove=set(),
        list_remove={
            # Only filter detailed execution info in lists
            "execution-details",
        },
        essential_relationships={
            "run",
            "state-versions",
        },
    ),
    ResourceType.STATE_VERSION: FilterConfig(
        always_remove={
            # Only remove VCS-specific fields that don't impact audit
            "vcs-commit-sha",
            "vcs-commit-url",
        },
        list_remove={
            # Remove only internal hosted URLs - can be derived when needed
            "hosted-state-download-url",
            "hosted-json-state-download-url",
            "hosted-state-upload-url",
        },
        essential_relationships={
            "workspace",
            "run",
            "outputs",
        },
    ),
    ResourceType.COST_ESTIMATE: FilterConfig(
        # Preserve status-timestamps for audit timeline
        always_remove=set(),
        read_remove=set(),  # Preserve error messages for audit context
        list_remove={
            # Only remove detailed resource counts in lists
            "resources-count",
        },
        essential_relationships={
            "run",
        },
    ),
    ResourceType.ASSESSMENT: FilterConfig(
        # Preserve result-count, created-at, updated-at for audit tracking
        always_remove=set(),
        read_remove=set(),  # Preserve log URLs for audit access
        list_remove=set(),
        essential_relationships={
            "workspace",
        },
    ),
    ResourceType.ACCOUNT: FilterConfig(
        always_remove={
            # Remove only personal/UI fields - preserve auth info for audits
            "password",  # Never should be present anyway
            "avatar-url",  # UI-only field
        },
        # Preserve is-sudo, is-site-admin, auth-method, etc. for security audits
        list_remove=set(),
    ),
}

# Path patterns for resource type detection (order matters for specificity)
PATH_PATTERNS = [
    ("state-versions", ResourceType.STATE_VERSION),
    ("state-version-outputs", ResourceType.STATE_VERSION),
    ("assessment-results", ResourceType.ASSESSMENT),
    ("cost-estimates", ResourceType.COST_ESTIMATE),
    ("workspaces", ResourceType.WORKSPACE),
    ("runs", ResourceType.RUN),
    ("organizations", ResourceType.ORGANIZATION),
    ("projects", ResourceType.PROJECT),
    ("plans", ResourceType.PLAN),
    ("applies", ResourceType.APPLY),
    ("vars", ResourceType.VARIABLE),
    ("variables", ResourceType.VARIABLE),
    ("account/details", ResourceType.ACCOUNT),
    ("users", ResourceType.ACCOUNT),
]

# Data type mapping for response-based detection
DATA_TYPE_MAP = {
    "projects": ResourceType.PROJECT,
    "vars": ResourceType.VARIABLE,
    "runs": ResourceType.RUN,
}

# Resource type mapping for consistent filtering
RESOURCE_TYPE_MAP = {
    "workspace": ResourceType.WORKSPACE,
    "workspaces": ResourceType.WORKSPACE,
    "run": ResourceType.RUN,
    "runs": ResourceType.RUN,
    "organization": ResourceType.ORGANIZATION,
    "organizations": ResourceType.ORGANIZATION,
    "project": ResourceType.PROJECT,
    "projects": ResourceType.PROJECT,
    "var": ResourceType.VARIABLE,
    "vars": ResourceType.VARIABLE,
    "plan": ResourceType.PLAN,
    "plans": ResourceType.PLAN,
    "apply": ResourceType.APPLY,
    "applies": ResourceType.APPLY,
    "state-version": ResourceType.STATE_VERSION,
    "state-versions": ResourceType.STATE_VERSION,
    "cost-estimate": ResourceType.COST_ESTIMATE,
    "cost-estimates": ResourceType.COST_ESTIMATE,
    "assessment-result": ResourceType.ASSESSMENT,
    "assessment-results": ResourceType.ASSESSMENT,
    "user": ResourceType.ACCOUNT,
    "users": ResourceType.ACCOUNT,
}
