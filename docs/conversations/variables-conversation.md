# Variables Management - Example Conversations

This document shows example conversations with Claude using the Terraform Cloud MCP variable management features.

## Setting Up Workspace Variables

```
User: I need to set up variables for my new web-app workspace. Can you first show me what variables already exist, then help me add some basic ones?

Claude: I'll check the existing variables in your web-app workspace and then help you add the ones you need.

[Claude uses list_workspace_variables tool]

I can see your workspace currently has no variables configured. Let me help you set up some common variables for a web application.

First, I'll add a Terraform variable for the environment:

[Claude uses create_workspace_variable tool]

I've created a Terraform variable called "environment" with the value "development" to help with resource naming.

Now let me add an environment variable for the application port:

[Claude uses create_workspace_variable tool]

I've added an environment variable "APP_PORT" set to "3000" for your application.

Finally, let me add a sensitive variable for database credentials:

[Claude uses create_workspace_variable tool]

I've created a sensitive environment variable "DB_PASSWORD" for your database connection. The value is hidden for security.

Your workspace now has three variables configured:
- **environment** (terraform): "development" - Used for resource naming
- **APP_PORT** (env): "3000" - Application port number  
- **DB_PASSWORD** (env): [hidden] - Database password (sensitive)

User: I need to update the environment variable from "development" to "staging" and make the database password more secure.

Claude: I'll help you update both of those variables. Let me modify the environment variable first, then update the database password.

[Claude uses update_workspace_variable tool]

I've updated the environment variable from "development" to "staging" and updated the description to reflect the change.

[Claude uses update_workspace_variable tool]

I've also updated the database password with a more secure value while keeping it marked as sensitive.

Both variables have been successfully updated:
- **environment**: Now set to "staging"
- **DB_PASSWORD**: Updated with a stronger password (value remains hidden)
```

## Variable Sets Management

```
User: I want to create a variable set for AWS configuration that I can share across multiple workspaces. It should include region, instance type, and some common tags.

Claude: I'll help you create an AWS configuration variable set that can be shared across your workspaces. This will ensure consistent configuration across your infrastructure.

[Claude uses create_variable_set tool]

I've created a variable set called "aws-common-config" with priority enabled, which means these variables will override any workspace-level variables with the same names.

Now let me add the AWS configuration variables to this set:

[Claude uses create_variable_in_variable_set tool]

I've added the AWS region variable set to "us-west-2".

[Claude uses create_variable_in_variable_set tool]

I've added the default instance type as "t3.micro".

[Claude uses create_variable_in_variable_set tool]

I've added common tags as an HCL variable that includes Environment, ManagedBy, and Team tags.

Your AWS configuration variable set is now ready with:
- **aws_region**: "us-west-2"
- **instance_type**: "t3.micro"  
- **common_tags**: HCL object with Environment, ManagedBy, and Team tags

Since this variable set has priority enabled, these variables will take precedence over any workspace-level variables with the same names.

User: I want to assign the AWS variable set to my web-app and api-service workspaces, and also assign it to my entire "production" project.

Claude: I'll assign the AWS configuration variable set to both your specific workspaces and the entire production project. This will ensure consistent AWS configuration across your infrastructure.

[Claude uses assign_variable_set_to_workspaces tool]

I've assigned the AWS variable set to your web-app and api-service workspaces.

[Claude uses assign_variable_set_to_projects tool]

I've also assigned the variable set to your entire production project.

The AWS configuration variable set is now active in:
- **web-app** and **api-service** workspaces directly
- All workspaces within the **production** project

Any new workspaces added to the production project will automatically inherit these AWS variables.
```

## Managing Sensitive Variables

