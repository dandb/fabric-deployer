from fabric.api import * 
from json import load
import urllib2

def load_config():
    with open('project.json') as f:
        return load(f)

def push_to_server(project, app_env, build_num, local_dir, local_code):
    put(local_code, '/var/tmp/')

def extract_deployment(tarball, deploy_location, project, build_num):
    with cd('/var/tmp/'):
        sudo('unzip -oq ' + tarball + ' -d ' + deploy_location + "/" + project + '_' + build_num)

def update_permissions(deploy_location):
    with cd(deploy_location):
        sudo('chown apache:apache -R *')

def verify_local_bn(deploy_location, project, bn_location="/current/www/public"):
    if project == "verified":
        bn_location = "/current/public"
    with cd(deploy_location + bn_location):
        bn = sudo('cat bn')

def update_symlinks(project, build_num, deploy_location):
    with cd(deploy_location):
        sudo('rm -fr current')
        sudo('ln -s ' + project + '_' + build_num + ' current') 

def rollback(project, app_env, bn, deploy_location):
    with cd(deploy_location):
        sudo('rm -fr current')
        sudo('ln -s ' + project + '_' + bn + ' current')

def check_build_number(project, app_env, host, project_config):
    req = urllib2.Request("http://" + host + "/bn", headers={"Host":project_config[project][app_env]})
    try:
        data = urllib2.urlopen(req)
        build_num = int(data.read())
    except urllib2.HTTPError:
        print "No existing Build number"
        build_num = 0
    return build_num

def compare_build_number(project, app_env, project_config, equality=True):
    build_nums = {}
    set_of_builds = set()
    for host in env.hosts:
        build_nums[host] = check_build_number(project, app_env, host, project_config)
    for server,build in build_nums.iteritems():
        set_of_builds.add(build) 
    if len(set_of_builds) > 1:
        equality = False
    return equality

def post_install(deploy_location):
    with cd(deploy_location):
        try:
            sudo('sh current/postinstall.sh')
        except:
            pass

def restart_services():
    sudo('service httpd restart')

def maintenance():
    pass

def deploy(project, app_env, build_num, local_dir='/var/lib/jenkins-slave/workspace/'):
    project_config = load_config()
    starting_bn = check_build_number(project, app_env, env.host_string, project_config)
    deploy_location = '/var/www/' + project_config[project][app_env] + '/' + project
    tarball = project + ".zip"
    local_code = local_dir + project + '_' + app_env + '_deploy/' + tarball

    push_to_server(project, app_env, build_num, local_dir, local_code)
    extract_deployment(tarball, deploy_location, project, build_num)
    update_symlinks(project, build_num, deploy_location)
    verify_local_bn(deploy_location, project)
    update_permissions(deploy_location)
    post_install(deploy_location)
    restart_services()

def verify_cluster_versions(project, app_env):
    project_config = load_config()
    if not compare_build_number(project, app_env, project_config):
        print "Build number mismatch"
