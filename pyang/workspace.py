"""Workspace Folder Context"""

import json
from optparse import Values  #pylint: disable=deprecated-module
import os
import sys
from typing import Any, List


from pyang import plugin
from pyang.context import Context
from pyang.repository import FileRepository


class WorkspaceFolderContext:
    name: str
    """Corresponds to `lsprotocol.types.WorkspaceFolder.name`"""
    path: str
    """Corresponds to `lsprotocol.types.WorkspaceFolder.uri`"""
    opts: Values
    """`optparse.Values`"""
    ctx: Context
    """`pyang.context.Context`"""
    cfg: Any
    """Folder level configuration file dictionary"""

    def __init__(self, name: str, path: str, opts: Values):
        self.name = name
        self.path = path
        self.opts = opts
        self._build_context()

    def _build_context(self):
        o = self.opts
        proj_dir = self.path

        if o.config:
            config_path = os.path.abspath(o.config)
        else:
            config_path = os.path.join(proj_dir, '.pyang.json')
        cfg = None
        path = ''
        ignore_path = ''
        cfg_paths: List[str] = []
        cfg_ignore_paths = []
        if os.path.exists(config_path) and os.path.isfile(config_path):
            if o.verbose:
                sys.stderr.write(f"# {self.name} context config: {os.path.abspath(config_path)}\n")
            with open(config_path, 'r', encoding='utf-8') as config_file:
                cfg = json.load(config_file)
                self.cfg = cfg
                if o.verbose:
                    sys.stderr.write(json.dumps(cfg, indent=4) + '\n')
                try:
                    cfg_paths = cfg["search"]["paths"]
                    cfg_ignore_paths = cfg["search"]["ignorePaths"]
                except KeyError:
                    pass

        path = ''
        for cfg_path in cfg_paths:
            if not os.path.isabs(cfg_path):
                cfg_path = os.path.join(proj_dir, cfg_path)
            if path:
                path = os.pathsep.join([path, cfg_path])
            else:
                path = cfg_path
        path = os.pathsep.join(o.path + [path])

        default_dirs = "."
        if o.proj_dir != ".":
            default_dirs += os.pathsep + "."
        # add standard search path
        if len(o.path) == 0:
            path = default_dirs
        else:
            path += os.pathsep + default_dirs

        ignore_path = ''
        for cfg_ignore_path in cfg_ignore_paths:
            if not os.path.isabs(cfg_ignore_path):
                cfg_ignore_path = os.path.join(proj_dir, cfg_ignore_path)
            if ignore_path:
                ignore_path = os.pathsep.join([ignore_path, cfg_ignore_path])
            else:
                ignore_path = cfg_ignore_path
        ignore_path = os.pathsep.join(o.ignore_path + [ignore_path])

        no_path_recurse = False
        if o.no_path_recurse:
            no_path_recurse = o.no_path_recurse
        elif cfg:
            try:
                no_path_recurse = not cfg["search"]["pathRecurse"]
            except KeyError:
                pass

        use_env = True
        if o.no_env_path is not None:
            use_env = not o.no_env_path
        elif cfg:
            try:
                use_env = cfg["search"]["useDefaults"]
            except KeyError:
                pass

        repos = FileRepository(path=path,
                               use_env=use_env,
                               no_path_recurse=no_path_recurse,
                               ignore_path=ignore_path,
                               verbose=o.verbose)
        self.ctx = Context(repos)

        self.ctx.opts = o # type: ignore
        self.ctx.cfg = cfg # type: ignore
        self.ctx.keep_arg_substrings = True

        if o.canonical is not None:
            self.ctx.canonical = o.canonical
        elif cfg:
            try:
                self.ctx.canonical = cfg["lint"]["canonical"]
            except KeyError:
                pass

        if o.max_line_len is not None:
            self.ctx.max_line_len = o.max_line_len
        elif cfg:
            try:
                if cfg["lint"]["longLine"]:
                    self.ctx.max_line_len = cfg["lint"]["longLine"]["length"]
            except KeyError:
                pass

        if o.max_identifier_len is not None:
            self.ctx.max_identifier_len = o.max_identifier_len
        elif cfg:
            try:
                if cfg["lint"]["longIdentifier"]:
                    self.ctx.max_identifier_len = cfg["lint"]["longIdentifier"]["length"]
            except KeyError:
                pass

        if o.strict is not None:
            self.ctx.strict = o.strict
        elif cfg:
            try:
                self.ctx.strict = cfg["lint"]["strict"]
            except KeyError:
                pass

        for p in plugin.plugins:
            p.setup_ctx(self.ctx)


    def is_ignored(self, doc_uri: str) -> bool:
        if 'validation' in doc_uri or 'visualization' in doc_uri:
            return True
        return False
