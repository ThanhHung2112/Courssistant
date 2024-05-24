import os
import subprocess
import time
from subprocess import Popen, PIPE

p = subprocess.Popen("ollama run duckdb-nsql",
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    shell=True)

out, err = p.communicate(input="CREATE TABLE TAXI (id int, cost varchar,) Which taxi have the highest cost?".encode())   

print(out)
if p.returncode != 0:
    print(out)
    print(err)