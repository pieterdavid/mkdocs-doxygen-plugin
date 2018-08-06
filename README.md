# MkDocs Doxygen plugin

This mkdocs plugin allows to generate Doxygen documentation as part of the build process.
Doxygen is run (post-build) for each entry in the `packages` configuration entry
(a list of mappings) and the html output moved to a subdirectory of `site_dir`,
with the same name as the entry's key.

As an example, the configuration
```yaml
plugins:
  - doxygen:
      packages:
        - doxygen:
            url : .
```
will run `doxygen` in the current project root, and move the output to `site/doxygen`.

In addition to the `url` parameter, the Doxygen configuration file (relative to `url`)
can be specified (by default `Doxyfile` and `doxygen.cfg` are searched for), as well as
the working directory (relative to the directory with the Doxygen configuration file).

`url` can be a local path as well as a remote url. In the latter case, `git clone` 
is used to get a working copy (only if enabled by setting `tryclone` to true), e.g.
```yaml
plugins:
  - doxygen:
      tryclone: yes
      packages:
        - doxygen:
            url    : .
        - doxyfwk:
            url    : https://github.com/cp3-llbb/Framework.git
            config : docs/doxygen.cfg
            workdir: . ## could be left out in this case
```
