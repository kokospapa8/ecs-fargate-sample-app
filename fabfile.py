import boto, os
from boto.ec2 import connect_to_region
from fabric import Connection, task

SSH_KEY = ""

# this function only gets ec2 on public subnets
def _get_ec2_instances():
    instances = []
    connection = connect_to_region(
        region_name = "us-east-2", #TODO beta env
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )

    try:
        reservations = connection.get_all_reservations(filters= {'tag:Name':'ecs-sample-api','tag:env':'staging'})
        for r in reservations:
            for instance in r.instances:
                instances.append(instance)

    except boto.exception.EC2ResponseError as e:
        print(e)
        return

    instances=filter(None, instances)
    return instances

def _get_ec2_ips():
    hosts = []
    instances = _get_ec2_instances()
    for i in instances:
        hosts.append(str(i.ip_address))
    return hosts


def _conn():
    hostConn = []
    #validate data
    host_ips = _get_ec2_ips()
    for ip in host_ips:
        hostConn.append(Connection(host=ip, user='ubuntu', port=22,
                   connect_kwargs={"key_filename": SSH_KEY}))
    return hostConn


def _run_cmd(conn, command):
    print(conn.host)
    print("\n")
    conn.run(command)
    print("------------------\n")
    conn.close()


@task
def get_ec2_status(c):
    instances = _get_ec2_instances()
    print("---------------------------------\n")
    for i in instances:
        print("host: ", i.id)
        print(i.ip_address)
        print(i.state)
        print("---------------------------------\n")

@task
def git_pull(c):
    for conn in _conn():
        with conn.cd('/home/ubuntu/ecs-fargate-sample-app'):
            _run_cmd(conn,'git pull')
            conn.close()

@task
def disk_space(c):
    for conn in _conn():
        _run_cmd(conn, 'df -h')
        conn.close()

@task
def docker_build(c):
    for conn in _conn():
        with conn.cd('/home/ubuntu/ecs-fargate-sample-app'):
            conn.run('docker-compose -f docker-compose-staging.yml up --build -d')

@task
def docker_ps(c):
    for conn in _conn():
        _run_cmd(conn, 'docker ps')
        conn.close()

@task
def docker_clean(c):
    for conn in _conn():
        _run_cmd(conn, 'docker rmi $(docker images -a -q)')
        conn.close()

@task
def cpu(c):
    for conn in _conn():
        conn.run('free -m')
        print("\n")
        print("--------------------------------")
        conn.run('ps aux --sort=-%mem | awk \'NR<10{print $0}\'')
        conn.close()


@task
def docker_logs(c):
    for conn in _conn():
        conn.run('docker logs $(docker ps -aqf "name=ecs-fargate-sample-app_app") --tail 50 ')
        conn.close()

@task
def check_env(c):
    for conn in _conn():
        _run_cmd(conn, 'export')
