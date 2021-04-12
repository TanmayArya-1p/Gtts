from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': [], 'excludes': []}

base = 'Console'

executables = [
    Executable('main.py', base=base, targetName = 'Gtts-Converter',icon="gtts.ico")
]

setup(name='Gtts-Converter',
      version = '1',
      description = 'Convert any String to TTS and save it to a directory instantly.',
      options = {'build_exe': build_options},
      executables = executables)
