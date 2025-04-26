# Project Management Conversation Examples

This document provides example conversations demonstrating how to use the project management tools in the Terraform Cloud MCP.

## Listing Projects in an Organization

```
User: Can you list all projects in my organization jptest-org-1?

Claude: I'll list the projects in that organization for you.

[Tool use: list_projects with organization="jptest-org-1"]

Claude: Here are the projects in jptest-org-1:

1. Development Infrastructure (prj-abc123def456)
   - 5 workspaces
   - Created: 2025-01-15

2. Production Systems (prj-ghi789jkl012)
   - 8 workspaces
   - Created: 2024-12-01

3. CI/CD Pipeline (prj-mno345pqr678)
   - 3 workspaces
   - Created: 2025-02-10

Would you like more details on any specific project?
```

## Getting Project Details

```
User: I'd like to see details for project prj-abc123def456

Claude: I'll retrieve the project details for you.

[Tool use: get_project_details with project_id="prj-abc123def456"]

Claude: Here are the details for project "Development Infrastructure" (prj-abc123def456):

Description: Resources for the development environment
Created: 2025-01-15T09:30:22Z
Last updated: 2025-03-20T14:15:43Z

Tags:
- environment: development
- team: platform
- cost-center: 12345

Contains 5 workspaces:
- dev-networking
- dev-compute
- dev-storage
- dev-databases
- dev-monitoring

No auto-destroy schedules are configured for this project.
```

## Creating a New Project

```
User: I'd like to create a new project called "QA Environment" in organization jptest-org-1

Claude: I'll create that project for you.

[Tool use: create_project with organization="jptest-org-1", name="QA Environment"]

Claude: I've created your new project "QA Environment" in jptest-org-1.

Project ID: prj-stu901vwx234
Created: 2025-04-26T15:45:12Z

The project currently has no workspaces associated with it. Would you like to add any workspaces to this project or configure additional settings like tags?
```

## Creating a Project with Detailed Settings

```
User: Create a project called "Compliance Systems" in jptest-org-1 with a description, environment tag set to "compliance", and configured to auto-destroy resources after 14 days of inactivity

Claude: I'll create that project with your specified settings.

[Tool use: create_project with organization="jptest-org-1", name="Compliance Systems", params={description: "Systems for regulatory compliance", auto_destroy_activity_duration: "14d", tag_bindings: [{key: "environment", value: "compliance"}]}]

Claude: I've created your new project "Compliance Systems" in jptest-org-1.

Project ID: prj-yz1234abcd56
Created: 2025-04-26T15:48:30Z
Description: Systems for regulatory compliance

Tags:
- environment: compliance

Auto-destroy configured: Resources will be destroyed after 14 days of inactivity.

The project is ready for use. Would you like to add any workspaces to it now?
```

## Updating a Project

```
User: I need to update the "Development Infrastructure" project (prj-abc123def456) to change its description and add a new tag

Claude: I'll update that project for you.

[Tool use: update_project with project_id="prj-abc123def456", params={description: "Development environment resources and infrastructure", tag_bindings: [{key: "priority", value: "medium"}]}]

Claude: I've updated the "Development Infrastructure" project (prj-abc123def456).

The description has been changed to "Development environment resources and infrastructure".
Added tag: priority: medium

The project now has the following tags:
- environment: development
- team: platform
- cost-center: 12345
- priority: medium

All other settings remain unchanged.
```

## Viewing Project Tag Bindings

```
User: What tags are applied to the "Production Systems" project (prj-ghi789jkl012)?

Claude: I'll check the tags for that project.

[Tool use: list_project_tag_bindings with project_id="prj-ghi789jkl012"]

Claude: The "Production Systems" project (prj-ghi789jkl012) has the following tags:

- environment: production
- team: platform
- cost-center: 67890
- criticality: high
- compliance: soc2
- backup-policy: daily

These tags are used for organization, filtering, and governance purposes in your Terraform Cloud organization.
```

## Adding Tags to a Project

```
User: I'd like to add two tags to the "CI/CD Pipeline" project (prj-mno345pqr678): category=pipeline and owner=devops-team

Claude: I'll add those tags to the project.

[Tool use: add_update_project_tag_bindings with project_id="prj-mno345pqr678", tag_bindings=[{key: "category", value: "pipeline"}, {key: "owner", value: "devops-team"}]]

Claude: I've added the tags to the "CI/CD Pipeline" project:

Added tags:
- category: pipeline
- owner: devops-team

The project now has a total of 5 tags:
- environment: shared
- team: devops
- category: pipeline
- owner: devops-team
- priority: high
```

## Moving Workspaces to a Project

```
User: I need to move the workspaces "test-network" and "test-compute" (IDs: ws-def456ghi789 and ws-jkl012mno345) to the "QA Environment" project (prj-stu901vwx234)

Claude: I'll move those workspaces to the QA Environment project.

[Tool use: move_workspaces_to_project with project_id="prj-stu901vwx234", workspace_ids=["ws-def456ghi789", "ws-jkl012mno345"]]

Claude: I've successfully moved both workspaces to the "QA Environment" project:

- "test-network" (ws-def456ghi789)
- "test-compute" (ws-jkl012mno345)

These workspaces will now inherit any project-level settings from the QA Environment project, such as tag bindings. The workspaces' individual settings remain unchanged.

The QA Environment project now has 2 workspaces associated with it.
```

## Deleting a Project

```
User: I want to delete the project "Compliance Systems" (prj-yz1234abcd56)

Claude: I'll delete that project for you.

[Tool use: delete_project with project_id="prj-yz1234abcd56"]

Claude: The "Compliance Systems" project (prj-yz1234abcd56) has been successfully deleted.

Note that this only deleted the project itself. Any workspaces that were in this project have been moved back to the organization's default project. No workspaces or infrastructure resources were deleted by this action.
```

## Finding Projects by Search Query

```
User: Can you find all projects in jptest-org-1 that have to do with development?

Claude: I'll search for development-related projects.

[Tool use: list_projects with organization="jptest-org-1", query="development"]

Claude: I found 2 projects related to "development" in jptest-org-1:

1. Development Infrastructure (prj-abc123def456)
   - 5 workspaces
   - Description: Development environment resources and infrastructure
   - Tags: environment:development, team:platform, cost-center:12345, priority:medium

2. API Development (prj-pqr678stu901)
   - 3 workspaces
   - Description: API development and testing
   - Tags: environment:development, team:api, service:rest

Would you like more details about either of these projects?
```

## Handling Project Errors

```
User: Delete project prj-nonexistent123456

Claude: I'll try to delete that project.

[Tool use: delete_project with project_id="prj-nonexistent123456"]

Claude: I wasn't able to delete the project. The system returned an error indicating that project ID "prj-nonexistent123456" doesn't exist.

Would you like me to list the available projects in your organization so you can confirm the correct ID?
```