class RecursiveProfitSolver:
    """
    Profit Solver using a recursive function
    """
    def __init__(self, case_context, machines):
        """
        Initializes the RecursiveProfitSolver object
        inputs:
            <case_context> :: List<Int> - context of case (N, C, D1)
            <machines> :: List<List<Int>> - List of machine descriptions (D2, P, R, G)
        N: number of machines, C: cash at hand, D1: days of restructuring
        D2: day of availability, P: acquisition price, R: resell price, G: daily profit
        outputs:
            None
        """
        self.cash_at_hand = case_context[1]
        self.number_of_restructuring_days = case_context[2]
        self.machines = sorted(machines, key=lambda x: x[0])
        self.maximum_profit = case_context[1]

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

    def recursive_solver(self, current_day, cash_at_hand, resell, daily_profit):
        """
        Recursively over the available machines at a specific time
        input:
            <cash_at_hand> :: Int - Cash ACM currently holds
            <days_to_end> :: Int - Days to go till the end of restructuring
            <resell> :: Int - Resell price of the machine currently owned
            <profit> :: Int - Profit the machine currently owned produces daily
        output:
            <out> :: Int - Accumulated profit till the end of restructuring
        """
        # lambda function to check if two days separate the currently owned machine 
        # from to currently available machine
        check_day = lambda m: m[0] > current_day+1
        # lambda function to check if switching to the available machine is a breaking-even
        # or profitable move
        solvable = lambda m: (m[0]-current_day-1)*daily_profit+cash_at_hand
        # Finds all available moves
        available_moves = list(filter(lambda m: check_day(m) and solvable(m)>=m[1], self.machines))
        # Updates the maximum profit possible if no machine switch is performed till the end
        self.maximum_profit = max(
            self.maximum_profit,
            self.profit_till_end(
                cash_at_hand, 
                self.number_of_restructuring_days-current_day, 
                resell,daily_profit
                )
        )
        # For each possible move, recurse with updating the current cash at hand
        for machine in available_moves:
            new_cash_at_hand = cash_at_hand - machine[1] + resell + daily_profit*(machine[0]-current_day-1)
            self.recursive_solver(machine[0], new_cash_at_hand, machine[2], machine[3])


    def solver(self):
        """
        Starts the solver and begins a recursion for each of the choices available to ACM with its starting cash.

        ACM's starting state (Number of machines, Cash at hand, Days of restructuring) can be 
        expressed as a machine state:
            - [Day, Cash-at-hand, Resell Price, Profit]
            - [0, cash at hand, 0, 0] ACM 'owns' a 0-value machine that earns 0 with resell price 0 at day 0

        inputs:
            <int> :: None
        outputs:
            <out> :: None
        """
        # initial_case = [-1, self.cash_at_hand, 0, 0]
        # -1 for the first element because the lambda function check_day in the
        # recursive function checks machines separated by at least 2 days (including)
        # but machines are available from day 1
        self.recursive_solver(-1, self.cash_at_hand, 0, 0)