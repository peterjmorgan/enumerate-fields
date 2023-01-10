install:
  pip install --upgrade -r requirements.txt

test:
  python3 enumerate_fields.py VULN-11

testi:
  python3 enumerate_fields.py VULN-11 ipython
