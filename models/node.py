class Node:
    def __init__(self, node_id, project_id, node_name, is_hourly, sla_limit, current_status):
        self.node_id = str(node_id)
        self.project_id = str(project_id)
        self.node_name = node_name
        self.is_hourly = is_hourly
        self.sla_limit = str(sla_limit)
        self.current_status = current_status

    def __repr__(self):
        return f"Node(node_id={self.node_id}, project_id={self.project_id}, node_name={self.node_name}, sla_limit={self.sla_limit}, status={self.current_status})"