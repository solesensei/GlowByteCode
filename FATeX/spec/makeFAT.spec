# -*- mode: python -*-

block_cipher = None


a = Analysis(['pyTeX.py'],
             pathex=['C:\\prj\\Py\\FATex'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
a.datas += [ ('rsb.png', '.\\img\\rsb.png', 'DATA'), ('rsb.ico', '.\\img\\rsb.ico', 'DATA')]
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='makeFAT',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True , icon='img\\rsb.ico')
