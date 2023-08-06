import boto3
import botocore

from ..user_code_launcher import ReconcileUserCodeLauncher


class EcsUserCodeLauncher(ReconcileUserCodeLauncher):
    def __init__(self, cluster, subnets, execution_role_arn, log_group):
        self.ecs = boto3.client("ecs")
        self.logs = boto3.client("logs")
        # TODO: Default to default cluster
        self.cluster = cluster
        # TODO: Default to default networking
        self.subnets = subnets
        # TODO: Create a role if one doesn't exist?
        self.execution_role_arn = execution_role_arn
        # TODO: Create a log group if one doesn't exist?
        self.log_group = log_group
        super(EcsUserCodeLauncher, self).__init__()

    def _add_server(self, location_name, metadata):
        # TODO: Upsert task definitions
        self.ecs.register_task_definition(
            family=location_name,
            requiresCompatibilities=["FARGATE"],
            networkMode="awsvpc",
            containerDefinitions=[
                {
                    "name": "server",
                    "image": metadata.image,
                    "command": ["dagster", "api", "grpc", "-p", "4000", "-h", "0.0.0.0"],
                    "logConfiguration": {
                        "logDriver": "awslogs",
                        "options": {
                            "awslogs-group": self.log_group,
                            "awslogs-region": self.ecs.meta.region_name,
                            "awslogs-stream-prefix": location_name,
                        },
                    },
                },
            ],
            executionRoleArn=self.execution_role_arn,
            # TODO: Configurable
            # https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-cpu-memory-error.html
            cpu="256",
            memory="512",
        )

        self.ecs.create_service(
            cluster=self.cluster,
            serviceName=location_name,
            taskDefinition=location_name,
            desiredCount=1,
            networkConfiguration={
                "awsvpcConfiguration": {
                    "subnets": self.subnets,
                    # TODO: Choose proper public IP strategy:
                    # https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_cannot_pull_image.html
                    "assignPublicIp": "ENABLED",
                },
            },
        )

        self._poll_service_start(location_name)

    def _remove_server(self, location_name, metadata):
        pass

    def _gen_update_server(self, location_name, old_metadata, new_metadata):
        pass

    def get_step_handler(self, _execution_config):
        pass

    def run_launcher(self):
        pass

    def _poll_service_start(self, service_name):
        # Check if we can place a task; this is fairly quick
        # TODO: handle IAM eventual consistency; sometimes the first event will
        # read "ECS was unable to assume the role" but will resolve itself with
        # enough time:
        # https://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_general.html#troubleshoot_general_eventual-consistency
        try:
            self.ecs.get_waiter("services_stable").wait(
                cluster=self.cluster,
                services=[service_name],
                # 2 minute
                WaiterConfig={
                    "Delay": 1,
                    "MaxAttempts": 120,
                },
            )

        except botocore.exceptions.WaiterError:
            service = self.ecs.describe_services(
                cluster=self.cluster,
                services=[service_name],
            ).get("services")[0]

            messages = [event.get("message") for event in service.get("events")]

            # These strings in event messages indicate we couldn't create a task
            # https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-event-messages.html#service-event-messages-list
            failures = ["unable", "unhealthy", "throttled"]
            for message in messages:
                if any(failure in message for failure in failures):
                    # TODO: Custom exception
                    raise Exception(messages)

        self._poll_tasks_start(service_name)

    def _poll_tasks_start(self, service_name):
        # Check if a task can start; this is pretty slow but
        # will return very quickly on the happy path
        # TODO: Can we make it fail faster if it can't pull the image?
        try:
            self.ecs.get_waiter("services_stable").wait(
                cluster=self.cluster,
                services=[service_name],
                # 5 minutes
                WaiterConfig={
                    "Delay": 1,
                    "MaxAttempts": 300,
                },
            )

        except botocore.exceptions.WaiterError:
            task_arns = self.ecs.list_tasks(
                cluster=self.cluster,
                serviceName=service_name,
                desiredStatus="STOPPED",
            ).get("taskArns")
            tasks = self.ecs.describe_tasks(cluster=self.cluster, tasks=task_arns).get("tasks")
            reasons = [task.get("stoppedReason") for task in tasks]
            raise Exception(reasons)

        self._poll_tasks_running(service_name)

    def _poll_tasks_running(self, service_name):
        # Get the list of running tasks:
        task_arns = self.ecs.list_tasks(
            cluster=self.cluster,
            serviceName=service_name,
            desiredStatus="RUNNING",
        ).get("taskArns")

        # Poll to see if they stop:
        # TODO: don't introduce this delay to the happy path
        try:
            self.ecs.get_waiter("tasks_stopped").wait(
                cluster=self.cluster,
                tasks=task_arns,
                # 1 minute
                WaiterConfig={
                    "Delay": 1,
                    "MaxAttempts": 60,
                },
            )

        # If they don't, conclude that they're healthy
        # and return early:
        except botocore.exceptions.WaiterError:
            return

        # If they stop, raise their logs:
        task_arns = self.ecs.list_tasks(
            cluster=self.cluster,
            serviceName=service_name,
            desiredStatus="STOPPED",
        ).get("taskArns")

        raise Exception(self._get_logs(task_arns[0]))

    def _get_logs(self, task_arn):
        task_id = task_arn.split("/")[-1]

        task = self.ecs.describe_tasks(cluster=self.cluster, tasks=[task_arn],).get(
            "tasks"
        )[0]
        task_definition = self.ecs.describe_task_definition(
            taskDefinition=task.get("taskDefinitionArn"),
        ).get("taskDefinition")
        family = task_definition.get("family")

        log_stream = f"{family}/server/{task_id}"

        events = self.logs.get_log_events(
            logGroupName=self.log_group,
            logStreamName=log_stream,
        ).get("events")

        return [event.get("message") for event in events]
