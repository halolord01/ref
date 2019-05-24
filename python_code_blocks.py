Useful python code blocks

=================================================
Read and write from google api

import apiclient
from oauth2client import file, client, tools
import json

OAUTH_FILE = 'oauth_tesla.json'
SPREADSHEET_ID = '1nxhIDcPBXVMkPP2nDxtVGMG62AKMSXcqmOPYdwlcNSs'
RANGE_NAME = 'SUB_Front_Controller!A1:F'

# range can be much larger, just mostly covering the necessary columns 
def add_row(vals, range_):
    sort_vals = [[v] for v in vals]
    return {'range':range_,
        'values':sort_vals,
        'majorDimension':'COLUMNS'}


def write_to_Google(to_log, service):

    build_string = add_row(to_log, RANGE_NAME)
    try:
        table_data = service.spreadsheets().values().get(
            spreadsheetId = SPREADSHEET_ID, 
            range = RANGE_NAME)

        appended = service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME,
            body=build_string,
            valueInputOption='RAW')
        appended.execute()
        
    except Exception as e:
        logger.warning('Tried to print to Google but error: ')
        logger.warning(e)


store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets(OAUTH_FILE, SCOPES)
    creds = tools.run_flow(flow, store)
service = build('sheets', 'v4', http=creds.authorize(Http()))

=================================================
Building executiables using pyinstaller




subprocess.run('pyinstaller {specFile} --distpath {destinationPath}' stdout = sys.stdout)



replace everything in the spec file below with the approprate replacements

SPEC FILE: generic.spec
--------------------------------------------------------
# -*- mode: python -*-
block_cipher = None
a = Analysis(['{MAIN_SOURCE_FILE}'],
             pathex=['{TOP_LEVEL_FOLDER}'],
             binaries=[],
             datas=[('{DATA_FILE_OR_FOLDER_1}', '{FOLDER_FILE_EXISTS_IN}'),
             ('../resources/templateLong.zpl', 'resources'),
             ('../resources/templateHCU.zpl', 'resources')],
             hiddenimports=[],
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
          name='{PROGRAM_NAME}',
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
               name='{PROGRAM_PATh_TO_SAVE}')
--------------------------------------------------------
=================================================
Config Files
import configparser
# config.ini

[DEFAULT]
toolIP: 10.180.184.33
sheetID = 1nxhIDcPBXVMkPP2nDxtVGMG62AKMSXcqmOPYdwlcNSs
rangeName = SUB_Front_Controller!A1:F
printerName = FC_Printer_GA4
scanLog = ~/Desktop/Front_Controller_Local_Log.csv
log = ~/Desktop/Front_Controller_Scanning_log.txt

[second]
data: 0
logMe: 1



config = configparser.ConfigParser()
config.read('config.ini')

toolIp = config['DEFAULT']['toolIP']
data = config['second']['data']
logMe = config['second'].getboolean('logMe')

config.sections()   | ['DEFAULT', 'second']

------------------------------------ bit parsing ------------------------------------

from struct import unpack

msg = b'0118006500100000000001000000169102L000001713\x00'


header_names = [
'Length',
'MID',
'Rev',
'ACKFlag',
'Res',
]

header_str = '4s4s3s1s8s'

lengths_61 = [4,2,25,25,2,3,4,4,1,1,1,6,6,6,6,5,5,5,5,19,19,1,10]
lengths_61_string = [str(x) + 's' for x in lengths_61]
format_61_str = header_str + '2x' + '2x'.join(lengths_61_string)


# Generic interface for creating the dict names
def _unpack_msg(len_msg_id_lengths):
    msg_ids = ['{:02d}'.format(x + 1) for x in range(len_msg_id_lengths)]
    msg_ids = header_names + msg_ids
    return msg_ids

# pack the message IDs with the unpacked data
def _make_msg_dict(msg_ids, unpacked_data):
    return dict(((k, v.decode('ASCII')) for (k,v) in zip(msg_ids, unpacked_data)))


# unpack msg 61 and return a dictionary
def parse_msg_61(msg):
    try:
        msg_ids = _unpack_msg(len(lengths_61))
        #NOTE: The msg[:-1] is because the guns put an end character
        unpacked_data = unpack(format_61_str, msg[:-1])
        return _make_msg_dict(msg_ids, unpacked_data)
    except Exception as E:
        print(E)
        return None

=================================================
Zebra printer with 2 lines and 1 QR

from zebra import zebra

label = re.sub("{_PRODUCTNO_GENERATED_}", pn[1:], label)
label = re.sub("{_SERIALNO_GENERATED_}", sn[1:], label)   

zeb.output(label)

template.zpl:'''
^XA
^MMT
^PW324
^LL0121
^LT20
~SD20
^BY54,54^FT27,86^BXN,3,200,0,0,1
^FH\^FDP{_PRODUCTNO_GENERATED_}:S{_SERIALNO_GENERATED_}^FS
^FT100,73^A0N,19,16^FH\^FD(S) {_SERIALNO_GENERATED_}^FS
^FT100,45^A0N,19,16^FH\^FD(P) {_PRODUCTNO_GENERATED_}^FS
^PQ1,0,1,Y^XZ
'''
=================================================
http://python-jenkins.readthedocs.io/en/latest/examples.html

