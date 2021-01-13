from .profit_solver import ProfitSolver
from .recursive_profit_solver import RecursiveProfitSolver
from os import path, getcwd

import linecache

class CaseHandler:
    """
    Class object that handles the content of the input file and 
    feeds cases to the ProfitSolver
    """
    def __init__(self, filename, print_descriptions = False):
        """
        Initializes the CaseHandler object
        inputs:
            <filename> :: String - relative path to file from current folder
            <print_description> :: Boolean - checker function prints results when True
        outputs:
            None
        """
        self.filename = filename
        self.print_descriptions = print_descriptions

    def line_parser(self, input_line):
        """
        Parses a line from a generic input file
        input:
            <input_line> :: String
        outputs:
            <out> :: List<Int> - 3-elem (context of case) or 4-elem (machine description) list
            <out> :: List<Empty> - if line not parsed (neg. numbers or non-Int value found)
        """
        try:
            if "-" in input_line:
                return []
            else:
                parsed_line = list(map(int, input_line.strip().split()))
                if len(parsed_line) in [3, 4]:
                    return parsed_line 
                else:
                    return []
        except ValueError:
            return []

    def case_caching(self, location_in_input):
        """
        Extracts from the input the list of elements that build a single case.
        input:
            <location_in_input> :: Int - current line where the cacher starts in the input file
        output:
            <out> :: Tuple(<0>, <1>, <2>, <3>)
                <0> :: Bool - To proceed or not after the case is solved (i.e. end of input file not reached)
                <1> :: Int - new location in input
                <2> :: List<Int> - context of case (N, C, D1)
                <3> :: List<List<Int>> - List of machine descriptions (D2, P, R, G)
        N: number of machines, C: cash at hand, D1: days of restructuring
        D2: day of availability, P: acquisition price, R: resell price, G: daily profit
        """
        # Cashes the line of input at the current location
        first_line = linecache.getline(self.filename, location_in_input)
        # If empty: Returns empty result with Stop instruction
        if first_line  in ["", "0 0 0", "0 0 0\n"]:
            return False, location_in_input, [], []
        else:
            # Parses the context of the current profit maximization case
            case_context = self.line_parser(first_line)
            # If the context is not formated properly (length is not 3): Returns empty result and GoTo next line
            if len(case_context) != 3:
                return True, location_in_input+1, [], []
            else:
                # Cashes the descriptions of the machines available in the case
                number_of_machines = case_context[0]
                number_of_restructuring_days = case_context[2]
                machines = [] # Initializing the list of machine information within the case
                # Iterates through the next <number_of_machine> lines and parses them
                for machine in range(location_in_input+1, location_in_input+number_of_machines+1):
                    # 1. Parses the characteristic D2, P, R, G of a machine 
                    machine_context = self.line_parser(linecache.getline(self.filename, machine))
                    # 2. Exits if a line supposed to be a machine does not parse well
                    if machine_context == [] or len(machine_context) != 4: 
                        return True, location_in_input+number_of_machines+1, [], []
                    # 3. Excludes machines that are available after the restructuring day
                    # 4. Appends the characteristics D2, P, R, G if no issue found
                    elif machine_context[0] <= number_of_restructuring_days:
                        machines.append(machine_context)

        return True, (location_in_input+number_of_machines+1), case_context, machines

    def content_handler(self, maximum_number_of_acquisitions=None):
        """
        Processes the input file and print the result (maximum profit) of each complete case found
        input:
            <maximum_number_of_acquisitions> :: Int - for testing, allows to reduce the number of permutations
        output:
            <out> :: List<Int> - List of maximum profit per case found
        """ 
        try:
            # Checks whether the given to the object is avaiable/accessible
            assert(self.check_file_exists()), "File not found/usable"
            assert(self.check_file_nonempty()), "File is empty"
            # Initializes counters for the current case, and current location in the input file 
            # /!\ the linechart.getline method starts at 1
            current_case = 1
            current_line = 1
            # Initializes the list of profits to be returned
            profits = []
            # Runs as long at the case_cashing method outputs a True value in the first member of its output
            while True:
                go_to_next_case, current_line, case_context, machines = self.case_caching(current_line)
                if case_context == []: # parsing error
                    if machines == []:
                        result = "Error in the case found while parsing the machine descriptions"
                    else:
                        result = "Error in the case found while parsing the context of the case"
                else:
                    # result = RecursiveProfitSolver(case_context, machines)
                    # result.solver() # Max recursion depth reached on tests_runtime
                    result = ProfitSolver(case_context, machines)
                    result.solver(maximum_number_of_acquisitions) # Solves the case in exponential time /!\
                    result = result.maximum_profit
                if go_to_next_case:
                    profits.append(result)
                    print(f"Case {current_case}: {result}")
                    current_case += 1
                else:
                    break
            return profits
        except AssertionError:
            print("Wrong initialization of the object")

    def check_filename(self):
        """
        Checks whether the input filename is a textfile
        """
        if self.filename == None:
            if self.print_descriptions:
                print("filename not provided")
            return False
        elif isinstance(self.filename, str) != True:
            if self.print_descriptions: 
                print("filename check: provided filename not receivable") 
            return False
        elif self.filename.endswith(".txt"): 
            if self.print_descriptions: 
                print("filename check: right format ")
            return True
        else:
            if self.print_descriptions: 
                print("filename check: wrong file format (need .txt)")
            return False

    def check_file_exists(self):
        """
        Checks if the file exists
        """
        if self.check_filename():
            if path.exists(self.filename):
                if self.print_descriptions: 
                    print(f"{self.filename} found in {getcwd()}")
                return True
            else:
                if self.print_descriptions: 
                    print(f"{self.filename} not found in {getcwd()}")
                return False
        return False

    def check_file_nonempty(self):
        """
        Checks if the file is empty
        """
        if self.check_filename():
            if path.getsize(self.filename) > 0:
                if self.print_descriptions: 
                    print(f"{self.filename} is non-empty")
                return True
            else:
                if self.print_descriptions: 
                    print(f"{self.filename} is empty")
                return False
        return False