
from docopt import docopt
import subprocess
import logging
import logging.handlers

logging.basicConfig(level=logging.INFO,  filename='logs.log', filemode='a', format='%(message)s  %(asctime)s', datefmt="%Y-%m-%d %T")


logger = logging.getLogger()

logger.addHandler(logging.handlers.SysLogHandler( ))


__version__ = 'Reset_1'
__revision__ = '1.2'
__deprecated__ = False


def get_args():
	"""Function to get command line arguments.

	Defines arguments needed to run this program.

	:return: Dictionary with arguments
	:rtype: dict
	"""
	
	usage = """
	Usage:
        try.py <driver> [--mode=<mode>]
		try.py --version
		try.py -h | --help

	Options:
        -h --help     Show this help message and exit.
        --mode=<mode>  Mode format (normal or hard) [default: normal].
	"""

	args = docopt(usage)
	return args	

def reset_cmd(drive, mode):
    try:
        cmd = f'/v1/drives/{drive}/reset {{"mode": {mode}}}'
        cmd = ['/opt/ITDT/itdt', '-f', drive, 'ros', 'POST', cmd]

        print(f'Driver id: {drive}')
        print(f'Reset mode: {mode}')
        print(f'Command to process: \n ~ {cmd}')
        com = ' '.join(cmd)
        print(f'Command to process: \n ~ {com}')

    
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        output, error = process.communicate()

        if output is not None:
            logging.info(f"Output: {output.decode('utf-8')}\n")
            print(output.decode('utf-8'))
            print(f"Drive {drive} successfully reseted.\n \n {output.decode('utf-8')}")
            

        if error is not None:
            logging.info(f"Error: {error.decode('utf-8')}\n")
            print(f"Error resetting drive {drive}:\n {error.decode('utf-8')}")
    
    except subprocess.CalledProcessError:
        return "Error running command."
    except FileNotFoundError:
        return "command not found."

def main(args):
    """
    
    # Example usage:
        python reset.py TAPE123 --mode hard

    """
    drive = args['<driver>']
    mode = args['--mode']
    reset_cmd(drive, mode)

if __name__ == '__main__':
    ARGS = get_args()
    main(ARGS)



