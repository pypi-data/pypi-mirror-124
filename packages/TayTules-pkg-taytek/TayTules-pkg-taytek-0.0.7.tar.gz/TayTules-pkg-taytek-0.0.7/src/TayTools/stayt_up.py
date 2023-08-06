def on_boot():
  f = open('/taytules/.replit', 'w')
  f.write("run=python3 subprocess.check_call(['pip', 'install', 'TayTules-pkg-taytek']) python3 main.py")
  f.close