RUNNING JENKINS FROM PYTHON
install python-jenkins --> import jenkins

from IDE: 
execfile('.py_jenkins.py') --> loads server info, in ~/ dirser

server = jenkins.Jenkins(url, username = '', password = '')
server.get_jobs()
server,build_job(jobName, {'param1': 'ans'})
(params we use)  {'NODE_TO_RUN_ON': 'master'}
server.delete_job('job_name')

nodes
server.create_node('slave1')
nodes= get_nodes
server.get_nodes()
.enable_node('name')   --   .disable_node('name')
.get_node_info('node_name')

queues
queue_info = .get_queue_info()
id = queue_info[0].get('id')
server.cancle_queu(id)

============================================================
--- argument parsing ---

Standard: 
sys.argv --> tuple of input arguments, accessable from anywhere

Advaned : arg parser
import argparse

*** Baseline arguments ***
parser = argparse.ArgumentParser(description = 'Parsing stuff')
parser.add_argument('-i', '--input', nargs='+', type=str, required = True)
parser.add_argument('-t', '--test', action = 'store_true')
parser.add_argument('-f', '--file-name', default='compiled_reciepts.csv')
parser.add_argument('-o', '--out', type=str, default='processed_files')

args = parser.parse_args()

See Python_reference for full description and class
====================================================================
Logging

log = logging.getLogger('this')
fh = logging.FileHandler(os.path.expanduser('~/Desktop/TTTTT.txt'))
log.setLevel(10)
log.addHandler(fh)

log.info('data')
====================================================================
Dot dictionaries

simpler use of dictionaries (ie d.var instead of d['var']) (is NOT recursive)
class Bunch(object):
  def __init__(self, adict):
    self.__dict__.update(adict)
  def repr__(self):  # optional one for formatted printing
    return '%s' % str('\n'.join('%s : %s' % (k, repr(v)) for (k, v) in self.__dict__.iteritems()))


x = Bunch(**d)
x.key

# RECURSIVE DICT FORM
class DotDict(dict):
    """
    a dictionary that supports dot notation 
    as well as dictionary access notation 
    usage: d = DotDict() or d = DotDict({'val1':'first'})
    set attributes: d.val2 = 'second' or d['val2'] = 'second'
    get attributes: d.val2 or d['val2']
    """
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, dct):
        for key, value in dct.items():
            if hasattr(value, 'keys'):
                value = DotDict(value)
            self[key] = value

x = DotDict(d)

====================================================================
Misc 

--- Progress bar ----
  if loop%(max_messages/10) ==0:
      print(':-- {:2}% done parsing bag'.format(percent))
      percent += 10
  loop += 1

====================================================================
Modules

# modularity
all_modules = []
for m in modules_folder.__all__:
all_modules.append(__import__('afs_reportgenerator.modules.' + m, fromlist=['stuff']))
active_mods = [m.Module() for m in all_modules]


for mod in active_mods:  
  req_data = {k:info[k] for k in mod.data_key_requests}
  mod.data.update(req_data)
  mod.process_data()
  info = dict_meld(info, mod.update_dict())
return info, active_mods


--- ECEF Convertions ---
import pyproj
ECEF = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
LLA = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')

====================================================================
PDF reports

import PIL
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.platypus import BaseDocTemplate, Paragraph, Spacer, Frame, PageTemplate, PageBreak
from reportlab.platypus.figures import ImageFigure
from reportlab.platypus.flowables import Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

import report # sub podule that has the main report tools
# establish the report
r = report.ReportGenerator('report_name.pdf')
r.add_title('title')
r.add_plot(plot_or_list, list_=True)
r.generate_report()

====================================================================
Save tables of data

t_data = [[data], [column_labels], 'center']
plt.axis('off')
plt.grid('off')
table = plt.table(cellText = table_data[0], colLabels = table_data[1], loc = table_data[2])
table.auto_set_font_size(False)
table.set_fontsize(10)
# table.scale(1.25,2)
plt.gcf().canvas.draw()
points = table.get_window_extent(plt.gcf()._cachedRenderer).get_points()
# points[0,:] -= 10; points[1,:] += 10
nbbox = matplotlib.transforms.Bbox.from_extents(points/plt.gcf().dpi)
if flag == 'states':
  cellDict=table.get_celld()
  for i in range(5):
    try:
      cellDict[(0,i)]
    except:
      rows_ = i
      break
  for i in range(30):
    try:
      cellDict[(i,0)]
    except:
      cols_ = i
      break

  for i in range(1, rows_):
    if len(cellDict[(1,i)].get_text().get_text()) < 10:
      for j in range(cols_):
        cellDict[(j,i)].set_width(0.15)
    if len(cellDict[(1,i)].get_text().get_text()) > 20:
      for j in range(cols_):
        w = cellDict[(j,i)].get_width()
        cellDict[(j,i)].set_width(w + 0.1)

plt.savefig(fn, bbox_inches = nbbox, dpi = 200)
plot_info['caption'] = title


====================================================================
