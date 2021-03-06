import bpy
import subprocess
import threading


from ..global_variables import thread_start_statement, thread_end_statement, thread_end_function_statement, thread_error_statement


# launch command in separate thread
def launchCommandFunction(command, debug, endfunction, *endfunction_args):

    if debug: print(thread_start_statement) #debug

    # launch command
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
    previous_line = ""

    # check on it
    while True:
        line = process.stdout.readline()

        if line != '' :
            if line != previous_line:
                if debug : print(line) #debug
            if b"Blender quit" in line :
                break
            elif b"EXCEPTION_ACCESS_VIOLATION" in line:
                if debug: print(thread_error_statement) #debug
                break
            previous_line = line
        else:
            break
    
    # when ending
    if debug: print(thread_end_statement) #debug

    if endfunction is not None:
        if debug: print(thread_end_function_statement) #debug
        endfunction(*endfunction_args)


# launch separate thread
def launchSeparateThread(arguments):
    render_thread = threading.Thread(target=launchCommandFunction, args=arguments)
    render_thread.start()