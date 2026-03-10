from datetime import datetime
from services.dataworks_client import DataWorksClient
from services.gsheet_manager import GoogleSheetManager
from core.notifier import NotificationManager
from utils.constants import GSHEET_STATUS
from models.node import Node
from models.instance import Instance


class SLAMonitor:

    def __init__(self):
        self.dataworks = DataWorksClient()
        self.sheet = GoogleSheetManager()
        self.notifier = NotificationManager()

    def update_sheet_status(self):
        print(f"Updating sheet status at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        nodes: list[Node] = self.sheet.get_nodes()
        instance_data_list = []         # for single-instance nodes (update by node_id)
        hourly_instance_data_list = []  # for multi-instance nodes (update by task_name)

        for node in nodes:
            
            if not node.project_id and not node.node_id:
                continue
            
            instances: list[Instance] = self.dataworks.get_instances(node.project_id, node.node_id)
            # print(f"Node: {node.node_name} (ID: {node.node_id}) - Found {len(instances)} instances")
            if not instances:
                continue
            
            if node.is_hourly:
                
                def parse_time_or_max(time_str):
                    if time_str == "-" or not time_str:
                        # return a very large datetime so it goes to the end
                        return datetime.max
                    return datetime.strptime(time_str, "%Y/%m/%d %H:%M")

                # Sort instances
                instances = sorted(instances, key=lambda x: parse_time_or_max(x.start_time))
                
                for idx, inst in enumerate(instances):
                    if not inst.node_name:
                        inst.node_name = node.node_name or ""
                        continue
                    
                    suffix = f"_{idx:02d}"  # 00, 01, 02 ...
                    hourly_instance_data_list.append({
                        "task_name": f"{inst.node_name}{suffix}",
                        "status": f"Status_{inst.status}",
                        "last_update": inst.end_time
                    })
            else:
                inst = instances[0]
                if not inst.node_id:
                    continue

                instance_data_list.append({
                    "node_id": str(inst.node_id),
                    "task_name": inst.node_name,
                    "status": f"Status_{inst.status}",
                    "last_update": inst.end_time
                })

        if instance_data_list:
            self.sheet.batch_update_status_by_id(instance_data_list)

        if hourly_instance_data_list:
            self.sheet.batch_update_status_by_task_name(hourly_instance_data_list)
    
    def build_table(self, breached_nodes: list[Node]):
        print("Building notification message for nodes...")
        if not breached_nodes:
            return None

        # Calculate dynamic column widths
        max_id_width = max(len(str(n.node_id)) for n in breached_nodes)
        max_name_width = max(len(n.node_name) for n in breached_nodes)
        max_status_width = max(len(n.current_status) for n in breached_nodes)

        # Header
        header = (
            f"{'ID'.ljust(max_id_width)}   "
            f"{'NAME'.ljust(max_name_width)}   "
            f"{'STATUS'.ljust(max_status_width)}"
        )

        rows = [header, "-" * len(header)]

        # Rows for breached nodes only
        for n in breached_nodes:
            row = (
                f"{str(n.node_id).ljust(max_id_width)}   "
                f"{n.node_name.ljust(max_name_width)}   "
                f"{n.current_status.ljust(max_status_width)}"
            )
            rows.append(row)

        table_text = "\n".join(rows)

        # Centered title
        title = f"⚠️ SLA BREACH ALERT - {datetime.now().strftime('%H:%M:%S')} ⚠️"
        table_width = len(header)
        centered_title = title.center(table_width)

        # Footer summary based on ALL nodes
        all_nodes = self.sheet.get_nodes()
        total_nodes = len(all_nodes)
        succeeded_count = sum(1 for n in all_nodes if n.current_status == GSHEET_STATUS.SUCCEEDED.value)
        failed_count = sum(1 for n in breached_nodes if n.current_status == GSHEET_STATUS.FAILED.value)
        not_running_count = sum(1 for n in breached_nodes 
                                if n.current_status not in [GSHEET_STATUS.SUCCEEDED.value, GSHEET_STATUS.FAILED.value])

        succeed_percent = round((succeeded_count / total_nodes) * 100) if total_nodes else 0

        footer_lines = [f"Total breached node/s: {len(breached_nodes)}"]
        if failed_count:
            footer_lines.append(f"Failed: {failed_count}")
        if not_running_count:
            footer_lines.append(f"Not running: {not_running_count}")
        if succeeded_count:
            footer_lines.append(f"Succeeded: {succeeded_count}/{total_nodes} ({succeed_percent}%)")

        footer_text = "\n".join(footer_lines)

        message = "```\n" + centered_title + "\n\n" + table_text + "\n" + "-" * len(header) + "\n" + footer_text + "\n```"

        return message

    def check_sla(self):
        print(f"Checking SLA at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        nodes: list[Node] = self.sheet.get_nodes()
        breaches = []
        now = datetime.now().hour

        for node in nodes:
            status = (node.current_status or "").strip()
            sla = node.sla_limit

            # Include FAILED nodes regardless of SLA
            if status == GSHEET_STATUS.FAILED.value:
                breaches.append(node)


            # Skip nodes with invalid SLA
            if not str(sla).isdigit():
                continue

            sla = int(sla)

            # Check SLA breach for non-failed nodes
            if now >= sla and status and status != GSHEET_STATUS.SUCCEEDED.value:
                breaches.append(node)

        if breaches:
            msg = self.build_table(breaches)
            print("SLA breaches found. Sending notification...")
            print(msg)
            self.notifier.send(msg)
    
    
    