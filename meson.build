project('xls-python', 'cpp',
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


# Handle libxls.so blob
blobs_dir = py.get_install_dir() / 'xls' / '_blob'
install_data('src/xls/_blob/libxls.so', install_dir: blobs_dir)

# Define libxls dependency
# We link against the prebuilt library in src/xls/_blob
libxls_dir = meson.current_source_dir() / 'src/xls/_blob'
libxls_dep = declare_dependency(
  link_args: ['-L' + libxls_dir, '-lxls', '-Wl,-rpath,' + libxls_dir],
  include_directories: include_directories('src/include')
)

nanobind_dep = dependency('nanobind')
omp_dep = dependency('openmp')

_limited_abi = py.language_version().version_compare('>=3.12') ? '3.12' : ''

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
