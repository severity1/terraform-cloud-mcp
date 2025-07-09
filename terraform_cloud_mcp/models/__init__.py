"""Data models for Terraform Cloud MCP"""

# Re-export the base models for easier access
from .base import (  # noqa: F401
    BaseModelConfig,
    APIRequest,
    APIResponse,
    ReqT,
    ExecutionMode,
    CollaboratorAuthPolicy,
)

# Import specific models
from .account import AccountDetailsRequest  # noqa: F401
from .applies import (  # noqa: F401
    ApplyStatus,
    ExecutionDetails as ApplyExecutionDetails,
    StatusTimestamps as ApplyStatusTimestamps,
    ApplyRequest,
    ApplyErroredStateRequest,
)
from .cost_estimates import (  # noqa: F401
    CostEstimateStatus,
    StatusTimestamps as CostEstimateStatusTimestamps,
    CostEstimateRequest,
)
from .organizations import (  # noqa: F401
    OrganizationDetailsRequest,
    OrganizationEntitlementsRequest,
    OrganizationDeleteRequest,
    OrganizationListRequest,
    OrganizationCreateRequest,
    OrganizationUpdateRequest,
    OrganizationParams,
)
from .plans import (  # noqa: F401
    PlanStatus,
    ExecutionDetails,
    StatusTimestamps,
    PlanRequest,
    PlanJsonOutputRequest,
    RunPlanJsonOutputRequest,
)
from .projects import (  # noqa: F401
    TagBinding,
    ProjectListRequest,
    BaseProjectRequest,
    ProjectCreateRequest,
    ProjectUpdateRequest,
    ProjectParams,
    ProjectTagBindingRequest,
    WorkspaceMoveRequest,
)
from .state_versions import (  # noqa: F401
    StateVersionStatus,
    StateVersionListRequest,
    StateVersionRequest,
    CurrentStateVersionRequest,
    StateVersionCreateRequest,
    StateVersionParams,
)
from .state_version_outputs import (  # noqa: F401
    StateVersionOutputListRequest,
    StateVersionOutputRequest,
)
from .variables import (  # noqa: F401
    VariableCategory,
    WorkspaceVariable,
    WorkspaceVariableParams,
    WorkspaceVariableCreateRequest,
    WorkspaceVariableUpdateRequest,
    VariableSet,
    VariableSetParams,
    VariableSetCreateRequest,
    VariableSetUpdateRequest,
    VariableSetVariable,
    VariableSetAssignmentRequest,
    VariableSetVariableParams,
)
from .runs import (  # noqa: F401
    RunOperation,
    RunStatus,
    RunSource,
    RunStatusGroup,
    RunVariable,
    RunListInWorkspaceRequest,
    RunListInOrganizationRequest,
    RunCreateRequest,
    RunActionRequest,
    RunParams,
)
from .workspaces import (  # noqa: F401
    VcsRepoConfig,
    WorkspaceListRequest,
    WorkspaceCreateRequest,
    WorkspaceUpdateRequest,
    WorkspaceParams,
)

# Define __all__ to control what's imported with wildcard imports
__all__ = [
    # Base models
    "BaseModelConfig",
    "APIRequest",
    "APIResponse",
    "ReqT",
    # Common enums
    "CollaboratorAuthPolicy",
    "ExecutionMode",
    # Account models
    "AccountDetailsRequest",
    # Apply models
    "ApplyStatus",
    "ApplyExecutionDetails",
    "ApplyStatusTimestamps",
    "ApplyRequest",
    "ApplyErroredStateRequest",
    # Cost estimate models
    "CostEstimateStatus",
    "CostEstimateStatusTimestamps",
    "CostEstimateRequest",
    # Organization models
    "OrganizationDetailsRequest",
    "OrganizationEntitlementsRequest",
    "OrganizationDeleteRequest",
    "OrganizationListRequest",
    "OrganizationCreateRequest",
    "OrganizationUpdateRequest",
    "OrganizationParams",
    # Plan models
    "PlanStatus",
    "ExecutionDetails",
    "StatusTimestamps",
    "PlanRequest",
    "PlanJsonOutputRequest",
    "RunPlanJsonOutputRequest",
    # Project models
    "TagBinding",
    "ProjectListRequest",
    "BaseProjectRequest",
    "ProjectCreateRequest",
    "ProjectUpdateRequest",
    "ProjectParams",
    "ProjectTagBindingRequest",
    "WorkspaceMoveRequest",
    # Run models
    "RunOperation",
    "RunStatus",
    "RunSource",
    "RunStatusGroup",
    "RunVariable",
    "RunListInWorkspaceRequest",
    "RunListInOrganizationRequest",
    "RunCreateRequest",
    "RunActionRequest",
    "RunParams",
    # State Version models
    "StateVersionStatus",
    "StateVersionListRequest",
    "StateVersionRequest",
    "CurrentStateVersionRequest",
    "StateVersionCreateRequest",
    "StateVersionParams",
    # State Version Output models
    "StateVersionOutputListRequest",
    "StateVersionOutputRequest",
    # Variable models
    "VariableCategory",
    "WorkspaceVariable",
    "WorkspaceVariableParams",
    "WorkspaceVariableCreateRequest",
    "WorkspaceVariableUpdateRequest",
    "VariableSet",
    "VariableSetParams",
    "VariableSetCreateRequest",
    "VariableSetUpdateRequest",
    "VariableSetVariable",
    "VariableSetAssignmentRequest",
    "VariableSetVariableParams",
    # Workspace models
    "VcsRepoConfig",
    "WorkspaceListRequest",
    "WorkspaceCreateRequest",
    "WorkspaceUpdateRequest",
    "WorkspaceParams",
]
