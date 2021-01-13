import itertools

class ProfitSolver:
    def __init__(self, case_context, machines):
        """
        Initializes the ProfitSolver object
        inputs:
            <case_context> :: List<Int> - context of case (N, C, D1)
            <machines> :: List<List<Int>> - List of machine descriptions (D2, P, R, G)
        N: number of machines, C: cash at hand, D1: days of restructuring
        D2: day of availability, P: acquisition price, R: resell price, G: daily profit
        outputs:
            None
        """
        self.starting_cash = case_context[1]
        self.maximum_profit = case_context[1]
        self.length_of_restructuring = case_context[2]
        self.machines = machines
        self.memory = {}

    def sorted_perms(self, machines, n=None):
        """
        Generates all sorted permutations of <machines> of max length <n>, creating "strategies"
        Checks if the first elements of the strategy are stored in memory and reuse an attached state
        Checks if the strategy breaks-even or profits (giving an end state), reusing the memory if available
        Records the strategy and its attached end state in memory
        Yields the end state of the strategy when the last machine of a strategy is acquired:
            - The end state represents ACM's finances at the end of the strategy
        
        ACM's starting state (Number of machines, Cash at hand, Days of restructuring) can be 
        expressed as a machine state:
            - [Day, Price, Resell Price, Profit]
            - [0, 0, cash at hand, 0] ACM 'owns' a 0-value machine that earns 0 with resell price 0 at day 0
        
        inputs:
            <machines> :: List<List<Int>> - List of machine descriptions (D, P, R, G)
            <n> :: Int - Maximum length of permutations authorized (used for testing)
        output:
            <out> :: Yields a machine description (D, P, R, G) -- the end state of the strategy
        """

        def is_strategy_valid(initial_state, strategy, strategy_string):
            """
            Iterates each step of the strategy (after memory if available):
                - Memorizes the end state for the whole strategy if iteration finishes
                - None if it fails at a step (i.e. it didn't break-even)
            inputs:
                <initial_state> :: List<Int> - State of ACM's finances at start of <strategy>
                <strategy> :: List<List<Int>> - List of machine descriptions (D, P, R, G)
                <strategy_string> :: String - string representation of the strategy
            outputs:
                <out> :: (List<Int>, Bool) - returns the end state if any, and a token to indicate to the solver()
                to try update the maximum_profit global variable
            """
            # Checks if each step of the strategy breaks-even or profits
            for step in strategy:
                cash_after_resell_buy = initial_state[1]+initial_state[2]-step[1]
                accumulated_profit = (max(step[0]-initial_state[0]-1,0))*initial_state[3]
                is_acquisition_valid = cash_after_resell_buy+accumulated_profit
                # if sound: update the initial state to an intermediary one
                if is_acquisition_valid >= 0:
                    initial_state = [step[0], step[2], is_acquisition_valid, step[3]]
                # if unsound: exit and memorizes the dead end
                else:
                    self.memory[strategy_string]=None
                    return None, False
            # Memorized the end state of the whole strategy
            self.memory[strategy_string]=initial_state
            return initial_state, True

        # Checks if the provided max length of permutation is acceptable, and defaults if not
        if (n==None or type(n)!=int) or (n>(self.length_of_restructuring+1)//2 or n<0):
            n = (self.length_of_restructuring+1)//2
        # Declares ACM's start state at day 0
        state_ACM_at_day_zero = [0,0,self.starting_cash,0] 
        # for each length of permutation do:
        for r in range(1, n+1):
            # clears memory of superfluous entries (length r-2). Permutations are iterated in order and end
            # states are carrried from one length of permutation to the next
            self.memory = {k: v for k, v in self.memory.items() if len(eval(k)) <= r-2}
            for strategy in itertools.permutations(machines, r):
                strategy_string = str(strategy)
                # if permutations are singletons
                if r == 1:
                    yield is_strategy_valid(state_ACM_at_day_zero, strategy, strategy_string)
                # Checks if the dates of the last two elements are ordered with 1 day between them
                elif strategy[-2][0] < strategy[-1][0]+1:
                    first_elements = str(strategy[:-1])
                    # Checks if the first elements of the permutation are absent from memory
                    if  first_elements not in self.memory.keys(): 
                        # Checks if the first elements of the permutation are sorted
                        if(all(((strategy[i][0] < (strategy[i + 1][0]+1) 
                                 for i in range(len(strategy)-1))))):                         
                            yield is_strategy_valid(state_ACM_at_day_zero, strategy, strategy_string)
                    else:
                        yield is_strategy_valid(self.memory[first_elements], [strategy[-1]], strategy_string)

    def profit_till_end(self, cash_at_hand, days_to_end, resell, profit):
        """
        Calculates the profit earned from the acquisition of a machine to end of restructuring
        input:
            <cash_at_hand> :: Int - Cash ACM currently holds
            <days_to_end> :: Int - Days to go till the end of restructuring
            <resell> :: Int - Resell price of the machine currently owned
            <profit> :: Int - Profit the machine currently owned produces daily
        output:
            <out> :: Int - Accumulated profit till the end of restructuring
        """
        return cash_at_hand + resell + days_to_end*profit

    def solver(self, maximum_number_of_acquisitions=None):
        """
        Starts the solver and consumes the result of each generated permutation of possible strategies.
        inputs:
            <maximum_number_of_acquisitions> :: Int - Maximum length of permutations authorized
        outputs:
            <out> :: None
        """
        for case, update in self.sorted_perms(self.machines, maximum_number_of_acquisitions):
            if update:
                self.maximum_profit = max(
                    self.maximum_profit,
                    self.profit_till_end(
                        case[1],
                        self.length_of_restructuring-case[0],
                        case[2],
                        case[3])
                )
