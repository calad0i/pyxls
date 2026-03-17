project('pyxls', 'cpp',
  version: run_command('python3', 'tools/gitversion.py', check: true).stdout().strip(),
  meson_version: '>=1.9.0',
  default_options: ['buildtype=release', 'cpp_std=c++20'],
  license: 'LGPL-3.0-only',
)

py = import('python').find_installation(pure: false)

vcs_tag(
  command: ['python3', 'tools/gitversion.py'],
  input: 'src/xls/_version.py.in',
  output: '_version.py',
  install_dir: py.get_install_dir() / 'xls',
  replace_string: '@VCS_TAG@',
  install: true,
)


# Priority: -Dlibxls_dir=<path> > LD paths > src/xls/_blob
# Use -Dskip_libxls=true to skip the check entirely (e.g. sdist builds).
cc = meson.get_compiler('cpp')
fs = import('fs')
_libxls_dir_opt = get_option('libxls_dir')
_blob_dir = meson.current_source_dir() / 'src/xls/_blob'
_blobs_install_dir = py.get_install_dir() / 'xls' / '_blob'

if get_option('skip_libxls')
  libxls_dep = declare_dependency(
    include_directories: include_directories('src/include'),
  )
elif _libxls_dir_opt != ''
  libxls_dep = declare_dependency(
    link_args: ['-L' + _libxls_dir_opt, '-lxls'],
    include_directories: include_directories('src/include'),
  )
  install_data(_libxls_dir_opt / 'libxls.so', install_dir: _blobs_install_dir)
else
  # LD paths or local dev
  _sys_libxls = cc.find_library('xls', required: false)
  if _sys_libxls.found()
    libxls_dep = declare_dependency(
      dependencies: _sys_libxls,
      include_directories: include_directories('src/include'),
    )
  elif fs.exists(_blob_dir / 'libxls.so')
    libxls_dep = declare_dependency(
      link_args: ['-L' + _blob_dir, '-lxls', '-Wl,-rpath,' + _blob_dir],
      include_directories: include_directories('src/include'),
    )
    install_data(_blob_dir / 'libxls.so', install_dir: _blobs_install_dir)
  else
    error('libxls.so not found. Set -Dlibxls_dir=<path>, install libxls system-wide, or place it in src/xls/_blob/.')
  endif
endif

nanobind_dep = dependency('nanobind')
omp_dep = dependency('openmp')

_limited_abi = ''

binder_bin = py.extension_module(
  'raw',
  sources: [
    'src/source/_raw.cpp',
    'src/source/_c_api.cpp',
    'src/source/_ir_builder.cpp',
    'src/source/_dslx.cpp',
    'src/source/_vast.cpp',
  ],
  dependencies: [nanobind_dep, omp_dep, libxls_dep],
  include_directories: include_directories('src/source'),
  install: true,
  install_rpath: '$ORIGIN/_blob',
  subdir: 'xls',
  limited_api: _limited_abi,
)

install_data('LICENSE', install_dir: py.get_install_dir() / 'xls')
install_subdir('src/xls', install_dir: py.get_install_dir(), exclude_files: ['_version.py.in'])


stubgen = nanobind_dep.get_variable('stubgen')

gen_stubs_helper = files('tools/gen_stubs.py')

custom_target(
  'raw_stubs',
  output: 'raw',
  depends: binder_bin,
  build_by_default: true,
  command: [py, gen_stubs_helper, stubgen, '@OUTDIR@', '0'],
  install: true,
  install_dir: py.get_install_dir() / 'xls',
)

custom_target(
  'wrap_stubs',
  output: ['_c_api.pyi', '_ir_builder.pyi'],
  depends: binder_bin,
  build_by_default: true,
  command: [py, gen_stubs_helper, stubgen, '@OUTDIR@', '1'],
  install: true,
  install_dir: [py.get_install_dir() / 'xls',py.get_install_dir() / 'xls'],
)
