import os
import sys
import time
import logging
import subprocess


class CasesNotMatchError(Exception):
    pass


class CasesNotFoundError(Exception):
    pass


class NoStdinError(Exception):
    pass


class checker:
    def __init__(self, input_data: dict, output_data: dict, gcc_path: str = "/usr/bin/g++", run_path: str = "/root/", extra_args: list = ["-lm"], check_float=False, ignore_space=True, time_limit=1.0, memory_limit="1G"):
        self.gcc_path = gcc_path
        self.input_data = input_data
        self.output_data = output_data
        if not os.path.exists(gcc_path):
            logging.error("Can't Find gcc")
            raise FileNotFoundError
            # return None
        self.gcc_path = gcc_path
        if not os.path.exists(run_path):
            logging.error("Can't Find buildpath")
            raise FileNotFoundError
        self.run_path = run_path
        self.extra_args = extra_args
        self.check_float = check_float
        #todo check float value is equal with different decimal places
        self.ignore_space = ignore_space
        self.time_limit = time_limit
        self.memory_limit = memory_limit
        # todo:limit_memory
        if set(input_data.keys()) != set(output_data.keys()):
            logging.error("Test Cases not match")
            raise CasesNotMatchError
        for key in input_data:
            data = input_data[key]
            if key not in output_data:
                raise CasesNotMatchError
            if "stdin" not in data:
                raise NoStdinError

        '''
        input_data_case:dict
        {
            "test_case_name":{
                "stdin":""
                "file on the same path":""
            }
        }
        output_data_case:dict
        {
            "test_case_name":{
                "stdout":""
                "file on the same path":""
            }
        }
        '''

    def get_filename(self, filepath):
        return filepath.split("/")[-1]

    def write_file(self, cpp_filename, extra_files=[]):
        try:
            fp = open(cpp_filename, "r")
            cpp_file = fp.read()
            fp.close()
        except FileNotFoundError:
            logging.error("Can't read CPP Files.")
            return {
                "status": False,
                "msg": "Can't Open CPP file."
            }
        cpp_file_in_lines = cpp_file.split("\n")
        int_main_line = -1
        first_program_line = -1
        for i in range(0, len(cpp_file_in_lines)):
            line = cpp_file_in_lines[i]
            line = line.strip()
            line_words = line.split()
            if len(line_words) >= 2:
                if line_words[0] == "int" and line_words[1].startswith("main") and not line_words[-1].endswith(";"):
                    int_main_line = i
                    if line_words[-1][-1] == '{':
                        first_program_line = i
                        break
                    elif cpp_file_in_lines[i+1].split()[0][0] == '{':
                        first_program_line = i+1
                        break
        if int_main_line == -1:
            logging.error("Can't Find main function.")
            return{
                "status": False,
                "msg": "Can't find main function"
            }
        cpp_file_in_lines[first_program_line] = cpp_file_in_lines[first_program_line] + \
            "\n    freopen(\"stdin\",\"r\",stdin);\n    freopen(\"stdout\",\"w\",stdout);\n"
        new_cpp_file = "\n".join(cpp_file_in_lines)
        fp = open(self.run_path+self.get_filename(cpp_filename), "w")
        fp.write(new_cpp_file)
        fp.close()

        return{
            "status": True
        }

    def compiling(self, orgfilename):
        filename = orgfilename.split("/")[-1]
        command = [self.gcc_path, self.run_path+filename, "-o",
                   self.run_path+filename.split(".")[0]+".o"] + self.extra_args
        try:
            subprocess.check_output(command, cwd=self.run_path)
        except subprocess.CalledProcessError as e:
            return {
                "status": False,
                "msg": "Complited Error!"
            }
        return {
            "status": True,
            "execfile": filename.split(".")[0]+".o"
        }

    def clear_testfile(self, test_case_name):
        if not test_case_name in self.input_data:
            raise CasesNotFoundError
        input_case = self.input_data[test_case_name]
        output_case = self.output_data[test_case_name]
        for filename in output_case:
            try:
                os.remove(self.run_path+filename)
            except:
                pass
        for filename in input_case:
            try:
                os.remove(self.run_path+filename)
            except:
                pass

    def run_a_task(self, execfile, test_case_name):
        if not test_case_name in self.input_data:
            raise CasesNotFoundError
        input_case = self.input_data[test_case_name]
        output_case = self.output_data[test_case_name]
        self.clear_testfile(test_case_name)
        for filename in input_case:
            text = input_case[filename]
            fp = open(self.run_path+filename, "w")
            fp.write(text)
            fp.close()
        command = [self.run_path+execfile]
        # todo:use docker to instead of shell to avoid someone use system("shutdown 0")
        try:
            #start_time = time.time()
            subprocess.check_output(
                command, timeout=self.time_limit, cwd=self.run_path)
            #end_time = time.time()
        except subprocess.TimeoutExpired as e:
            self.clear_testfile(test_case_name)
            return{
                "status": False,
                "type": "TLE"
            }
        except subprocess.CalledProcessError as e:
            cmd = e.output
            returncode = e.returncode
            self.clear_testfile(test_case_name)
            return {
                "status": False,
                "errorcode": returncode,
                "type": "RE",
                "msg": "Runtime Error(maybe call some unexist memory)"
            }
        is_correct = True
        error_file = []
        for filename in output_case:
            text = output_case[filename]
            try:
                fp = open(self.run_path+filename, "r")
            except FileNotFoundError:
                return {
                    "status": False,
                    "type": "NO_FILE"
                }
            now_text = fp.readlines()
            correct_text = text.split("\n")
            if len(now_text) != len(correct_text):
                is_correct = False
                error_file.append(filename)
                continue
            for i in range(0, len(now_text)):
                if self.ignore_space:
                    now_line = now_text[i].strip()
                    correct_line = correct_text[i].strip()
                else:
                    now_line = now_text[i]
                    correct_line = correct_text[i]
                if now_line != correct_line:
                    is_correct = False
                    error_file.append({"filename": filename, "text": now_text})
                    break
        if is_correct:
            self.clear_testfile(test_case_name)
            return {"status": True}
        else:
            self.clear_testfile(test_case_name)
            return {"status": False,
                    "type": "WA",
                    "error_files": error_file
                    }

    def autojudge(self, filename):
        res = self.write_file(filename)
        if res["status"] == False:
            return res
        res_comp = self.compiling(filename)
        if res_comp["status"] == False:
            res_comp["type"] = "CE"
            return res_comp
        res_final = {
            "status": True,
            "correct_cases": 0,
            "all_cases": len(self.input_data)
        }
        for case in self.input_data:
            res_run = self.run_a_task(res_comp["execfile"], case)
            if res_run["status"] == False:
                res_final["status"] = False
                if "error_data" not in res_final:
                    res_final["error_data"] = []
                res_run["case"] = case
                res_final["error_data"].append(res_run)
            else:
                res_final["correct_cases"] += 1
        try:
            os.remove(self.run_path+res_comp["execfile"])
            os.remove(self.run_path+self.get_filename(filename))
        except:
            pass
        return res_final


if __name__ == "__main__":
    pass
