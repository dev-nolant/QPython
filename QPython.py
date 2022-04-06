import os
import re

import periodictable
from periodictable import core, density, elements, formula, mass


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def error(user_input_element, error_message):
    print(f"An error has occured[{user_input_element}]: {error_message}")


def exit_Safe(exitcode):
    print(f"Goodbye. Exit({exitcode})")
    exit(exitcode)


class QP:
    def __init__(self):
        # Define the Independent variables to be used throughout the program.
        self.neutron_weight = 1.00867
        self.proton_weight = 1.00782  # /28
        self.speed_of_light = float(2.9979) * 10 ** 8
        self.AMU = 931.5  # MeV/c^2

    @staticmethod
    def elements():
        list_of_elements = []
        for element in elements:
            list_of_elements.append(element)
        return ("ELEMENTS:\n" + str(list_of_elements))

    '''[mass defect]
    Description:
        Calculate the mass defect based on an input protons, neutrons, and relative weight.
    Output:
        Mass Defect Bool Value; Mass Defect Value; Units;
    Formula:
        Δ𝑚=𝑍𝑚𝑝+(𝐴−𝑍)𝑚𝑛−𝑚𝑛𝑢𝑐
        or
       ( The total mass of protons + total mass of neutrons ) - total relative mass of nucleus == Δ𝑚 (changing mass)
    '''

    def massdefect(self, element, charge):

        element_protons_ = (
            eval("elements."+element+"["+str(charge)+"].number"))
        element_neutrons_ = int(charge) - element_protons_

        Zmp_ = element_protons_ * self.proton_weight
        Zmn = element_neutrons_ * self.neutron_weight

        self.massdefect = (Zmp_ + Zmn) - \
            (eval("elements."+element+"["+str(charge)+"].mass"))
        self.massdefect_bool = abs(round(self.massdefect, 4)) > .0005

        return {'Mass Defect': self.massdefect_bool, 'Value': self.massdefect, 'Units': 'AMU'}

    '''[required binding energy]
    Description:
        Binding energy is the smallest amount of energy required to remove a particle
        from a system of particles or to disassemble a system of particles into individual parts.
    Output:
        Required binding energy value; Units;
    Formula:
        E = ΔM*C^2
        or
        Defect Mass * (Speed of light ^ 2) = Required Energy / Energy matter
    '''

    def binding_energy(self, element, charge):
        massdefect = self.massdefect(element, charge)['Value']
        energy_mass = massdefect * (1.6606 * 10 ** (-27))
        energy = (energy_mass * self.speed_of_light) ** 2
        return {'Value': energy, 'Units': 'Joules/Nucleon'}

    '''[energy per neutron]
    Description:
        It takes energy, called binding energy, to hold nucleons together as a nucleus. Iron has a
        mass number of 56 and is one of the most stable of all the elements. We say that iron has a
        high binding energy per nucleon. Elements with lower and higher mass numbers per nucleon are less stable..
    Output:
        Individual Neutorn Energy Value; Units;
    Formula:
        E = ΔM*C^2
        or
        Defect Mass * (Speed of light ^ 2) = Required Energy / Energy matter
    '''

    def neutron_energy(self, element, charge):
        element_protons_ = (
            eval("elements."+element+"["+str(charge)+"].number"))
        element_neutrons_ = int(charge) - element_protons_
        element_mass_ = eval("elements."+element+"["+str(charge)+"].mass")
        BE1 = ((element_protons_ * self.proton_weight +
               element_neutrons_ * self.neutron_weight) - element_mass_)
        BEF = (BE1)*(self.AMU*(self.speed_of_light))/self.speed_of_light
        BEN = BEF / charge
        return {'Value': BEN, 'Units': 'MeV/Nucleon'}

    # Radioactive Decay Rate \
    #   −𝑑𝑁𝑑𝑡=λ𝑁


    # Radioactive decay law
    #   𝑁=𝑁0𝑒−λ𝑡
QPHANDLER = QP()  # Object of main function

method_list = [method for method in dir(
    QP) if method.startswith('__') is False]  # Locates methods in QP (not to be mistaken for QPHANDLER)


def BUI():
    while(True):

        user_intention = input(
            f"Please choose a feature to use({method_list}) or exit/clear: ")

        if(user_intention in method_list):
            pass
        elif('exit' in user_intention):
            exit_Safe(1)
        elif('clear' in user_intention):
            print("Clearing...")
            clear()
            continue
        else:
            print(f"{user_intention} is not recognized.")
            continue

        # Input element handling
        user_input_element = ""
        try:
            user_input_element = input(
                f"({user_intention}) Element name(or back): ")
            if(user_input_element == "back"):
                print("Escaping...")
                continue
            if((user_input_element)):
                r = re.compile("([a-zA-Z]+)([0-9]+)")
                m = r.match(user_input_element)
                eval("elements."+m.group(1)+"["+m.group(2)+"].mass")
                Answer = eval(
                    f"QPHANDLER.{user_intention}(\"{m.group(1)}\", {m.group(2)})")
            else:
                Answer = eval(f"QPHANDLER.{user_intention}()")
        except AttributeError as e:

            if('PeriodicTable' in str(e)):
                error(user_input_element, "This is common. \n \
                    Please try Capitalizing your element.\n \
                    For example: Cu63, H1, Cu62")
            print(e)
            continue
        except KeyError as e:

            if('is not an isotope' in str(e)):
                error(user_input_element, "This is common. \n \
                    Please try making sure your isotope is in your element's range(s).\n \
                    For example: Cu63, H1, Cu62")
            continue

            # Simple equation handler
        print(Answer)


'''DEBUG ELEMENTS[ignore]'''
# print(elements.U[235].mass)
BUI()
