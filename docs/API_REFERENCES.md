# Terraform Cloud API References

This document contains links to all available Terraform Cloud API reference documentation.

## Implementation Status

✅ = Implemented with response filtering optimization  
⏸️ = Not yet implemented  
💰 = Requires paid Terraform Cloud tier

## API Documentation

### Core
- [Overview](https://developer.hashicorp.com/terraform/cloud-docs/api-docs)
- [Changelog](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/changelog)
- [Stability Policy](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/stability-policy)

### APIs
- [✅] [Account](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/account) - User profile and authentication info
- [⏸️] [Agent Pools](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/agents) 💰 - Private agent management
- [⏸️] [Agent Tokens](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/agent-tokens) 💰 - Agent authentication
- [✅] [Applies](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/applies) - Infrastructure apply operations
- [⏸️] [Audit Trails](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/audit-trails) 💰💰💰 - Organization audit logs
- [⏸️] [Audit Trails Tokens](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/audit-trails-tokens) 💰💰💰 - Audit access tokens
- [✅] [Assessment Results](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/assessment-results) 💰💰💰 - Health assessments
- [⏸️] [Change Requests](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/change-requests) 💰💰💰 - Infrastructure change workflows
- [⏸️] [Comments](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/comments) - Run and plan comments
- [⏸️] [Configuration Versions](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/configuration-versions) - Terraform configuration uploads
- [✅] [Cost Estimates](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/cost-estimates) - Infrastructure cost projections
- [ ] [Explorer](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/explorer)
- [ ] [Feature Sets](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/feature-sets) 💰
- [ ] [GitHub App Installations](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/github-app-installations)
- [ ] [Invoices](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/invoices)
- [ ] [IP Ranges](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/ip-ranges)
- [ ] [No-Code Provisioning](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/no-code-provisioning)
- [ ] [Notification Configurations](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/notification-configurations)
- [ ] [OAuth Clients](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/oauth-clients)
- [ ] [OAuth Tokens](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/oauth-tokens)
- [✅] [Organizations](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/organizations) - Organization settings and management
- [⏸️] [Organization Memberships](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/organization-memberships) - User membership management
- [⏸️] [Organization Tags](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/organization-tags) - Organization-wide tagging
- [⏸️] [Organization Tokens](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/organization-tokens) - API token management
- [⏸️] [Plan Exports](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/plan-exports) - Plan data export functionality
- [✅] [Plans](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/plans) - Terraform execution plans
- [ ] [Policies](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/policies) 💰💰
- [ ] [Policy Checks](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/policy-checks) 💰💰
- [ ] [Policy Evaluations](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/policy-evaluations) 💰💰
- [ ] [Policy Sets](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/policy-sets) 💰💰
- [ ] [Policy Set Parameters](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/policy-set-params) 💰💰
- Private Registry
  - [ ] [Modules](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/private-registry/modules)
  - [ ] [Manage Module Versions](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/private-registry/manage-module-versions)
  - [ ] [Providers](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/private-registry/providers)
  - [ ] [Private Provider Versions and Platforms](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/private-registry/provider-versions-platforms)
  - [ ] [GPG Keys](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/private-registry/gpg-keys)
  - [ ] [Tests](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/private-registry/tests)
- [✅] [Projects](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/projects) - Workspace organization and management
- [⏸️] [Project Team Access](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/project-team-access) 💰 - Team permissions for projects
- [⏸️] [Reserved Tag Keys](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/reserved-tag-keys) - System-reserved tag management
- [✅] [Runs](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/run) - Terraform execution runs
- Run Tasks
  - [ ] [Run Tasks](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/run-tasks/run-tasks) 💰💰
  - [ ] [Stages and Results](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/run-tasks/run-task-stages-and-results) 💰💰
  - [ ] [Custom Integration](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/run-tasks/run-tasks-integration) 💰💰
- [ ] [Run Triggers](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/run-triggers)
- [ ] [SSH Keys](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/ssh-keys)
- [✅] [State Versions](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/state-versions) - Terraform state management
- [✅] [State Version Outputs](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/state-version-outputs) - State output values
- [⏸️] [Subscriptions](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/subscriptions) - Billing and subscription management
- [⏸️] [Team Membership](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/team-members) 💰 - Team member management
- [⏸️] [Team Tokens](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/team-tokens) 💰 - Team-level API tokens
- [⏸️] [Teams](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/teams) 💰 - Team management
- [⏸️] [User Tokens](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/user-tokens) - User API token management
- [⏸️] [Users](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/users) - User account management
- [✅] [Variables](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/variables) - Terraform variable management
- [✅] [Variable Sets](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/variable-sets) - Reusable variable collections
- [⏸️] [VCS Events](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/vcs-events) - Version control system events
- [✅] [Workspaces](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/workspaces) 💰 - Terraform workspace management
- [✅] [Workspace-Specific Variables](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/workspace-variables) - Workspace variable management
- [⏸️] [Workspace Team Access](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/team-access) 💰 - Team permissions for workspaces
- [⏸️] [Workspace Resources](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/workspace-resources) - Resource tracking and management