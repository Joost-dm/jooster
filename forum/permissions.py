""" Forum permissions decloration. """

from django.http import Http404
from rest_framework import permissions
from forum import models
from django.shortcuts import get_object_or_404


class IsAuthorOrReadOnlyOrAdmin(permissions.BasePermission):
    """ Is author or read only permission. """

    def has_object_permission(self, request, view, obj):
        if (request.user and request.user.is_staff):
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author.id == request.user.id


class IsPrivateForumMemberOrAdmin(permissions.BasePermission):
    """ User is a member of private forum. """

    def has_permission(self, request, view):
        if (request.user and request.user.is_staff):
            return True
        if 'forum' in view.kwargs.keys():
            forum_id = view.kwargs['forum']
        elif 'parent_forum' in request.data.keys():
            forum_id = request.data['parent_forum']
        elif 'parent_branch' in request.data.keys():
            forum_id = models.Branch.objects.get(id=request.data['parent_branch']).parent_forum.id
        elif 'parent_thread' in request.data.keys():
            branch_id = models.Thread.objects.get(id=request.data['parent_thread']).parent_branch.id
            forum_id = models.Branch.objects.get(id=branch_id).parent_forum.id
        else:
            forum_id = 0
        try:
            get_object_or_404(models.ForumMembership, user = request.user.id, forum=forum_id)
            return True
        except Http404:
            try:
                forum = get_object_or_404(models.Forum, id=forum_id)
                if forum.is_private:
                    return False
            except Http404:
                pass
            return True


class IsPrivateBranchMemberOrAdmin(permissions.BasePermission):
    """ User is a member of private branch. """

    def has_permission(self, request, view):
        if (request.user and request.user.is_staff):
            return True
        if 'branch' in view.kwargs.keys():
            branch_id = view.kwargs['branch']
        elif 'parent_branch' in request.data.keys():
            branch_id = request.data['parent_branch']
        elif 'parent_thread' in request.data.keys():
            branch_id = models.Thread.objects.get(id=request.data['parent_thread']).parent_branch.id
        else:
            branch_id = 0
        print(branch_id)
        try:
            get_object_or_404(models.BranchMembership, user = request.user.id, branch=branch_id)
            return True
        except Http404:
            try:
                branch = get_object_or_404(models.Branch, id=branch_id)
                if branch.is_private:
                    return False
            except Http404:
                pass
            return True
