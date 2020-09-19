class StateDict(dict):
    def __getitem__(self, value):
        try:
            return super().__getitem__(value)
        except KeyError:
            return 0  # default (in/out)put value


class State:

    def __init__(self, hardware):
        self._reset_input(hardware.inputs)
        self._reset_output(hardware.outputs)

    @property
    def input(self):
        return self._input

    @property
    def output(self):
        return self._output

    @property
    def input_type(self):
        return self._input_type

    @property
    def output_type(self):
        return self._output_type

    def _reset_input(self, inputs):
        self._input_type = inputs
        self.clear_input()

    def _reset_output(self, outputs):
        self._output_type = outputs
        self.clear_output()

    def clear_input(self):
        self._input = StateDict()  # dict(input code -> input value)
        # In MATLAB: [0] * hardware.n_inputs

    def clear_output(self):
        self._output = StateDict()  # dict(output code -> output value)
        # In MATLAB: [0] * (hardware.n_outputs + 3)
