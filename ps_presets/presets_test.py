
# BEGIN_AUTOGEN

def cooling():
    #cooling preset
    return {
        "amplitudes": {
            "397c": 0.0,
            "397b": 0.2,
            "850 RP": 0.6,
            "854 SP1": 0.9,
            "866 RP": 0.0,
        },
        "detunings": {
            "397c": 0,
            "397b": -13,
            "850 RP": 0,
            "854 SP1": 0,
            "866 RP": 0,
        },
    }

def measurement():
    #measurement preset
    return {
  "length": 2000,
  "threshold": 5,
  "amplitudes": {
    "397c": 0.1,
    "397b": 0.3,
    "866 RP": 0.05
  },
  "detunings": {
    "397c": 0.0,
    "397b": -13.0,
    "866 RP": 0.0
  },
}

def trapping():
    #trapping preset
    return {
  "amplitudes": {
    "397c": 0.4
  },
  "detunings": {
    "397c": -50
  }
}


def pump_to_stretch():
    return {
        "detunings": {},  # include if you want detuning overwrite protection for this section
        "duration": 18.0,
        "pmt_gate_high": True,
        "dds_functions": {
            "397c": (lambda t: 0.35),
            "866 OP": (lambda t: 0.50),
            "854 SP1": (lambda t: 0.20),
        },
        "phase_functions": {},  # optional
        "coincidence_detector": False,
    }


def STIRAP():

    return dict(

        name="STIRAP",

        duration=5.0,

        dds_functions={

            "397a": gaussian(mu=1.0, sigma=2.0),

            "866": gaussian(mu=1.0, sigma=3.5),

        },

        pmt_gate_high=True,

    )
# END_AUTOGEN