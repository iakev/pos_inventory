from rest_access_policy import AccessPolicy


class CategoryAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["list", "retrieve", "search", "list_all_products"],
            "principal": ["*"],
            "effect": "allow",
        },
        {
            "action": ["create", "update", "partial_update", "destroy"],
            "principal": ["group:Owners", "group:Trusted Staff", "superuser"],
            "effect": "allow",
        },
    ]
