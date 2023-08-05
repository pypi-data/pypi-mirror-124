import click

from sym.flow.cli.commands.services.click.external_id_option import ExternalIdOption
from sym.flow.cli.commands.services.click.service_type_option import ServiceTypeOption
from sym.flow.cli.commands.services.hooks.slack_delete import slack_delete
from sym.flow.cli.errors import ReferencedObjectError
from sym.flow.cli.helpers.api import SymAPI
from sym.flow.cli.helpers.global_options import GlobalOptions
from sym.flow.cli.helpers.utils import filter_dict
from sym.flow.cli.models.service import Service
from sym.flow.cli.models.service_type import ServiceType


def pre_service_delete_hooks(options: GlobalOptions, service: Service) -> None:
    """Registered hooks to call after before deletion of services"""

    if service.service_type == ServiceType.SLACK.type_name:
        slack_delete(options.api_url, service.id)


@click.command(name="delete", short_help="Delete an existing service")
@click.make_pass_decorator(GlobalOptions, ensure=True)
@click.option(
    "--service-type",
    help="The service to delete",
    prompt=True,
    required=True,
    cls=ServiceTypeOption,
)
@click.option(
    "--external-id",
    help="The identifier for the service",
    prompt=True,
    required=True,
    cls=ExternalIdOption,
)
def services_delete(
    options: GlobalOptions, service_type: ServiceType, external_id: str
) -> None:
    """Set up a new service for your organization."""

    api = SymAPI(url=options.api_url)
    service = api.get_service(service_type.type_name, external_id)

    active_references = filter_dict(
        api.get_service_references(service.id), lambda refs: len(refs) > 0
    )
    if active_references:
        raise ReferencedObjectError(active_references)

    pre_service_delete_hooks(options, service)
    api.delete_service(service_type, external_id)
    click.secho(
        f"Successfully deleted service type {service_type.type_name} with external ID {external_id}!",
        fg="green",
    )
