
class Mass:
    AAMass = {'A': 71.0371138,
              'C_': 103.00918,
              'C': 160.0306481,
              'D': 115.0269429,
              'E': 129.042593,
              'F': 147.0684139,
              'G': 57.0214637,
              'H': 137.0589118,
              'I': 113.0840639,
              'K': 128.094963,
              'L': 113.0840639,
              'M': 131.0404846,
              'N': 114.0429274,
              'P': 97.0527638,
              'Q': 128.0585774,
              'R': 156.101111,
              'S': 87.0320284,
              'T': 101.0476784,
              'V': 99.0684139,
              'W': 186.0793129,
              'Y': 163.0633285
              }

    ProtonMass = 1.0072766  # H+
    IsotopeMass = 1.003

    ElementMass = {'C': 12.,
                   'H': 1.0078250321,
                   'O': 15.9949146221,
                   'N': 14.0030740052,
                   }

    CompoundMass = {
        'H2O': ElementMass['H'] * 2 + ElementMass['O'],
        'NH3': ElementMass['N'] + ElementMass['H'] * 3,
    }

    ModificationMass = {'Carbamidomethyl': 57.0214637,
                        'C[Carbamidomethyl]': 57.0214637,
                        'Oxidation': ElementMass['O'],
                        'M[Oxidation]': ElementMass['O'],
                        'TMT': 229.1629,
                        '1': 147.0353992,  # M[16]
                        '2': 167.03203,  # S[80]
                        '3': 181.04768,  # T[80]
                        '4': 243.06333,  # Y[80]
                        }

# C[Carbamidomethyl] = 103.00918 + 57.0214637
# M[Oxidation] = 131.04048 + 16

# H2O + H+ -> 'e'
# H+ -> 'h'
