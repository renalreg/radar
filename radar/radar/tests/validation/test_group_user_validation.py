import pytest

from radar.models.groups import Group, GroupUser
from radar.models.users import User
from radar.roles import ROLE
from radar.validation.group_users import GroupUserValidation
from radar.validation.core import ValidationError
from radar.tests.validation.helpers import validation_runner
from radar.exceptions import PermissionDenied


@pytest.fixture
def group_user():
    obj = GroupUser()
    obj.user = User()
    obj.group = Group()
    obj.role = ROLE.SENIOR_RESEARCHER
    return obj


def test_valid(group_user):
    obj = valid(group_user)
    assert obj.user is not None
    assert obj.group is not None
    assert obj.role == ROLE.SENIOR_RESEARCHER
    assert obj.created_user is not None
    assert obj.created_date is not None
    assert obj.modified_user is not None
    assert obj.modified_date is not None


def test_user_missing(group_user):
    group_user.user = None
    invalid(group_user)


def test_group_missing(group_user):
    group_user.group = None
    invalid(group_user)


def test_role_missing(group_user):
    group_user.role = None
    invalid(group_user)


def test_add_to_group():
    group = Group()

    current_user = User()
    current_user_group_user = GroupUser()
    current_user_group_user.group = group
    current_user_group_user.user = current_user
    current_user_group_user.role = ROLE.SENIOR_RESEARCHER
    current_user.group_users.append(current_user_group_user)

    group_user = GroupUser()
    group_user.group = group
    group_user.user = User()
    group_user.role = ROLE.RESEARCHER

    valid(group_user, user=current_user)


def test_add_to_another_group():
    current_user = User()
    current_user_group_user = GroupUser()
    current_user_group_user.group = Group()
    current_user_group_user.user = current_user
    current_user_group_user.role = ROLE.SENIOR_RESEARCHER
    current_user.group_users.append(current_user_group_user)

    group_user = GroupUser()
    group_user.group = Group()
    group_user.user = User()
    group_user.role = ROLE.RESEARCHER

    with pytest.raises(PermissionDenied):
        valid(group_user, user=current_user)


def test_add_to_group_not_managed_role():
    group = Group()

    current_user = User()
    current_user_group_user = GroupUser()
    current_user_group_user.group = group
    current_user_group_user.user = current_user
    current_user_group_user.role = ROLE.SENIOR_RESEARCHER
    current_user.group_users.append(current_user_group_user)

    group_user = GroupUser()
    group_user.group = group
    group_user.user = User()
    group_user.role = ROLE.SENIOR_RESEARCHER

    with pytest.raises(PermissionDenied):
        valid(group_user, user=current_user)


def test_remove_own_membership():
    current_user = User()

    old_group_user = GroupUser()
    old_group_user.group = Group()
    old_group_user.user = current_user
    old_group_user.role = ROLE.SENIOR_RESEARCHER
    current_user.group_users.append(old_group_user)

    new_group_user = GroupUser()
    new_group_user.group = Group()
    new_group_user.user = User()
    new_group_user.role = ROLE.RESEARCHER

    with pytest.raises(PermissionDenied):
        valid(new_group_user, user=current_user, old_obj=old_group_user)


def test_update_own_membership():
    current_user = User()
    group = Group()

    old_group_user = GroupUser()
    old_group_user.group = group
    old_group_user.user = current_user
    old_group_user.role = ROLE.SENIOR_RESEARCHER

    current_user.group_users.append(old_group_user)

    new_group_user = GroupUser()
    new_group_user.group = group
    new_group_user.user = current_user
    new_group_user.role = ROLE.RESEARCHER

    with pytest.raises(PermissionDenied):
        valid(new_group_user, user=current_user, old_obj=old_group_user)


def test_already_in_group():
    user = User()
    group = Group()

    group_user1 = GroupUser()
    group_user1.user = user
    group_user1.group = group
    group_user1.role = ROLE.RESEARCHER
    user.group_users.append(group_user1)

    group_user2 = GroupUser()
    group_user2.user = user
    group_user2.group = group
    group_user2.role = ROLE.SENIOR_RESEARCHER

    valid(group_user2)


def test_already_in_group_and_role():
    user = User()
    group = Group()

    group_user1 = GroupUser()
    group_user1.user = user
    group_user1.group = group
    group_user1.role = ROLE.RESEARCHER
    user.group_users.append(group_user1)

    group_user2 = GroupUser()
    group_user2.user = user
    group_user2.group = group
    group_user2.role = ROLE.RESEARCHER

    invalid(group_user2)


def invalid(obj, **kwargs):
    with pytest.raises(ValidationError) as e:
        valid(obj, **kwargs)

    return e


def valid(obj, **kwargs):
    return validation_runner(GroupUser, GroupUserValidation, obj, **kwargs)
