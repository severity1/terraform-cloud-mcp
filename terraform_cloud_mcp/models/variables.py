"""Variable models for Terraform Cloud API

This module contains models for Terraform Cloud variable-related requests,
including workspace variables and variable sets.

Reference:
- https://developer.hashicorp.com/terraform/cloud-docs/api-docs/workspace-variables
- https://developer.hashicorp.com/terraform/cloud-docs/api-docs/variable-sets
"""

from enum import Enum
from typing import List, Optional

from pydantic import Field

from .base import APIRequest


class VariableCategory(str, Enum):
    """Variable category options for workspace variables.

    Defines the type of variable:
    - TERRAFORM: Terraform input variables available in configuration
    - ENV: Environment variables available during plan/apply operations

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/workspace-variables

    See:
        docs/models/variables.md for reference
    """

    TERRAFORM = "terraform"
    ENV = "env"


class WorkspaceVariable(APIRequest):
    """Model for workspace variable data.

    Represents a variable that can be set on a workspace, including
    Terraform input variables and environment variables.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/workspace-variables

    See:
        docs/models/variables.md for reference
    """

    key: str = Field(
        ...,
        description="Variable name/key",
        min_length=1,
        max_length=255,
    )
    value: Optional[str] = Field(
        None,
        description="Variable value",
        max_length=256000,
    )
    description: Optional[str] = Field(
        None,
        description="Description of the variable",
        max_length=512,
    )
    category: VariableCategory = Field(
        ...,
        description="Variable category (terraform or env)",
    )
    hcl: Optional[bool] = Field(
        False,
        description="Whether the value is HCL code (only valid for terraform variables)",
    )
    sensitive: Optional[bool] = Field(
        False,
        description="Whether the variable value is sensitive",
    )


class WorkspaceVariableParams(APIRequest):
    """Parameters for workspace variable operations without routing fields.

    This model provides all optional parameters for creating or updating workspace
    variables, separating configuration parameters from routing information like
    workspace ID and variable ID.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/workspace-variables

    See:
        docs/models/variables.md for reference
    """

    key: Optional[str] = Field(
        None,
        description="Variable name/key",
        min_length=1,
        max_length=255,
    )
    value: Optional[str] = Field(
        None,
        description="Variable value",
        max_length=256000,
    )
    description: Optional[str] = Field(
        None,
        description="Description of the variable",
        max_length=512,
    )
    category: Optional[VariableCategory] = Field(
        None,
        description="Variable category (terraform or env)",
    )
    hcl: Optional[bool] = Field(
        None,
        description="Whether the value is HCL code (only valid for terraform variables)",
    )
    sensitive: Optional[bool] = Field(
        None,
        description="Whether the variable value is sensitive",
    )


class WorkspaceVariableCreateRequest(APIRequest):
    """Request model for creating workspace variables.

    Used for POST /workspaces/:workspace_id/vars endpoint.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/workspace-variables

    See:
        docs/models/variables.md for reference
    """

    workspace_id: str = Field(
        ...,
        description="The workspace ID",
        pattern=r"^ws-[a-zA-Z0-9]{16}$",
    )
    key: str = Field(
        ...,
        description="Variable name/key",
        min_length=1,
        max_length=255,
    )
    category: VariableCategory = Field(
        ...,
        description="Variable category (terraform or env)",
    )
    params: Optional[WorkspaceVariableParams] = Field(
        None,
        description="Additional variable parameters",
    )


class WorkspaceVariableUpdateRequest(APIRequest):
    """Request model for updating workspace variables.

    Used for PATCH /workspaces/:workspace_id/vars/:variable_id endpoint.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/workspace-variables

    See:
        docs/models/variables.md for reference
    """

    workspace_id: str = Field(
        ...,
        description="The workspace ID",
        pattern=r"^ws-[a-zA-Z0-9]{16}$",
    )
    variable_id: str = Field(
        ...,
        description="The variable ID",
        pattern=r"^var-[a-zA-Z0-9]{16}$",
    )
    params: Optional[WorkspaceVariableParams] = Field(
        None,
        description="Variable parameters to update",
    )


# Variable Sets Models


class VariableSet(APIRequest):
    """Model for variable set data.

    Represents a collection of variables that can be applied to multiple
    workspaces or projects.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/variable-sets

    See:
        docs/models/variables.md for reference
    """

    name: str = Field(
        ...,
        description="Variable set name",
        min_length=1,
        max_length=90,
    )
    description: Optional[str] = Field(
        None,
        description="Description of the variable set",
        max_length=512,
    )
    global_: Optional[bool] = Field(
        False,
        alias="global",
        description="Whether this is a global variable set",
    )
    priority: Optional[bool] = Field(
        False,
        description="Whether this variable set takes priority over workspace variables",
    )


