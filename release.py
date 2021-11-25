#!/usr/bin/python

import sys, os, shutil

__arg_list = (sys.argv)[1:]
__PROJ_ROOT = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
__client_files = ['backend/controllers/auth_controller.py', 'backend/controllers/client_controller.py', 'backend/controllers/data_controller.py',\
    'backend/implementations']


def _mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def common_copy(working_dir):
    print('copying implementations for release...')
    src = os.path.join(__PROJ_ROOT, 'backend', 'implementations')
    dst = os.path.join(working_dir, 'backend', 'implementations')
    shutil.copytree(src, dst)

    print('copying globals.py for release...')
    src_file = os.path.join(__PROJ_ROOT, 'backend', 'globals.py')
    dst_file = os.path.join(working_dir, 'backend', 'globals.py')
    shutil.copyfile(src_file, dst_file)


if str(__arg_list[0]) == 'client':
    working_dir = os.path.join(__PROJ_ROOT, 'release', 'client_side')
    _mkdir(working_dir)

    common_copy(working_dir)

    print('copying frontend for release...')
    src = os.path.join(__PROJ_ROOT, 'frontend')
    dst = os.path.join(working_dir, 'frontend')
    shutil.copytree(src, dst)

    print('copying client side codes for release...')
    src = os.path.join(__PROJ_ROOT, 'backend', 'controllers')
    dst = os.path.join(working_dir, 'backend', 'controllers')
    files = [
        'auth_controller.py', 'client_controller.py', 'data_controller.py'
    ]

    for file in files:
        src_file = os.path.join(src, file)
        dst_file = os.path.join(dst, file)
        shutil.copyfile(src_file, dst_file)

    print('copying main app for release...')
    src_file = os.path.join(__PROJ_ROOT, 'client_app.py')
    dst_file = os.path.join(working_dir, 'client_app.py')
    shutil.copyfile(src_file, dst_file)

elif str(__arg_list[0]) == 'server':
    working_dir = os.path.join(__PROJ_ROOT, 'release', 'server_side')
    _mkdir(working_dir)

    common_copy(working_dir)

    print('copying server side codes for release...')
    src = os.path.join(__PROJ_ROOT, 'backend', 'controllers')
    dst = os.path.join(working_dir, 'backend', 'controllers')
    files = ['server_controller.py', 'data_controller.py']

    for file in files:
        src_file = os.path.join(src, file)
        dst_file = os.path.join(dst, file)
        shutil.copyfile(src_file, dst_file)

    print('copying main app for release...')
    src_file = os.path.join(__PROJ_ROOT, 'serverapp.py')
    dst_file = os.path.join(working_dir, 'serverapp.py')
    shutil.copyfile(src_file, dst_file)
