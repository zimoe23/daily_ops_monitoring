from enum import Enum

class GSHEET_STATUS(Enum):
    SUCCEEDED = "Status_SUCCESS"
    RUNNING = "Status_RUNNING"
    NO_RUNNING = "Status_NOT_RUN"
    WAITING = "Status_WAIT_TIME"
    FAILED = "Status_FAILURE"
    
class GSHEET_HEADER(Enum):
    NODE_ID = "node_id"
    PROJECT_ID = "project_id"
    PROJECT_NAME = "Project Name"
    PROJECT_DEPENDENCIES = "Project_dependencies"
    WORKFLOW_NAME = "workflow name"
    TASK_NAME = "Task Name"
    NODE_TYPE = "Node Type"
    DATE_ADDED = "Date Added"
    ACTIVE_ISSUE = "Active Issue"
    SLA = "SLA"
    SLA_SCHEDULE = "SLA/Schedule"
    STATUS = "status"
    LAST_UPDATE = "last_update"