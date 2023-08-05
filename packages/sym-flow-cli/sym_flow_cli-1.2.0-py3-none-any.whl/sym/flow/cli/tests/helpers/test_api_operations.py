import copy

import pytest

from sym.flow.cli.helpers.api_operations import (
    Operation,
    OperationHelper,
    OperationSets,
    OperationType,
)
from sym.flow.cli.models.user import Identity, User
from sym.flow.cli.tests.factories.users import ServiceFactory, UserFactory


class TestOperationHelper:
    @pytest.fixture
    def user(self):
        user: User = UserFactory.create()
        user.identities.append(
            Identity(
                service=ServiceFactory(slug="google", external_id="symops.io"),
                matcher={"email": "google_user@symops.io"},
            )
        )
        return user

    @pytest.fixture
    def update_user_ops(self, user):
        edited_user = copy.deepcopy(user)

        edited_user.get_identity_from_key("google:symops.io").matcher = {
            "email": "new_google_user@symops.io"
        }

        return [
            Operation(
                operation_type=OperationType.update_user,
                original_value=user,
                new_value=edited_user,
            )
        ]

    @pytest.fixture
    def delete_identities_ops(self, user):
        edited_user = copy.deepcopy(user)

        edited_user.identities = [
            ident
            for ident in edited_user.identities
            if ident.service.service_type != "google"
        ]

        return [
            Operation(
                operation_type=OperationType.delete_identity,
                original_value=user,
                new_value=edited_user,
            )
        ]

    @pytest.fixture
    def delete_user_ops(self, user):
        return [
            Operation(
                operation_type=OperationType.delete_user,
                original_value=user,
            )
        ]

    def test_update_operations(self, update_user_ops):
        operation_helper = OperationHelper(
            api_url="http://fake.symops.com/api/v1",
            operations=OperationSets(update_user_ops=update_user_ops),
        )
        assert len(operation_helper.update_users_payload.get("users")) == 1

        update = [
            ident["matcher"]["email"]
            for ident in operation_helper.update_users_payload["users"][0]["identities"]
            if ident["service_type"] == "google"
        ]
        assert update[0] == "new_google_user@symops.io"

    def test_delete_identity_operations(self, delete_identities_ops):

        operation_helper = OperationHelper(
            api_url="http://fake.symops.com/api/v1",
            operations=OperationSets(delete_identities_ops=delete_identities_ops),
        )
        idents = operation_helper.delete_user_identity_payload.get("identities")
        assert len(idents) == 1
        assert idents[0]["service_type"] == "google"
        assert idents[0]["external_id"] == "symops.io"

    def test_delete_user_ops(self, delete_user_ops):
        operation_helper = OperationHelper(
            api_url="http://fake.symops.com/api/v1",
            operations=OperationSets(delete_user_ops=delete_user_ops),
        )
        idents = operation_helper.delete_users_payload.get("users")
        assert len(idents) == 1
        assert idents[0]["id"] == delete_user_ops[0].original_value.id
