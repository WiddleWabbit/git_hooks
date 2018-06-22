#!/usr/bin/python

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
file = '/home/%%CPANELUSERHERE%%/public_html/transfer/.permissions'

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
uid_%%CPANELUSERHERE%% = pwd.getpwnam("%%CPANELUSERHERE%%").pw_uid
gid_%%CPANELUSERHERE%% = pwd.getpwnam("%%CPANELUSERHERE%%").pw_gid
uid_%%DEVUSERHERE%% = pwd.getpwnam("%%DEVUSERHERE%%").pw_uid
gid_%%DEVUSERHERE%% = pwd.getpwnam("%%DEVUSERHERE%%").pw_gid
gid_nobody = pwd.getpwnam("nobody").pw_gid

for perm in permissions:
    
    os.chmod(perm[PER.Path.value], int(perm[PER.Stat.value], 8))

    if perm[PER.Owner.value] == "root":

        os.chown(perm[PER.Path.value], uid_root, gid_root)

    elif perm[PER.Group.value] == "nobody":
    
        os.chown(perm[PER.Path.value], uid_%%CPANELUSERHERE%%, gid_nobody)

    else:

        os.chown(perm[PER.Path.value], uid_%%CPANELUSERHERE%%, gid_%%CPANELUSERHERE%%)
