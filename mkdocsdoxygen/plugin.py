import os.path
import subprocess
import shutil
import logging
logger = logging.getLogger("mkdocs")

from mkdocs.config import config_options as mkd
from .configitems import ConfigItems
from mkdocs.plugins import BasePlugin

def get_doxygen_key(doxyfile, key, default=None):
    try:
        return next(ln.split("=")[1].strip() for ln in open(doxyfile) if ln.strip().startswith(key))
    except StopIteration:
        if default is not None:
            return default
        else:
            raise RuntimeError("Could not find a value for '{0}' in doxygen config file '{1}'".format(key, doxyfile))

def runDoxygen(basedir, cfg=None, workdir=None, dest=None, tryClone=False, recursive=False):
    if os.path.isdir(basedir):
        basedir = os.path.abspath(basedir)
        ## check config (and guess, if needed)
        if cfg is None:
            defaultCfg = [ os.path.join(basedir, cfgName) for cfgName in ("Doxyfile", "doxygen.cfg") ]
            for cfgTry in defaultCfg:
                if os.path.exists(cfgTry):
                    cfg = cfgTry
                    break
            if cfg is None:
                raise RuntimeError("No doxygen with default name found in {0}. please specify the name through the 'config' key".format(basedir))
        else:
            if not os.path.isabs(cfg):
                cfg = os.path.join(basedir, cfg)
            if not os.path.exists(cfg):
                raise ValueError("File {0} not found".format(cfg))

        ## check workdir (and guess, if needed)
        if workdir is None:
            workdir = os.path.dirname(cfg)
        else:
            if not os.path.isabs(workdir):
                workdir = os.path.join(os.path.dirname(cfg), workdir)
            if not os.path.isdir(workdir):
                raise ValueError("Working directory {0} for running doxygen not found".format(workdir))

        outpath = os.path.join(os.path.join(workdir, get_doxygen_key(cfg, "OUTPUT_DIRECTORY", ".")), get_doxygen_key(cfg, "HTML_OUTPUT", default="html"))
        doxylog = "doxygen.log"
        with open(doxylog, "w") as logfile:
            subprocess.check_call(["doxygen", cfg], cwd=workdir, stdout=logfile, stderr=logfile)
        shutil.move(outpath, dest)
        shutil.move(doxylog, dest)
    else:
        if not tryClone:
            raise ValueError("No such directory: {0} (set 'tryclone' if you want to clone from a remote url)".format(basedir))
        else:
            from urllib.parse import urlparse
            pres = urlparse(basedir)
            if pres.scheme and pres.netloc:
                from tempfile import TemporaryDirectory
                with TemporaryDirectory() as tmpDir:
                    reponame = os.path.split(basedir)[-1].split(".")[0]
                    if len(reponame) == 0:
                        reponame = "repo"
                    repopath = os.path.join(tmpDir, reponame)
                    if recursive:
                        subprocess.check_call(["git", "clone", "--recursive", "--depth", "1", basedir, repopath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    else:
                        subprocess.check_call(["git", "clone", "--depth", "1", basedir, repopath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    runDoxygen(repopath, cfg=cfg, workdir=workdir, dest=dest, tryClone=False, recursive=False)
            else:
                raise ValueError("'{0}' represents neither an existing directory nor a valid URL".format(basedir))

class DoxygenPlugin(BasePlugin):
    config_scheme = (
        ("packages", ConfigItems(
            ("url"    , mkd.Type(str)),
            ("config" , mkd.Type(str)),
            ("workdir", mkd.Type(str)),
            )),
        ("tryclone", mkd.Type(bool, default=False)),
        ("recursive", mkd.Type(bool, default=False)),
        )

    def on_post_build(self, config):
        for pkgConf in self.config["packages"]:
            for outname, cfg in pkgConf.items():
                outpath = os.path.abspath(os.path.join(config["site_dir"], outname))
                try:
                    basedir = cfg.get("url", ".")
                    icfg = cfg.get("config")
                    logger.info("Running doxygen for {0} with {1}, saving into {2}".format(
                        (basedir if basedir != "." else "current directory"), (icfg if icfg else "default config"), outpath))
                    runDoxygen(basedir, cfg=icfg, workdir=cfg.get("workdir"), dest=outpath, tryClone=self.config["tryclone"], recursive=self.config["recursive"])                
                except Exception as e:
                    logger.error("Skipped doxygen for package {0}: {1!s}".format(outname, e))
