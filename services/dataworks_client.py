from datetime import datetime, timedelta
from alibabacloud_dataworks_public20200518.client import Client
from alibabacloud_dataworks_public20200518 import models
from alibabacloud_tea_openapi import models as open_api_models
from config.settings import AK_ID, AK_SECRET, REGION, DAY_BEHIND
from utils.helpers import Helper
from models.instance import Instance

class DataWorksClient:

    def __init__(self):
        config = open_api_models.Config(
            access_key_id=AK_ID,
            access_key_secret=AK_SECRET,
            endpoint=f"dataworks.{REGION}.aliyuncs.com"
        )
        self.client = Client(config)

    # def get_status_name(self, status):

    #     mapping = {
    #         1: "Not Run",
    #         2: "Wait Time",
    #         4: "Running",
    #         5: "Failure",
    #         6: "Success",
    #         7: "Terminated"
    #     }

        # return mapping.get(status, "Unknown")

    def get_instances(self, project_id, node_id) -> list[Instance]:
        results = []

        today = Helper.format_date_yyyymmdd(Helper.get_prev_day(DAY_BEHIND))

        start = f"{today} 00:00:00"
        end = f"{today} 23:59:59"

        request = models.ListInstancesRequest(
            project_id=int(project_id),
            node_id=int(node_id),
            project_env="PROD",
            begin_bizdate=start,
            end_bizdate=end,
            page_size=100
        )

        response = self.client.list_instances(request)

        if response.body.data.instances:
            for inst in response.body.data.instances:
                
                start_time = (
                    datetime.fromtimestamp(inst.begin_running_time / 1000).strftime('%Y/%m/%d %H:%M')
                    if inst.begin_running_time else "-"
                )

                end_time = (
                    datetime.fromtimestamp(inst.finish_time / 1000).strftime('%Y/%m/%d %H:%M')
                    if inst.finish_time else "-"
                )

                instance = Instance(
                    baseline_id=inst.baseline_id,
                    bizdate=inst.bizdate,
                    business_id=inst.business_id,
                    connection=inst.connection,
                    create_time=inst.create_time,
                    create_user=inst.create_user,
                    cyc_time=inst.cyc_time,
                    dag_id=inst.dag_id,
                    dag_type=inst.dag_type,
                    dqc_description=inst.dqc_description,
                    error_message=inst.error_message,
                    instance_id=inst.instance_id,
                    modify_time=inst.modify_time,
                    node_id=inst.node_id,
                    node_name=inst.node_name,
                    param_values=inst.param_values,
                    priority=inst.priority,
                    repeatability=inst.repeatability,
                    status=inst.status,
                    task_rerun_time=inst.task_rerun_time,
                    task_type=inst.task_type,
                    start_time=start_time,
                    end_time=end_time
                )

                results.append(instance)

        return results