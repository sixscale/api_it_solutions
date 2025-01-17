from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView
from typing import Any


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: APIView, obj: Any) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
