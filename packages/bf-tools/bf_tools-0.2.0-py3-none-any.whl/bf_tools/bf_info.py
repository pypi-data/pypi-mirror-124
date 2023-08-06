#
# Copyright (c) 2021 Dilili Labs, Inc.  All rights reserved. Contains Dilili Labs Proprietary Information. RESTRICTED COMPUTER SOFTWARE.  LIMITED RIGHTS DATA.
#

from argparse import ArgumentParser
import subprocess
import requests
import json


header = [
                "Copyright (c) 2021 Dilili Labs, Inc.  All rights reserved.\n\n"
                "bf_info utility checks BrainFrame system information and all inference computing dependencies.\n"
                "=======\n"
        ]

footer = [
                "\n\n"
        ]

cmdlines = [
		"date",
		"date -u",
		"uptime",
		"uptime -s",
		"cat /etc/os-release",
		"uname -a",
		"cat /proc/cpuinfo",
		"cat /etc/docker/daemon.json",
		"nvidia-smi",
		"ls /dev/dri -l",
		"df -h",
		"which brainframe",
		"which brainframe-client",
		"brainframe info",
		"cat $(brainframe info install_path)/.env",
		"cat $(brainframe info install_path)/docker-compose.yml",
		"cat $(brainframe info install_path)/docker-compose.override.yml",
		"ls -la $(brainframe info install_path)",
		"ls -la $(brainframe info data_path)/capsules",
		"docker container ls",
		"curl http://localhost/api/version",
		"curl http://localhost/api/license",
		"curl http://localhost/api/plugins | python -mjson.tool",
		"curl http://localhost/api/streams | python -mjson.tool",
		"curl http://localhost/api/streams/status | python -mjson.tool",
		"hostname -I",
		"cat /proc/uptime",
		"nslookup aotu.ai",
		"cat /proc/uptime",
		"ping aotu.ai -c 3",
		"cat /proc/uptime",
		"date",
		"date -u",
        ]


def _parse_args():
	parser = ArgumentParser(
		"This tool will print out the system information for brainframe"
	)
	parser.add_argument(
		"-f", "--file",
		default="bf.info",
		help="The output brainframe info file name"
	)
	args = parser.parse_args()

	return args


def main():
    args = _parse_args()


    file = open(args.file, "w")

    for line in header:
        print(line)
        file.writelines(line)

    for line in cmdlines:

        bf_info = "\n======== " + line + ' ...\n'

        print(bf_info)
        file.writelines(str(bf_info))

        if line.startswith("no curl"):

            url = line.replace("no curl ", "")
            session = requests.Session()
            session.trust_env = False

            response = session.get(url)
            bf_info = json.dumps(response.json(), indent=2)
            # json.dump(bf_info, file, indent=4) # sys.stdout

        else:
            sys_process =  subprocess.Popen(line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            bf_info =  sys_process.stdout.read().decode('utf-8')

            if len(bf_info) == 0:
                bf_info = "None.\n"

        print(bf_info)
        # file.writelines(str(bf_info.encode('utf-8')))
        file.writelines(str(bf_info))

    for line in footer:
        print(line)
        file.writelines(line)

    file.close()


if __name__ == "__main__":
	main()