```
User: I need to add some API keys and database credentials to my workspace. How should I handle these sensitive values?

Claude: For sensitive data like API keys and credentials, I'll make sure to mark them as sensitive so their values are hidden in the UI and API responses. This is crucial for security.

Let me add these sensitive variables for you:

[Claude uses create_workspace_variable tool]

I've added your Stripe API secret key as a sensitive environment variable. The value is now hidden from the UI and logs.

[Claude uses create_workspace_variable tool]

I've added the database connection string as a sensitive environment variable as well.

[Claude uses create_workspace_variable tool]

I've also added your OAuth client secret as a sensitive environment variable.

All three sensitive variables have been created:
- **STRIPE_SECRET_KEY** (env, sensitive): Your payment processing key
- **DATABASE_URL** (env, sensitive): Database connection string  
- **OAUTH_CLIENT_SECRET** (env, sensitive): OAuth application secret

These values are now secured and won't be visible in the Terraform Cloud UI or appear in logs. They'll only be available to your Terraform runs as environment variables.

User: How can I see what variables are available across all my variable sets?

Claude: I'll help you get an overview of your variable sets and their contents. Let me start by listing all your variable sets.

[Claude uses list_variable_sets tool]

You have several variable sets configured:

1. **aws-common-config** - Common AWS configuration (priority enabled)
2. **production-secrets** - Production environment secrets (priority enabled)  
3. **development-config** - Development environment variables (global)

Let me show you what variables are in each set:

[Claude uses list_variables_in_variable_set tool]

**aws-common-config** contains:
- aws_region: "us-west-2"
- instance_type: "t3.micro"
- common_tags: HCL object with standard tags

[Claude uses list_variables_in_variable_set tool]

**production-secrets** contains:
- DATABASE_URL: [sensitive] - Production database connection
- API_KEY: [sensitive] - Production API key
- REDIS_URL: [sensitive] - Redis connection string

[Claude uses list_variables_in_variable_set tool]

**development-config** contains:
- DEBUG_MODE: "true"
- LOG_LEVEL: "debug"
- MOCK_SERVICES: "true"

This gives you a complete view of your variable organization across different environments and purposes.
```

## Variable Set Organization Strategy

```
User: What's the best way to organize variables for development, staging, and production environments?

Claude: Let me show you an effective variable organization strategy and help you see how your current setup compares to best practices.

[Claude uses list_variable_sets tool]

Looking at your current variable sets, I can recommend an organization strategy that follows best practices:

**Environment-specific variable sets:**
- Create separate variable sets for each environment (dev, staging, prod)
- Use `global=false` and assign to specific projects/workspaces
- Include environment-specific values like database URLs, API endpoints

**Common configuration variable sets:**
- Shared provider configuration (like your AWS set)
- Common tags and naming conventions  
- Use `priority=true` to ensure consistency

**Application-specific variables:**
- Keep at workspace level for unique configurations
- Use for application-specific secrets and settings

Based on your current setup, you're already following good practices with your "aws-common-config" set. Here's what I'd recommend:

1. **Keep your AWS common config** - It's well structured with priority enabled
2. **Create environment-specific sets** - Separate sets for dev/staging/prod environments
3. **Use project assignments** - Assign environment sets to corresponding projects
4. **Workspace-level for unique values** - Keep application-specific variables at workspace level

This approach provides:
- Clear separation of concerns
- Easy environment promotion  
- Consistent infrastructure configuration
- Secure handling of sensitive data

Would you like me to help you implement any of these organizational improvements?
```

## Variable Cleanup and Maintenance

```
User: I need to clean up some old variables from my AWS variable set and remove a deprecated variable set entirely.

Claude: I'll help you clean up those unused variables and remove the deprecated variable set. Since these are delete operations, they'll permanently remove the data.

Let me start by removing the unused variable from your AWS variable set:

[Claude uses delete_variable_from_variable_set tool]

I've removed the old variable from your AWS variable set. The variable is now gone from all workspaces that use this variable set.

Now let me remove the deprecated variable set entirely:

[Claude uses delete_variable_set tool]

The deprecated variable set has been completely removed. This action:
- Deleted all variables within the set
- Unassigned it from all workspaces and projects  
- Cannot be undone

Your variable management is now cleaned up:
- Unused variable removed from AWS configuration set
- Deprecated variable set completely deleted
- All affected workspaces updated automatically

The cleanup is complete and your variable organization is now more streamlined.
```