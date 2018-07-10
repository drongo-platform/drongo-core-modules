import uuid

from datetime import datetime

from passlib.hash import pbkdf2_sha256

import pymongo

from .models import (
    User, UserToken, Group, ObjectOwner, Permission, ObjectPermission
)


HASHER = pbkdf2_sha256.using(rounds=10000)


class AuthServiceBase(object):
    @classmethod
    def init(cls, module):
        cls.module = module

        User.set_collection(
            module.database.instance.get_collection('auth_users'))
        User.__collection__.create_index([('username', pymongo.HASHED)])

        UserToken.set_collection(
            module.database.instance.get_collection('auth_user_tokens'))
        UserToken.__collection__.create_index([('token', pymongo.HASHED)])
        UserToken.__collection__.create_index([('expires', pymongo.ASCENDING)])

        Group.set_collection(
            module.database.instance.get_collection('auth_groups'))
        Group.__collection__.create_index([('name', pymongo.HASHED)])
        Group.__collection__.create_index([('users', pymongo.ASCENDING)])

        ObjectOwner.set_collection(
            module.database.instance.get_collection('auth_object_owners'))
        ObjectOwner.__collection__.create_index([
            ('object_type', pymongo.ASCENDING),
            ('object_id', pymongo.ASCENDING),
            ('user', pymongo.ASCENDING)
        ])

        Permission.set_collection(
            module.database.instance.get_collection('auth_permissions'))
        Permission.__collection__.create_index([
            ('permission_id', pymongo.ASCENDING),
            ('client', pymongo.ASCENDING)
        ])

        ObjectPermission.set_collection(
            module.database.instance.get_collection(
                'auth_object_permissions'))
        ObjectPermission.__collection__.create_index([
            ('object_type', pymongo.ASCENDING),
            ('object_id', pymongo.ASCENDING),
            ('permission_id', pymongo.ASCENDING),
            ('client', pymongo.ASCENDING)
        ])


class UserForTokenService(AuthServiceBase):
    def __init__(self, token):
        self.token = token

    def call(self):
        token = UserToken.objects.find_one(token=self.token)

        if token is None:
            return None

        if token.expires < datetime.utcnow():
            token.delete()
            return None

        token.refresh(span=self.module.config.token_age)
        return token.user


class UserCreateService(AuthServiceBase):
    def __init__(self, username, password, active=False, superuser=False):
        self.username = username
        self.password = HASHER.hash(password)
        self.active = active
        self.superuser = superuser

    def check_exists(self):
        return User.objects.find_one(username=self.username) is not None

    def call(self, ctx=None):
        if self.check_exists():
            raise Exception('User already exists.')

        return User.create(
            username=self.username,
            password=self.password,
            active=self.active,
            superuser=self.superuser,
            created_on=datetime.utcnow()
        )


class UserChangePasswordService(AuthServiceBase):
    def __init__(self, username, password):
        self.username = username
        self.password = HASHER.hash(password)

    def call(self):
        user = User.objects.find_one(username=self.username, active=True)
        user.password = self.password
        user.save()


class UserLoginService(AuthServiceBase):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def check_credentials(self):
        user = User.objects.find_one(username=self.username, active=True)
        if user is None:
            return False

        return HASHER.verify(self.password, user.password)

    def create_token(self):
        user = User.objects.find_one(username=self.username, active=True)
        token = UserToken.create(
            user=user,
            token=uuid.uuid4().hex
        )
        token.refresh(span=self.module.config.token_age)
        return token.token


class UserLogoutService(AuthServiceBase):
    def expire_token(self, token):
        token = UserToken.objects.find_one(token=token)
        if token is not None:
            token.delete()

    def call(self, ctx):
        pass


class UserListService(AuthServiceBase):
    def call(self, ctx):
        return User.objects.find()


class GroupCreateService(AuthServiceBase):
    def __init__(self, name):
        self.name = name

    def call(self):
        group = Group.objects.find_one(name=self.name)
        if group is not None:
            return group

        else:
            return Group.create(name=self.name)


class GroupDeleteService(AuthServiceBase):
    def __init__(self, name):
        self.name = name

    def call(self):
        group = Group.objects.find_one(name=self.name)
        if group is not None:
            group.delete()


