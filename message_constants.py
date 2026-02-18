sensitivity=360/65536

header_to_bytes = (b'\r',b'\n',b'~')
header = b'\r\n~'

dorient = 'DORIENT'
dorient_format = '>HHHHHHHHH'
dorient_id = 112

setfil = 'SETFIL'
setfil_format = '>H'
setfil_ans_format = '>cccBBBH'
setfil_id = 113
setfil_count = 3