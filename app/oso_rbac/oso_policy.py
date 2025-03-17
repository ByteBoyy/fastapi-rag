from oso import Oso
from app.models.user import User
from app.models.resource import AppResource

oso = Oso()

def setup_oso():
    oso.register_class(User)
    oso.register_class(AppResource)

    oso.load_str('''
        actor User {}
        resource AppResource {}

        allow(user: User, action, resource: AppResource) if
            has_permission(user, action, resource);

        has_permission(user: User, "read", resource: AppResource) if
            (resource.name = "profile" or resource.name = "rag_query") and
            (user.role = "user" or user.role = "admin");

        has_permission(user: User, "manage", resource: AppResource) if
            (resource.name = "profile" or resource.name = "rag_upload") and
            user.role = "admin";
    ''')

setup_oso()
