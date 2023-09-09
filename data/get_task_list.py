import subprocess

if __name__ == '__main__':

    outfile = '/home/richard/gee_task_list.txt'

    with open(outfile, 'w') as f:

        command = "earthengine task list"
        proc = subprocess.Popen(command.split(" "),
                                stdout=subprocess.PIPE)
        f.write(proc.stdout.read())

    print(proc)
    print('Done!')