class GroupListService(AuthServiceBase):
    def call(self):
        return Group.objects.find()


class GroupUserAddService(AuthServiceBase):
    def __init__(self, name, username):
        self.name = name
        self.username = username

    def call(self):
        group = Group.objects.find_one(name=self.name)
        if group is None:
            group = Group.create(name=self.name)

        group.add_user(self.username)


class GroupUserDeleteService(AuthServiceBase):
    def __init__(self, name, username):
        self.name = name
        self.username = username

    def call(self):
        group = Group.objects.find_one(name=self.name)
        if group is None:
            return

        group.remove_user(self.username)


class GroupUserListService(AuthServiceBase):
    def __init__(self, name):
        self.name = name

    def call(self):
        group = Group.objects.find_one(name=self.name)
        if group is None:
            return []

        return group.users


class GroupsForUserListService(AuthServiceBase):
    def __init__(self, username):
        self.username = username

    def call(self):
        return Group.for_user(username=self.username)


class ObjectOwnerGetService(AuthServiceBase):
    def __init__(self, object_type, object_id):
        self.object_type = object_type
        self.object_id = object_id

    def call(self):
        owner = ObjectOwner.objects.find_one(
            object_type=self.object_type, object_id=self.object_id)

        if owner is not None:
            return owner.user


class ObjectOwnerSetService(AuthServiceBase):
    def __init__(self, object_type, object_id, username):
        self.object_type = object_type
        self.object_id = object_id
        self.username = username

    def call(self):
        owner = ObjectOwner.objects.find_one(
            object_type=self.object_type, object_id=self.object_id)

        if owner is not None:
            owner.user = self.username
            owner.save()
        else:
            ObjectOwner.create(
                object_type=self.object_type,
                object_id=self.object_id,
                user=self.username
            )


class PermissionCheckService(AuthServiceBase):
    def __init__(self, permission_id, username):
        self.permission_id = permission_id
        self.username = username

    def call(self):
        user = User.objects.find_one(username=self.username, active=True)
        if user is None:
            return False

        if user.superuser:
            return True

        permission = Permission.objects.find_one(
            permission_id=self.permission_id, client='user.' + self.username)
        if permission is not None:
            return True

        groups = list(map(
            lambda group: 'group.{group}'.format(group=group),
            Group.for_user(self.username)
        ))
        permission = Permission.objects.find_one(
            permission_id=self.permission_id,
            client={'$in': groups}
        )
        if permission is not None:
            return True

        return False


class PermissionSetService(AuthServiceBase):
    def __init__(self, permission_id, client):
        self.permission_id = permission_id
        self.client = client

    def call(self):
        permission = Permission.objects.find_one(
            permission_id=self.permission_id,
            client=self.client
        )
        if permission is None:
            Permission.create(
                permission_id=self.permission_id,
                client=self.client
            )


class ObjectPermissionCheckService(AuthServiceBase):
    def __init__(self, object_type, object_id, permission_id, username):
        self.object_type = object_type
        self.object_id = object_id
        self.permission_id = permission_id
        self.username = username

    def call(self):
        user = User.objects.find_one(username=self.username, active=True)
        if user is None:
            return False

        if user.superuser:
            return True

        permission = ObjectPermission.objects.find_one(
            object_type=self.object_type, object_id=self.object_id,
            permission_id=self.permission_id, client='user.' + self.username)
        if permission is not None:
            return True

        groups = list(map(
            lambda group: 'group.{group}'.format(group=group),
            Group.for_user(self.username)
        ))
        permission = ObjectPermission.objects.find_one(
            object_type=self.object_type, object_id=self.object_id,
            permission_id=self.permission_id,
            client={'$in': groups}
        )
        if permission is not None:
            return True

        return False


class ObjectPermissionSetService(AuthServiceBase):
    def __init__(self, object_type, object_id, permission_id, client):
        self.object_type = object_type
        self.object_id = object_id
        self.permission_id = permission_id
        self.client = client

    def call(self):
        permission = ObjectPermission.objects.find_one(
            object_type=self.object_type,
            object_id=self.object_id,
            permission_id=self.permission_id,
            client=self.client
        )
        if permission is None:
            ObjectPermission.create(
                object_type=self.object_type,
                object_id=self.object_id,
                permission_id=self.permission_id,
                client=self.client
            )