# pyHCT
Python ADIF tool for QRPWorks logging modules

Don't have a Windows box? Don't want the Windows utility? Use this thing.

(note: not currently tested)

    usage: dump-adif.py [-h] port output

    Load ADIF from a QRPworks HCT or SideKar module.

    positional arguments:
      port        serial port to be used
      output      .adi file to be written (WILL BE OVERWRITTEN)

    optional arguments:
      -h, --help  show this help message and exit

    use 'python -m serial.tools.list_ports' to find port
