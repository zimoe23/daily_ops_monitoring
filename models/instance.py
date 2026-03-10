class Instance:
    def __init__(
        self,
        baseline_id,
        bizdate,
        business_id,
        connection,
        create_time,
        create_user,
        cyc_time,
        dag_id,
        dag_type,
        dqc_description,
        error_message,
        instance_id,
        modify_time,
        node_id,
        node_name,
        param_values,
        priority,
        repeatability,
        status,
        task_rerun_time,
        task_type,
        start_time=None,
        end_time=None
    ):
        self.baseline_id = baseline_id
        self.bizdate = bizdate
        self.business_id = business_id
        self.connection = connection
        self.create_time = create_time
        self.create_user = create_user
        self.cyc_time = cyc_time
        self.dag_id = dag_id
        self.dag_type = dag_type
        self.dqc_description = dqc_description
        self.error_message = error_message
        self.instance_id = instance_id
        self.modify_time = modify_time
        self.node_id = str(node_id)
        self.node_name = node_name
        self.param_values = param_values
        self.priority = priority
        self.repeatability = repeatability
        self.status = status
        self.task_rerun_time = task_rerun_time
        self.task_type = task_type
        self.start_time = start_time
        self.end_time = end_time

    def __repr__(self):
        return (
            f"Instance(node_id={self.node_id}, "
            f"node_name={self.node_name}, "
            f"status={self.status}, "
            f"start_time={self.start_time}, "
            f"end_time={self.end_time}, "
            f"error_message={self.error_message})"
        )