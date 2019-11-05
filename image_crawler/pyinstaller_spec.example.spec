# -*- mode: python -*-
 
# if you use pyqt5, this patch must be adjusted
# https://github.com/bjones1/pyinstaller/tree/pyqt5_fix
 
block_cipher = None
 
 
a = Analysis(['image_crawler.py'],
             pathex=[r'PROJECT_ROOT'],
             binaries=[],
			 # (target folder or file, move folder)
             datas=[('./crawler_info/userinfo.ini', './crawler_info'),
					('./webdriver/*.bat', './webdriver'),
					('./webdriver/*.exe', './webdriver')],
             hiddenimports=["crawler.base_crawler",
							"crawler.pixiv_crawler",
							"crawler_info.info",
							"crawler_util.crawler_enum",
							"crawler_util.crawler_file_util",
							"crawler_util.system_logger",
							"crawler_util.system_messages",
							
							"certifi",
							"chardet",
							"cssselect",
							"display",
							"idna",
							"lxml",
							"pyperclip",
							"requests",
							"selenium",
							"urllib3",
							
							"os",
							"time",
							"subprocess",
							"threading",
							"random",
							"configparser",
							"enum",
							"shutil",
							],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='image_crawler',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='image_crawler')