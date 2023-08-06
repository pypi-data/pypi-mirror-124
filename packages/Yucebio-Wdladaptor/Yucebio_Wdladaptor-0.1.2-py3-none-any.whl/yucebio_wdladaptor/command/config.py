import json
import click
from .base import AliasedGroup
from yucebio_wdladaptor.util.config import Config
from yucebio_wdladaptor.backend import SUPPORTTED_BACKENDS, create_adaptor, PLACEHOLDER_SIMG_PATH, PLACEHOLDER_GLOBAL_PATH, BaseAdaptor


@click.group('config', cls=AliasedGroup)
def cli():
    """查看或管理配置"""
    pass


@cli.command()
@click.option("--platform", "-p", type=click.Choice(list(SUPPORTTED_BACKENDS)), required=True, help="platform")
@click.option("--alias", "-a", help="配置别名，支持同一平台下的多个cromwell服务", default=None)
@click.option('--host', '-h', help="cromwell server 地址", required=True)
@click.option('--global_path', '-g', help=f"公共文件路径，用于自动替换json中的[{PLACEHOLDER_GLOBAL_PATH}]", type=str, required=True)
@click.option('--simg_path', '-s', help=f"singulartiy镜像路径，用于自动替换json中的[{PLACEHOLDER_SIMG_PATH}]", type=str, required=True)
@click.option('--runtimes', '-r', help=f"配置当前服务支持的自定义RUNTIME属性，多个属性之间使用逗号分隔", type=str)
def add_cromwell(**kw):
    """新增或更新更新Cromwell Server平台配置"""
    config = Config()

    platform = kw['platform']
    if kw['runtimes']:
        kw['runtimes'] = kw['runtimes'].split(',')
    if kw['host']:
        kw['host'] = kw['host'].strip('/')
    cfg = {k: kw[k] for k in kw if kw[k]}
    alias = kw['alias']
    if not kw['alias']:
        alias = platform
    if cfg:
        config.add_server(alias, cfg)
    config.pp(config.servers)

@cli.command()
def list_cromwell(**kw):
    """查看Cromwell Server平台配置"""
    config = Config()
    config.pp(config.servers)

@cli.command()
@click.option("--alias", "-a", help="配置别名", required=True)
def delete_cromwell(alias: str):
    """查看Cromwell Server平台配置"""
    config = Config()
    config.del_server(alias)
    config.pp(config.servers)

@cli.command()
@click.option('--host', '-h', help="服务器地址", type=str)
@click.option('--port', '-p', help="服务器端口号", type=int)
def api_service(host: str, port: int):
    """配置或查看适配器专用的API服务器地址

    适配器专用API服务器通过restful接口提供任务状态同步、进度跟踪、结果下载等复杂操作支持

    1. 通过适配器投递任务时，适配器自动在api服务器添加当前用户的作业信息
    2. api服务器自动监测任务进度，
    """
    config = Config()
    if host and port:
        config.set_api_service({"host": host, "port": port})
    api_server = config.api_server
    if not api_server:
        click.secho("未配置", fg="red")
    else:
        click.secho("当前服务配置信息为: ", fg="green")
        config.pp(api_server)

@cli.command()
@click.option('--upload/--download', '-u/-d', is_flag=True, default=False, help="设置同步模式（上传或下载）", show_default=True)
def sync(upload: str):
    """执行配置同步：

    1. 上传个人配置到gitlab
    2. 从gitlab下载个人配置
    """
    config = Config()
    if not upload:
        try:
            url = config.download_config()
            click.secho(f"download success from {url}", fg='green')
        except Exception as e:
            click.secho(f"下载配置异常: {e}", fg='red')
            raise e
    else:
        click.secho("upload config to gist", fg='yellow')
        url = config.upload_config()
        click.secho(f"upload success: {url}", fg='green')