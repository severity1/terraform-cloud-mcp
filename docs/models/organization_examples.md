# Organization Model Examples

## Basic Usage

```python
from terraform_cloud_mcp.models.organizations import (
    OrganizationParams,
    CollaboratorAuthPolicy,
    ExecutionMode
)

# Create a basic organization configuration
org_params = OrganizationParams(
    name="my-organization",
    email="admin@example.com"
)

# Set organization with default execution mode
remote_org = OrganizationParams(
    name="remote-execution-org",
    email="admin@example.com",
    default_execution_mode=ExecutionMode.REMOTE
)
```

## Common Patterns

```python
# Configure security settings
secure_org = OrganizationParams(
    name="secure-org",
    email="security@example.com",
    collaborator_auth_policy=CollaboratorAuthPolicy.TWO_FACTOR_MANDATORY,
    session_timeout=60,  # minutes
    session_remember=1440  # minutes (1 day)
)

# Configure cost estimation and assessments
enterprise_org = OrganizationParams(
    name="enterprise-org",
    email="enterprise@example.com",
    cost_estimation_enabled=True,
    assessments_enforced=True
)

# Configure VCS status update settings
vcs_org = OrganizationParams(
    name="vcs-integrated-org",
    email="devops@example.com",
    aggregated_commit_status_enabled=True,
    send_passing_statuses_for_untriggered_speculative_plans=True
)
```

## Advanced Use Cases

```python
# Configure agent-based execution
agent_org = OrganizationParams(
    name="agent-based-org",
    email="ops@example.com",
    default_execution_mode=ExecutionMode.AGENT,
    default_agent_pool_id="apool-1234abcd"
)

# Configure organization with workspace management settings
workspace_management_org = OrganizationParams(
    name="workspace-mgmt-org",
    email="infrastructure@example.com",
    allow_force_delete_workspaces=True,
    speculative_plan_management_enabled=True
)

# Configure SAML integration settings
saml_org = OrganizationParams(
    name="saml-integrated-org",
    email="identity@example.com",
    collaborator_auth_policy=CollaboratorAuthPolicy.TWO_FACTOR_MANDATORY,
    owners_team_saml_role_id="owners"
)
```