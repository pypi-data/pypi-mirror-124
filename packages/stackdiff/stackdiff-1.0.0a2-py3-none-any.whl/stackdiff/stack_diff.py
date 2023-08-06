from functools import cached_property
from typing import IO, Optional

from ansiscape import green, heavy, yellow
from boto3.session import Session
from differently import render
from tabulate import tabulate


class StackDiff:
    """
    Visualises the changes described by an Amazon Web Services CloudFormation
    change set.

    Arguments:
        change:  ARN, ID or name of the CloudFormation change set to visualise
        session: boto3 session (defaults to a new session)
        stack:   ARN, ID or name of the change set's CloudFormation stack
    """

    def __init__(
        self,
        change: str,
        stack: str,
        session: Optional[Session] = None,
    ) -> None:

        session = session or Session()

        self.change = change
        self.client = session.client(
            "cloudformation"
        )  # pyright: reportUnknownMemberType=false
        self.stack = stack

    @cached_property
    def change_template(self) -> str:
        response = self.client.get_template(
            ChangeSetName=self.change,
            StackName=self.stack,
            TemplateStage="Original",
        )
        return response.get("TemplateBody", "")

    def render_changes(self, writer: IO[str]) -> None:
        """Renders a visualisation of the changes to `writer`."""

        response = self.client.describe_change_set(
            ChangeSetName=self.change,
            StackName=self.stack,
        )

        rows = [
            [
                heavy("Logical ID").encoded,
                heavy("Physical ID").encoded,
                heavy("Resource Type").encoded,
                heavy("Action").encoded,
            ]
        ]

        for change in response["Changes"]:
            rc = change.get("ResourceChange", None)
            if not rc:
                continue

            if rc["Action"] == "Add":
                color = green
            else:
                color = yellow

            replacement = rc.get("Replacement", "False").lower()
            will_replace = replacement == "true"

            action: str = rc["Action"]

            if action == "Modify":
                action = "Replace ⚠️" if will_replace else "Update"

            rows.append(
                [
                    color(rc["LogicalResourceId"]).encoded,
                    color(rc["PhysicalResourceId"]).encoded,
                    color(rc["ResourceType"]).encoded,
                    color(action).encoded,
                ]
            )

        t = tabulate(rows, headers="firstrow", tablefmt="plain")

        writer.write("\n" + t + "\n\n")

    def render_differences(self, writer: IO[str]) -> None:
        """Renders a visualisation of the differences to `writer`."""

        render(self.stack_template, self.change_template, writer)

    @cached_property
    def stack_template(self) -> str:
        response = self.client.get_template(
            StackName=self.stack,
            TemplateStage="Original",
        )
        return response.get("TemplateBody", "")
