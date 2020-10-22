#!/usr/bin/python
# Prod site hook
# Run by the post-checkout hook to restore file permissions after transfer

import os
import os.path
import pwd
import grp
from enum import Enum
from enum import IntEnum

class PER(IntEnum):
    Path = 0
    Stat = 1
    Owner = 2
    Group = 3

permissions = []
file = '/home/produser/public_html/transfer/.permissions'

with open(file) as permissions_file:
    for line in permissions_file:

        split = line
        split = split.split(";")
        perm = []

        for each in split:

            each = each.strip()
            perm.append(each)

        permissions.append(perm)

uid_root = pwd.getpwnam("root").pw_uid
gid_root = pwd.getpwnam("root").pw_gid
uid_produser = pwd.getpwnam("produser").pw_uid
gid_produser = pwd.getpwnam("produser").pw_gid
uid_devuser = pwd.getpwnam("devuser").pw_uid
gid_devuser = pwd.getpwnam("devuser").pw_gid
gid_nobody = pwd.getpwnam("nobody").pw_gid

for perm in permissions:

    if os.path.exists(perm[PER.Path.value]):

        os.chmod(perm[PER.Path.value], int(perm[PER.Stat.value], 8))

        if perm[PER.Owner.value] == "root":

            os.chown(perm[PER.Path.value], uid_root, gid_root)

        elif perm[PER.Group.value] == "nobody":

            os.chown(perm[PER.Path.value], uid_produser, gid_nobody)

        else:

            os.chown(perm[PER.Path.value], uid_produser, gid_produser)

    else:

        print("File Does Not Exist: ", perm[PER.Path.value])
