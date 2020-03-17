from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Only allow owners of an object to read and edit it
    """
    
    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the owner of the snippet
        return obj.owner == request.user

class IsNotDefault(permissions.BasePermission):
    """
    Only admin can change default object
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_superuser:
            return True
        elif obj.default == True:
            return False 

class IsPropertyOwner(permissions.BasePermission):
    """
    Only asset owner of property can read and write
    """

    def has_object_permission(self,request,view,obj):
        return obj.asset.owner == request.user

class IsPremisesOwner(permissions.BasePermission):
    """
    Only property onwer can read and write
    """

    def has_object_permission(self, request, view, obj):
        return obj.property.asset.owner == request.user

class IsRentOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.premises.property.asset.owner == request.user


