#!/usr/bin/env python

import os
import sys
import struct
import prettytable
import six
from textwrap import wrap

HEAD_LEN = 256
VAL_WRAP_WIDTH = 100


def _print(pt, order):
    print(pt.get_string(sortby=order))

def print_dict(print_dict, property="Property"):
    pt = prettytable.PrettyTable([property, 'Value'], caching=False)
    pt.align = 'l'
    for key, val in six.iteritems(print_dict):
        wrapped_value_lines = wrap(str(val) or '', VAL_WRAP_WIDTH) or ['']
        pt.add_row([key, wrapped_value_lines[0]])
        for subseq in wrapped_value_lines[1:]:
            pt.add_row(['', subseq])
    _print(pt, None)


def print_dict_ordered(print_dict, property="Property"):
    pt = prettytable.PrettyTable([property, 'Value'], caching=False)
    pt.align = 'l'
    for key in sorted(six.iterkeys(print_dict)):
        wrapped_value_lines = wrap(
            str(print_dict[key]) or '', VAL_WRAP_WIDTH) or ['']
        pt.add_row([key, wrapped_value_lines[0]])
        for subseq in wrapped_value_lines[1:]:
            pt.add_row(['', subseq])
    _print(pt, None)

class PeekHead(object):
    """
    We have file with head format.
    """
    def __init__(self, fname):
        if not os.path.isfile(fname):
            print "not a file"
        self.version_file = fname
        self.head_data = {}

    def get_head_data(self):
        with open(self.version_file, mode='rb') as f:
            data = f.read(HEAD_LEN)
        return data

    def verify(self, head):
        """
        verify through:
        x. signature
        x. checkvalue
        x. VerHeadSize
        x. VerHeadCrc, how to?
        """
        check_value = struct.unpack("i", head[52:56])
        if check_value != 'eaeaeaea':
            print "invalude file header, wrong checkvalue"

    def parse(self, head):
        board, x0, v_type, f_type, cpu_type = struct.unpack(">hhhhh", head[56:66])
        ver_no, pcb_no = struct.unpack("ii", head[68:76])
        make_time = struct.unpack("i", head[80:84])
        ext_ver_no = struct.unpack("i", head[100:104])
        pkg_id = struct.unpack("i", head[116:120])
        ver_name = struct.unpack("80s", head[120:200])
        body_crc = struct.unpack("i", head[204:208])
        body_len = struct.unpack("i", head[208:212])
        ext_pkg_id = struct.unpack("i", head[212:216])
        pkg_len = struct.unpack("i", head[216:220])
        pkg_make_time = struct.unpack("i", head[220:224])
        os_ver_no = struct.unpack("i", head[224:228])
        os_type = struct.unpack("c", head[228])
        patched_ver_no, patched_ver_crc = struct.unpack("ii", head[232:240])
        self.head_data.update(board_id=board, ver_type=v_type, func_type=f_type,
                              cpu_type=cpu_type, ver_no=ver_no, pcb_no=pcb_no,
                              make_time=make_time, ext_ver_no=ext_ver_no,
                              pkg_id=pkg_id, ver_name=ver_name, body_crc=body_crc,
                              body_len=body_len, ext_pkg_id=ext_pkg_id,
                              pkg_len=pkg_len, pkg_make_time=pkg_make_time,
                              os_ver_no=os_ver_no, os_type=os_type,
                              patched_ver_no=patched_ver_no,
                              patched_ver_crc=patched_ver_crc)
        return self.head_data

    def show(self):
        print "board id : %s" % self.head_data.get("board_id", "")
        print "ver type : %s" % self.head_data.get("ver_type", "")
        print "func type : %s" % self.head_data.get("func_type", "")
        print "cpu type : %s" % self.head_data.get("cpu_type", "")
        print "ver no: %s" % self.head_data.get("ver_no", "")

    def show_table(self):
        info = self.head_data.copy()
        print_dict_ordered(info)

def main():
    #if len(sys.argv) != 2:
    #    print("error imput argument")
    #    sys.exit(-1)
    #ph = PeekHead(sys.argv[1:])
    ph = PeekHead("/tmp/test.00.out")
    data = ph.get_head_data()
    # ph.verify(data)
    ph.parse(data)
    # ph.show()
    ph.show_table()


if __name__ == "__main__":
    main()

