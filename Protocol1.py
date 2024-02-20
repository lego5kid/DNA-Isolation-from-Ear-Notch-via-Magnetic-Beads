# Pre-freeze steps
from opentrons import protocol_api

requirements = {"robotType": "OT-2", "apiLevel": "2.16"}

metadata = {
    'protocolName': 'DNA Extraction via Robot Part 1',
    'description': '''This protocol is for extraction of DNA from ear notches using magnets.''',
    'author': 'Nathaniel Hemmert'
    }

def run(protocol: protocol_api.ProtocolContext):
    protocol.set_rail_lights(True)
    
    #Loading Labware
    tips200 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 5)
    wellplate = protocol.load_labware('thermoscientific_96_wellplate_1200ul', 2)
    mix = protocol.load_labware('nest_12_reservoir_15ml', 3)

    #Defining Reagents
    reagentmix = protocol.define_liquid(
        name="Reagent Mix",
        description="30mL Laird's Buffer with 500uL Proteinase K, split between two reservoirs.",
        display_color="#0000ff"
    )

    #Loading Reagents
    mix["A11"].load_liquid(liquid=reagentmix, volume=15250)
    mix["A12"].load_liquid(liquid=reagentmix, volume=15250)

    #Loading Pipetter
    left_pipette = protocol.load_instrument('p300_multi_gen2', 'left', tip_racks=[tips200])

    #Step 2: Add 305 uL mix to all wells
    left_pipette.well_bottom_clearance.dispense = 10
    left_pipette.transfer(
        305,
        mix.wells(10, 11),
        wellplate.rows()[0],
        new_tip="once",
        blow_out=True,
        blowout_location="destination well"
    )

    #Complete, please freeze and incubate overnight
    protocol.comment('Protocol complete, please remove samples, and proceed to freezing and overnight incubation step.')