class VariableSetParams(APIRequest):
    """Parameters for variable set operations without routing fields.

    This model provides all optional parameters for creating or updating variable
    sets, separating configuration parameters from routing information.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/variable-sets

    See:
        docs/models/variables.md for reference
    """

    name: Optional[str] = Field(
        None,
        description="Variable set name",
        min_length=1,
        max_length=90,
    )
    description: Optional[str] = Field(
        None,
        description="Description of the variable set",
        max_length=512,
    )
    global_: Optional[bool] = Field(
        None,
        alias="global",
        description="Whether this is a global variable set",
    )
    priority: Optional[bool] = Field(
        None,
        description="Whether this variable set takes priority over workspace variables",
    )


class VariableSetCreateRequest(APIRequest):
    """Request model for creating variable sets.

    Used for POST /organizations/:organization/varsets endpoint.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/variable-sets

    See:
        docs/models/variables.md for reference
    """

    organization: str = Field(
        ...,
        description="The organization name",
        min_length=1,
    )
    name: str = Field(
        ...,
        description="Variable set name",
        min_length=1,
        max_length=90,
    )
    params: Optional[VariableSetParams] = Field(
        None,
        description="Additional variable set parameters",
    )


class VariableSetUpdateRequest(APIRequest):
    """Request model for updating variable sets.

    Used for PATCH /varsets/:varset_id endpoint.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/variable-sets

    See:
        docs/models/variables.md for reference
    """

    varset_id: str = Field(
        ...,
        description="The variable set ID",
        pattern=r"^varset-[a-zA-Z0-9]{16}$",
    )
    params: Optional[VariableSetParams] = Field(
        None,
        description="Variable set parameters to update",
    )


class VariableSetVariable(APIRequest):
    """Model for variables within a variable set.

    Represents a variable that belongs to a variable set with the same
    structure as workspace variables.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/variable-sets

    See:
        docs/models/variables.md for reference
    """

    key: str = Field(
        ...,
        description="Variable name/key",
        min_length=1,
        max_length=255,
    )
    value: Optional[str] = Field(
        None,
        description="Variable value",
        max_length=256000,
    )
    description: Optional[str] = Field(
        None,
        description="Description of the variable",
        max_length=512,
    )
    category: VariableCategory = Field(
        ...,
        description="Variable category (terraform or env)",
    )
    hcl: Optional[bool] = Field(
        False,
        description="Whether the value is HCL code (only valid for terraform variables)",
    )
    sensitive: Optional[bool] = Field(
        False,
        description="Whether the variable value is sensitive",
    )


class VariableSetAssignmentRequest(APIRequest):
    """Request model for assigning variable sets to workspaces or projects.

    Used for POST /varsets/:varset_id/relationships/workspaces or projects endpoints.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/variable-sets

    See:
        docs/models/variables.md for reference
    """

    varset_id: str = Field(
        ...,
        description="The variable set ID",
        pattern=r"^varset-[a-zA-Z0-9]{16}$",
    )
    workspace_ids: Optional[List[str]] = Field(
        None,
        description="List of workspace IDs to assign the variable set to",
    )
    project_ids: Optional[List[str]] = Field(
        None,
        description="List of project IDs to assign the variable set to",
    )


# Variable Set Variables Models


class VariableSetVariableParams(APIRequest):
    """Parameters for variable set variable operations without routing fields.

    This model provides all optional parameters for creating or updating variables
    within variable sets, separating configuration parameters from routing information
    like variable set ID and variable ID.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/variable-sets

    See:
        docs/models/variables.md for reference
    """

    key: Optional[str] = Field(
        None,
        description="Variable name/key",
        min_length=1,
        max_length=255,
    )
    value: Optional[str] = Field(
        None,
        description="Variable value",
        max_length=256000,
    )
    description: Optional[str] = Field(
        None,
        description="Description of the variable",
        max_length=512,
    )
    category: Optional[VariableCategory] = Field(
        None,
        description="Variable category (terraform or env)",
    )
    hcl: Optional[bool] = Field(
        None,
        description="Whether the value is HCL code (only valid for terraform variables)",
    )
    sensitive: Optional[bool] = Field(
        None,
        description="Whether the variable value is sensitive",
    )
