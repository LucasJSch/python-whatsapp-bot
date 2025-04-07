import json

class StateMachine:
    INITIAL_STATE = "initial_state"
    def __init__(self, json_data):
        self.state_machine = json.loads(json_data)
        self.current_state = self.get_initial_state()

        # TODO: Add verifications

    def get_initial_state(self):
        return self.state_machine.get(self.INITIAL_STATE)

    def get_message(self, state):
        if state in self.state_machine:
            return self.state_machine[state].get("message", [])
        else:
            raise KeyError(f"State '{state}' not found in the state machine.")

    def get_menu(self, state):
        if state in self.state_machine:
            return self.state_machine[state].get("menu", {})
        else:
            raise KeyError(f"State '{state}' not found in the state machine.")

    def get_next_state(self, state):
        if state in self.state_machine:
            menu = self.state_machine[state].get("menu", {})
            return menu.get("next_state", [])
        else:
            raise KeyError(f"State '{state}' not found in the state machine.")

    def get_all_states(self):
        return list(self.state_machine.keys())

if __name__ == "__main__":
    # Example JSON string representing the updated state machine
    json_data = '''
    {
        "initial_state": "state_a",
        "state_a": {
            "message": ["text123"], 
            "menu": {
                "messages": ["i want b", "i want c"], 
                "next_state": ["state_b", "state_c"]
            }
        },
        "state_b": {
            "message": ["that's all"]
        }
    }
    '''

    # Instantiate the class with the JSON data
    state_machine = StateMachine(json_data)

    # Example of how to use the class methods:
    print(state_machine.get_initial_state())  # Output: 'state_a'
    print(state_machine.get_message("state_a"))  # Output: ['text123']
    print(state_machine.get_menu("state_a"))  # Output: {'messages': ['i want b', 'i want c'], 'next_state': ['state_b', 'state_c']}
    print(state_machine.get_next_state("state_a"))  # Output: ['state_b', 'state_c']
    print(state_machine.get_all_states())  # Output: ['initial_state', 'state_a', 'state_b']


