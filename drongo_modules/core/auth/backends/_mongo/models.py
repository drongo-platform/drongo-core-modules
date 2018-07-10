from datetime import datetime, timedelta

from drongo_modules.core.database.utils.mongo_orm.document import Document


class User(Document):
    __version__ = '1.0.0'
    __fields__ = [
        'username',
        'password',
        'active',
        'superuser',
        'created_on',
        'extras'
    ]


class UserToken(Document):
    __version__ = '1.0.0'
    __fields__ = [
        'user_id',
        'token',
        'expires'
    ]
    __resolve__ = {
        'user': ('user_id', User)
    }

    def refresh(self, span):
        self.expires = datetime.utcnow() + timedelta(minutes=span)
        self.save()


class Group(Document):
    __version__ = '1.0.0'
    __fields__ = [
        'name',
        'users',
        'extras'
    ]

    def add_user(self, username):
        if self.users is None:
            self.users = []

        if username not in self.users:
            self.users.append(username)

        self.save(force=True)

    def remove_user(self, username):
        if self.users is None:
            return

        if username in self.users:
            self.users.remove(username)
            self.save(force=True)

    @classmethod
    def for_user(cls, username):
        return list(map(
            lambda item: item.name,
            cls.objects.find(users=username)
        ))


class ObjectOwner(Document):
    __version__ = '1.0.0'
    __fields__ = [
        'object_type',
        'object_id',
        'user'
    ]


class Permission(Document):
    __version__ = '1.0.0'
    __fields__ = [
        'permission_id',
        'client'
    ]


class ObjectPermission(Document):
    __version__ = '1.0.0'
    __fields__ = [
        'object_type',
        'object_id',
        'permission_id',
        'client'
    ]
