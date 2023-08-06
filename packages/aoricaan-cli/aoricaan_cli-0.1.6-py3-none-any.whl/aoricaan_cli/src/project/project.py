import json
import os
from pathlib import Path

import typer

from aoricaan_cli import templates
from aoricaan_cli.src.utils.core import copytree, write_templates, write_dev_ops_files
from aoricaan_cli.src.utils.debugger import Debug
from aoricaan_cli.src.utils.install_layers import install
from aoricaan_cli.src.utils.state import State
from aoricaan_cli.src.utils.synth import build_all_lambdas, update_deploy_id_resource_api_gateway, build_layers

state = State()
app = typer.Typer()


@app.command('synth')
def build_project():
    """
    Build the files for deploy the project in aws.
    """
    # TODO: Modify for use best practices.
    build_all_lambdas(lambdas_path='src/lambdas', path_cfn_template='projectTemplate.json',
                      path_swagger_template='src/petcare.json', bucket=os.environ.get('artifact_bucket'))
    update_deploy_id_resource_api_gateway(path_template='projectTemplate.json')
    build_layers(layers_path='src/layers')


@app.command('install')
def install_layers():
    """
    Install layer in local environment.
    """
    install()


@app.command('init')
def initialize_new_project():
    """
    Initialize a new empty project in the current path.

    """
    path = Path(os.getcwd())

    src_path = path.joinpath('src')
    src_path.mkdir()

    src_path.joinpath('lambdas').mkdir()

    layers_path = src_path.joinpath('layers')
    layers_path.mkdir()

    src_path.joinpath('api.json').write_text(json.dumps({}))

    templates_path = path.joinpath('utils')
    templates_path.mkdir()

    templates_path = templates_path.joinpath('templates')
    templates_path.mkdir()

    write_templates(templates_path)

    write_dev_ops_files(path)

    from_path = Path(os.path.dirname(templates.__file__)).joinpath('layers')
    copytree(from_path, layers_path)

    Debug.success('Project init successfully!')



@app.command('show')
def show_path():
    print(os.path.dirname(templates.__file__))


@app.callback()
def root(ctx: typer.Context, verbose: bool = False):
    """
    Manage the project.

    """
    state.verbose = verbose
    if state.verbose and ctx.invoked_subcommand:
        Debug.info(f"Running command: {ctx.invoked_subcommand}")


if __name__ == '__main__':
    app()
