import pandas as pd
import random

# Define possible values for the knowledge base
incident_states = ["New", "In Progress", "On Hold", "Resolved", "Closed"]
short_descriptions = [
    "Unable to access the platform dashboard",
    "API returning 500 Internal Server Error",
    "Database connection timeout",
    "User account locked due to multiple failed login attempts",
    "High memory usage on the application server",
    "File upload feature not working",
    "Email notifications are not being sent",
    "Service is unavailable for certain regions",
    "Slow response times for API requests",
    "Error while generating reports",
    "Unable to reset user password",
    "Integration with third-party service is failing",
    "Application crashes when uploading large files",
    "Scheduled jobs are not running as expected",
    "Permission denied error for certain users",
    "Data synchronization between services is delayed",
    "Session timeout occurs too quickly",
    "Unable to create new user accounts",
    "Search functionality is not returning results",
    "Unexpected logout from the platform"
]
resolutions = [
    "Restarted the affected service and monitored for stability.",
    "Increased database connection pool size to handle more requests.",
    "Unlocked the user's account and provided instructions to reset the password.",
    "Optimized server configuration to reduce memory usage.",
    "Fixed a bug in the file upload module.",
    "Updated email server configuration to resolve the issue.",
    "Deployed a patch to fix the service availability issue.",
    "Improved API response times by optimizing database queries.",
    "Resolved the error by updating the report generation logic.",
    "Provided the user with a temporary password and instructions to reset it.",
    "Fixed the integration issue by updating API keys.",
    "Resolved the crash by increasing the file size limit.",
    "Reconfigured scheduled jobs to run at the correct intervals.",
    "Updated user permissions to resolve the access issue.",
    "Fixed the data synchronization delay by optimizing the sync process.",
    "Increased session timeout duration as per user feedback.",
    "Resolved the issue by fixing a bug in the user creation workflow.",
    "Fixed the search functionality by reindexing the database.",
    "Resolved the unexpected logout issue by fixing session handling logic."
]

# Generate 100 records
data = []
for i in range(1, 101):
    incident_number = f"INC{i:07d}"  # Format as INC0000001, INC0000002, etc.
    incident_state = random.choice(incident_states)
    short_description = random.choice(short_descriptions)
    resolution = random.choice(resolutions)
    combined_text = f"{incident_state} {short_description} {resolution}"
    data.append([incident_number, incident_state, short_description, resolution, combined_text])

# Create a DataFrame
columns = ["incident_number", "incident_state", "short_description", "resolution", "combined_text"]
knowledge_base = pd.DataFrame(data, columns=columns)

# Save to CSV
csv_file_path = "service_now_knowledge_base.csv"
knowledge_base.to_csv(csv_file_path, index=False)

print(f"Knowledge base with 100 records has been generated and saved as '{csv_file_path}'.")