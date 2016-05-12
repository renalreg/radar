import pytest
from cornflake.exceptions import ValidationError

from radar.api.serializers.group_users import GroupUserSerializer
from radar.exceptions import PermissionDenied
from radar.models.groups import Group, GroupUser
from radar.models.users import User
from radar.roles import ROLE


@pytest.fixture
def group_user():
    return {
        'user': User(),
        'group': Group(),
        'role': ROLE.SENIOR_RESEARCHER
    }


def test_valid(group_user):
    obj = valid(data=group_user)
    assert obj.user is not None
    assert obj.group is not None
    assert obj.role == ROLE.SENIOR_RESEARCHER
    assert obj.created_user is not None
    assert obj.created_date is not None
    assert obj.modified_user is not None
    assert obj.modified_date is not None


def test_user_missing(group_user):
    group_user['user'] = None
    invalid(data=group_user)


def test_group_missing(group_user):
    group_user['group'] = None
    invalid(data=group_user)


def test_role_missing(group_user):
    group_user['role'] = None
    invalid(data=group_user)


def test_add_to_group():
    group = Group()

    current_user = User()
    current_user_group_user = GroupUser()
    current_user_group_user.group = group
    current_user_group_user.user = current_user
    current_user_group_user.role = ROLE.SENIOR_RESEARCHER
    current_user.group_users.append(current_user_group_user)

    data = {
        'group': group,
        'user': User(),
        'role': ROLE.RESEARCHER
    }

    valid(data=data, user=current_user)


def test_add_to_another_group():
    current_user = User()
    current_user_group_user = GroupUser()
    current_user_group_user.group = Group()
    current_user_group_user.user = current_user
    current_user_group_user.role = ROLE.SENIOR_RESEARCHER
    current_user.group_users.append(current_user_group_user)

    data = {
        'group': Group(),
        'user': User(),
        'role': ROLE.RESEARCHER
    }

    with pytest.raises(PermissionDenied):
        valid(data=data, user=current_user)


def test_add_to_group_not_managed_role():
    group = Group()

    current_user = User()
    current_user_group_user = GroupUser()
    current_user_group_user.group = group
    current_user_group_user.user = current_user
    current_user_group_user.role = ROLE.SENIOR_RESEARCHER
    current_user.group_users.append(current_user_group_user)

    data = {
        'group': group,
        'user': User(),
        'role': ROLE.SENIOR_RESEARCHER
    }

    with pytest.raises(PermissionDenied):
        valid(data=data, user=current_user)


def test_remove_own_membership():
    current_user = User()

    group_user = GroupUser()
    group_user.group = Group()
    group_user.user = current_user
    group_user.role = ROLE.SENIOR_RESEARCHER
    current_user.group_users.append(group_user)

    data = {
        'group': Group(),
        'user': User(),
        'role': ROLE.RESEARCHER
    }

    with pytest.raises(PermissionDenied):
        valid(group_user, data=data, user=current_user)


def test_update_own_membership():
    current_user = User()
    group = Group()

    group_user = GroupUser()
    group_user.group = group
    group_user.user = current_user
    group_user.role = ROLE.SENIOR_RESEARCHER
    current_user.group_users.append(group_user)

    data = {
        'group': group,
        'user': current_user,
        'role': ROLE.RESEARCHER
    }

    with pytest.raises(PermissionDenied):
        valid(group_user, data=data, user=current_user)


def test_already_in_group():
    user = User()
    group = Group()

    group_user = GroupUser()
    group_user.user = user
    group_user.group = group
    group_user.role = ROLE.RESEARCHER
    user.group_users.append(group_user)

    data = {
        'user': user,
        'group': group,
        'role': ROLE.SENIOR_RESEARCHER
    }

    valid(data=data)


def test_already_in_group_and_role():
    user = User()
    group = Group()

    group_user = GroupUser()
    group_user.user = user
    group_user.group = group
    group_user.role = ROLE.RESEARCHER
    user.group_users.append(group_user)

    data = {
        'user': user,
        'group': group,
        'role': ROLE.RESEARCHER
    }

    invalid(data=data)


def invalid(*args, **kwargs):
    with pytest.raises(ValidationError) as e:
        valid(*args, **kwargs)

    return e


def valid(instance=None, data=None, user=None):
    if user is None:
        user = User(is_admin=True)

    serializer = GroupUserSerializer(instance=instance, data=data, context={'user': user})
    serializer.is_valid(raise_exception=True)
    return serializer.save()
