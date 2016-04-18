#!/usr/bin/python
import sys
import subprocess
import json


args = sys.argv[2]
args = json.loads(args)
owner = args["repo"]["owner"]
name = args["repo"]["name"]
branch = args["build"]["branch"]
commit = args["build"]["commit"]
artifact_name = "%s_%s_%s_%s" % (owner, name, branch, commit)
plugin_args = args["vargs"]
published_branches = plugin_args["published_branches"]
build_succeeded = args["build"]["status"] == "success" 
rados_hosts = plugin_args["rados_hosts"]
rados_fsid = plugin_args["rados_fsid"]
included_dirs = plugin_args["published_directories"]
code_path = args["workspace"]["path"]
rados_pool = plugin_args["rados_pool"]

if branch not in published_branches:
    print("%s not in published branches, skipping upload" % branch)
    sys.exit(0)


def create_archive(path, artifact_name, included_dirs):
    subprocess.call(["/bin/tar", "czvf", "/tmp/%s.tar.gz" % artifact_name, "-C", path] + included_dirs)

def generate_config(fsid, hosts):
    hosts = ", ".join(hosts)
    template = """[global]
      fsid = %s
      mon host = %s
      """ % (fsid, hosts)
    f = open("/etc/ceph/ceph.conf", "w")
    f.write(template)
    f.close()

generate_config(rados_fsid, rados_hosts)

create_archive(code_path, artifact_name, included_dirs)

subprocess.call(["/usr/bin/rados", "-p", rados_pool, "put", artifact_name+".tar.gz", "/tmp/%s.tar.gz" % artifact_name])