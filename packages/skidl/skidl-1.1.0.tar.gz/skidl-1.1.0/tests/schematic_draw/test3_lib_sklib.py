from skidl import SKIDL, TEMPLATE, Alias, Part, Pin, SchLib

SKIDL_lib_version = '0.0.1'

test3_lib = SchLib(tool=SKIDL).add_parts(*[
        Part(**{ 'name':'GND', 'dest':TEMPLATE, 'tool':SKIDL, 'move_box':<skidl.coord.BBox object at 0x7f990ac8ca90>, 'datasheet':'', 'tool_version':'kicad', '_match_pin_regex':False, 'keywords':'power-flag', 'region':<skidl.arrange.Region object at 0x7f990ac8c640>, 'description':'Power symbol creates a global label with name "GND" , ground', 'value_str':'GND', 'ref_prefix':'#PWR', 'num_units':1, 'fplist':[], 'do_erc':True, 'aliases':Alias(), 'pin':None, 'footprint':None, 'pins':[
            Pin(num='1',name='GND',func=Pin.types.PWRIN,do_erc=True)] }),
        Part(**{ 'name':'VCC', 'dest':TEMPLATE, 'tool':SKIDL, 'move_box':<skidl.coord.BBox object at 0x7f990ac8c070>, 'datasheet':'', 'tool_version':'kicad', '_match_pin_regex':False, 'keywords':'power-flag', 'region':<skidl.arrange.Region object at 0x7f990ac8c640>, 'description':'Power symbol creates a global label with name "VCC"', 'value_str':'VCC', 'ref_prefix':'#PWR', 'num_units':1, 'fplist':[], 'do_erc':True, 'aliases':Alias(), 'pin':None, 'footprint':None, 'pins':[
            Pin(num='1',name='VCC',func=Pin.types.PWRIN,do_erc=True)] }),
        Part(**{ 'name':'NCS2325D', 'dest':TEMPLATE, 'tool':SKIDL, 'datasheet':'http://www.ti.com/lit/ds/symlink/opa2197.pdf', 'tool_version':'kicad', 'symtx':'V', '_match_pin_regex':False, 'keywords':'dual opamp rtor', 'description':'Dual 36V, Precision, Rail-to-Rail Input/Output, Low Offset Voltage, Operational Amplifier, SOIC-8', '_aliases':Alias({'OPA2197xD', 'AD8676xR', 'OPA2156xD', 'MCP6L02x-xSN', 'OPA2196xD', 'OPA1692xD', 'NCS20072D'}), 'value_str':'NCS2325D', 'ref_prefix':'U', 'num_units':3, 'fplist':['SOIC*3.9x4.9mm*P1.27mm*'], 'do_erc':True, 'aliases':Alias({'OPA2197xD', 'AD8676xR', 'OPA2156xD', 'MCP6L02x-xSN', 'OPA2196xD', 'OPA1692xD', 'NCS20072D'}), 'pin':None, 'footprint':None, 'pins':[
            Pin(num='1',name='~',func=Pin.types.OUTPUT,do_erc=True),
            Pin(num='2',name='-',func=Pin.types.INPUT,do_erc=True),
            Pin(num='3',name='+',func=Pin.types.INPUT,do_erc=True),
            Pin(num='5',name='+',func=Pin.types.INPUT,do_erc=True),
            Pin(num='6',name='-',func=Pin.types.INPUT,do_erc=True),
            Pin(num='7',name='~',func=Pin.types.OUTPUT,do_erc=True),
            Pin(num='4',name='V-',func=Pin.types.PWRIN,do_erc=True),
            Pin(num='8',name='V+',func=Pin.types.PWRIN,do_erc=True)] }),
        Part(**{ 'name':'R_US', 'dest':TEMPLATE, 'tool':SKIDL, 'move_box':<skidl.coord.BBox object at 0x7f990ac8c550>, 'tx_ops':'L', 'datasheet':'~', 'tool_version':'kicad', 'symtx':'L', '_match_pin_regex':False, 'keywords':'R res resistor', 'region':<skidl.arrange.Region object at 0x7f990ac87dc0>, 'description':'Resistor, US symbol', 'value_str':'4K7', 'ref_prefix':'R', 'num_units':1, 'fplist':['R_*'], 'do_erc':True, 'aliases':Alias(), 'pin':None, 'footprint':None, 'pins':[
            Pin(num='1',name='~',func=Pin.types.PASSIVE,do_erc=True),
            Pin(num='2',name='~',func=Pin.types.PASSIVE,do_erc=True)] })])