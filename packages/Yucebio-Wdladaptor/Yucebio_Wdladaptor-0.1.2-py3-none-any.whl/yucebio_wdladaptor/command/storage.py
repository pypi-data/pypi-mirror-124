import sys

import click
# from yucebio_wdladaptor.util.config import Config
from yucebio_wdladaptor.util.monitor import Monitor

from .base import AliasedGroup


@click.group('monitor', cls=AliasedGroup)
def cli():
    """作业监控"""
    pass

@cli.command()
@click.option("--prefix", '-p', help="Cromwell作业中输入数据中的的prefix字段内容", type=str)
@click.option("--server", '-s', help="cromwell 服务器别名", type=str)
@click.option("--job_id", '-j', help="cromwell 作业id")
@click.option("--call_name", '-n', help="流程子步骤名称（不需要流程名前缀）", default=None, type=str)
@click.option("--call_index", '-i', help="子步骤序号（从0开始计数）", default=None)
@click.option("--output", '-o', help="需要下载的输出文件（多个文件之间使用逗号分隔）")
def project_path(**kw):
    """根据prefix或cromwell作业id获取云上的中间文件路径

    prefix 和 【服务器名称+作业id】 必须提供一种
    """
    # config = Config(check_login=False)
    monitor = Monitor()
    
    # 1. 根据server + jobid 或 prefix 获取cromwell_job
    job = monitor.get_job(prefix=kw['prefix'], server=kw['server'], cromwell_id=kw['job_id'])
    job.get_metadata()
    job.format()

    # 2. 获取默认输出目录
    cromwell_id = job.cromwell_id
    metadata = job.metadata
    # 2.1 若存在outputs，则从outputs中找
    first_out_file = get_first_output_file(cromwell_id, metadata)    # type: str
    if first_out_file:
        base = first_out_file.split(cromwell_id)[0]
    # 2.2 尝试从每个calls中获取路径
    else:
        if not metadata.get('calls'):
            click.secho("当前作业未执行", fg="red")
            return

        calls = metadata['calls'] # type: dict[str, list[dict]]
        for call_task in calls.values():
            call_item = call_task[0]

            first_out_file = get_first_output_file(cromwell_id, call_item)
            if not first_out_file:
                continue
            base = first_out_file.split(cromwell_id)[0]
            break

    if not base:
        click.secho("无法获取当前作业的分析目录", fg="red")
        return
    cmd = get_download_command(base)
    base += cromwell_id + '/'

    if not kw['call_name']:
        print("请使用", click.style(cmd, fg="yellow"), "下载目录: ", click.style(base, fg='green'))
        return

    # 3. 根据子步骤下载文件
    if not metadata.get('calls'):
        click.secho("当前作业没有已执行的子步骤", fg="red")
        return
    
    calls = metadata['calls']   # type: dict[str, list[dict]]
    expect_call_name = kw['call_name'].lower()
    expect_call_task = None
    for call_name, call_task in calls.items():
        if call_name.lower().endswith(expect_call_name):
            expect_call_task = call_task
            break
    if not expect_call_task:
        click.secho(f"子步骤{expect_call_name}未找到", fg="red")
        return

    # 从当前task中获取输出目录
    first_out_file = get_first_output_file(cromwell_id, expect_call_task[0])
    if not first_out_file:
        print(
            f"当前步骤{call_name}没有输出内容。\n", 
            "请使用", 
            click.style(cmd, fg="yellow"), 
            "下载目录: ", 
            click.style(base, fg='green')
        )
        return
    # base = first_out_file.split(cromwell_id)[0]
    _, sub = first_out_file.split(cromwell_id)
    dir_calls = sub.strip('/').split('/')
    if dir_calls:
        base += dir_calls[0] + '/'

    if kw['call_index'] is None:
        print("请使用", click.style(cmd, fg="yellow"), "下载目录: ", click.style(base, fg='green'))
        return

    idx = int(kw['call_index']) or 0
    if len(expect_call_task) <= idx:
        click.secho(f"子步骤序号不能超过{len(expect_call_task)-1}", fg="red")
        return
    first_out_file = get_first_output_file(cromwell_id, expect_call_task[idx])
    if not first_out_file:
        print(
            f"当前步骤{call_name}的第{idx}次执行没有输出内容。\n", 
            "请使用", 
            click.style(cmd, fg="yellow"), 
            "下载目录: ", 
            click.style(base, fg='green')
        )
        return
    _, sub = first_out_file.split(cromwell_id)
    dir_calls = sub.strip('/').split('/')
    if len(dir_calls) > 1:
        base += dir_calls[1] + '/'
        # base = '/'.join([base[:-1]] + dir_calls[1:2])

    print("请使用", click.style(cmd, fg="yellow"), "下载目录: ", click.style(base, fg='green'))
    return

def get_first_output_file(cromwell_id: str, item: dict) -> str:
    if not item.get('outputs'):
        return ""
    outputs = item['outputs'] # type: dict
    for _, v in outputs.items():
        if isinstance(v, str) and cromwell_id in v:
            return v
    return ""

def get_download_command(basepath: str):
    cmd = "scp"
    if basepath.startswith('oss'):
        cmd ='aliyun oss cp 或 ossutil cp'
    elif basepath.startswith('s3'):
        cmd = 'aws s3 cp'
    return cmd

@cli.command()
@click.option("--prefix", '-p', help="Cromwell作业中输入数据中的的prefix字段内容", type=str)
@click.option("--server", '-s', help="cromwell 服务器别名", type=str)
@click.option("--job_id", '-j', help="cromwell 作业id")
def export_json(**kw):
    """导出作业对应的JSON文件. 导出内容直接打印到控制台，调用者可以使用重定向将内容输出到文件中

    prefix 和 【服务器名称+作业id】 必须提供一种
    """
    monitor = Monitor()
    
    # 1. 根据server + jobid 或 prefix 获取cromwell_job
    try:
        job = monitor.get_job(prefix=kw['prefix'], server=kw['server'], cromwell_id=kw['job_id'])
    except Exception as e:
        click.secho(e, fg="red", file=sys.stderr)
        return
    if not job:
        click.secho("无法获取作业信息", fg="red", file=sys.stderr)
        return

    job.get_metadata()
    # job.format()

    # 2. 从metadata中导出input
    metadata = job.metadata # type: dict
    submittedFiles = metadata.get('submittedFiles') # type: dict
    if not submittedFiles or not submittedFiles.get('inputs'):
        click.secho("作业内容无效，无法获取提交的文件内容", fg="red", file=sys.stderr)

    inputs = submittedFiles['inputs']
    # print(inputs)

    import json5
    d = json5.loads(inputs)
    json5.dump(d, sys.stdout, indent=2)
