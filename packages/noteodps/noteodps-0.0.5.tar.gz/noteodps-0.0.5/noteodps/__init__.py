from notetool.secret import load_secret_str, read_secret
from odps import ODPS

load_secret_str()
access_id = read_secret(cate1='DataWorks', cate2='notechats', cate3='secret', cate4='access_id')
secret_access_key = read_secret(cate1='DataWorks', cate2='notechats', cate3='secret', cate4='access_key')
project = read_secret(cate1='DataWorks', cate2='notechats', cate3='secret', cate4='project')
endpoint = read_secret(cate1='DataWorks', cate2='notechats', cate3='secret', cate4='endpoint')
tunnel_endpoint = read_secret(cate1='DataWorks', cate2='notechats', cate3='secret', cate4='tunnel_endpoint')

opt = ODPS(access_id=access_id,
           secret_access_key=secret_access_key,
           project=project,
           endpoint=endpoint,
           tunnel_endpoint=tunnel_endpoint
           )
opt.to_global()
