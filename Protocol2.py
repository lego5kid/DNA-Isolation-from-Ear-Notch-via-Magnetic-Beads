#Rest of Protocol
from opentrons import protocol_api

requirements = {"robotType": "OT-2", "apiLevel": "2.15"}

metadata = {
    'protocolName': 'DNA Extraction via Robot Part 2',
    'description': '''This protocol is for extraction of DNA from ear notches using magnets.''',
    'author': 'Nathaniel Hemmert'
    }

def run(protocol: protocol_api.ProtocolContext):
    protocol.set_rail_lights(True)

    #Loading Labware
    tips1 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 4)
    tips2 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 5)
    tips3 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 6)
    tips4 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 7)
    tips5 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 8)
    tips6 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 9)
    tips7 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 10)
    tips8 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 11)
    tips9 = protocol.load_labware('opentrons_96_filtertiprack_200ul', protocol_api.OFF_DECK)
    tips10 = protocol.load_labware('opentrons_96_filtertiprack_200ul', protocol_api.OFF_DECK)           ##  MAKE SURE TO UNCOMMENT THIS FOR TESTING ON MACHINE, IT'S ONLY COMMENTED FOR SIMULATION ##
    tips11 = protocol.load_labware('opentrons_96_filtertiprack_200ul', protocol_api.OFF_DECK)
    tips12 = protocol.load_labware('opentrons_96_filtertiprack_200ul', protocol_api.OFF_DECK)
    tips13 = protocol.load_labware('opentrons_96_filtertiprack_200ul', protocol_api.OFF_DECK)
    tips14 = protocol.load_labware('opentrons_96_filtertiprack_200ul', protocol_api.OFF_DECK)
    mag_mod = protocol.load_module('magnetic module gen2', 1)
    plate1 = mag_mod.load_labware('thermoscientific_96_wellplate_1200ul', 1)
    notch= protocol.load_labware('thermoscientific_96_wellplate_1200ul', 2)
    plate2= protocol.load_labware('thermoscientific_96_wellplate_1200ul', protocol_api.OFF_DECK)
    plate3= protocol.load_labware('nest_96_wellplate_100ul_pcr_full_skirt', protocol_api.OFF_DECK)
    source = protocol.load_labware('nest_12_reservoir_15ml', 3)

    #Defining Reagents
    guanidinehcl = protocol.define_liquid(
        name="Guanidine HCl",
        description="Guanidine HCl",
        display_color="#cc00ff"
    )
    magbeads = protocol.define_liquid(
        name="Magnetic Beads",
        description="Magentic Beads",
        display_color="#cc0000"
    )
    ethanol = protocol.define_liquid(
        name="70% Ethanol",
        description="70% Ethanol",
        display_color="#ff6600"
    )
    tebuffer = protocol.define_liquid(
        name="TE Buffer",
        description="TE Buffer",
        display_color="#ffff00"
    )

    #Loading Reagents
    source["A1"].load_liquid(liquid=guanidinehcl, volume=8500)
    source["A2"].load_liquid(liquid=tebuffer, volume=8500)
    source["A3"].load_liquid(liquid=ethanol, volume=15000)
    source["A4"].load_liquid(liquid=ethanol, volume=15000)
    source["A5"].load_liquid(liquid=ethanol, volume=15000)
    source["A6"].load_liquid(liquid=ethanol, volume=15000)
    source["A7"].load_liquid(liquid=magbeads, volume=11500)
    source["A8"].load_liquid(liquid=magbeads, volume=11500)
    source["A9"].load_liquid(liquid=magbeads, volume=11500)
    source["A10"].load_liquid(liquid=magbeads, volume=11500)

    #Loading Pipetter
    left_pipette = protocol.load_instrument('p300_multi_gen2', 'left', tip_racks=[tips1, tips2, tips3, tips4, tips5, tips6, tips7, tips8, tips9, tips10, tips11, tips12, tips13, tips14])

    #Step 4.1 - Add 40ul lysate to all wells
    left_pipette.well_bottom_clearance.aspirate = 4
    left_pipette.transfer(
        40,
        notch.rows()[0],
        plate1.rows()[0],
        new_tip="always",
        blow_out=True,
        blowout_location="destination well"
    )

    #Step 4.2 - Add 40ul Guanidine HCl to all wells
    left_pipette.well_bottom_clearance.aspirate = 1
    left_pipette.transfer(
        40,
        source.well('A1'),
        plate1.rows()[0],
        new_tip="always",
        mix_after=(3,80),
        blow_out=True,
        blowout_location="destination well"
    )

    #Step 5 - Incubate 10 minutes
    protocol.comment('Incubating for 10 minutes.')
    protocol.delay(minutes=10)

    #Step 6 - Add 218ul magbeads to all wells
    #Had to use building block commands to handle the viscosity
    left_pipette.flow_rate.aspirate = 74
    left_pipette.flow_rate.dispense = 74
    left_pipette.flow_rate.blow_out = 4

    for p in range(6):
        wells = plate1.columns()[p]
        left_pipette.pick_up_tip()
        left_pipette.move_to(source['A7'].top())
        left_pipette.move_to(source['A7'].bottom(), speed=10)
        left_pipette.mix(
            10,
            150
        )
        left_pipette.aspirate(
            109
        )
        protocol.delay(seconds=6)
        left_pipette.move_to(source['A7'].top(), speed=1)
        left_pipette.move_to(wells[0].top())
        left_pipette.move_to(wells[0].bottom(z=10), speed=10)
        left_pipette.dispense(
            109
        )
        protocol.delay(seconds=6)
        left_pipette.blow_out()
        left_pipette.move_to(source['A7'].top())
        left_pipette.move_to(source['A7'].bottom(), speed=10)
        left_pipette.aspirate(
            109
        )
        protocol.delay(seconds=6)
        left_pipette.move_to(source['A7'].top(), speed=1)
        left_pipette.move_to(wells[0].top())
        left_pipette.move_to(wells[0].bottom(), speed=10)
        left_pipette.dispense(
            109
        )
        protocol.delay(seconds=6)
        left_pipette.mix(
            10,
            150
        )
        protocol.delay(seconds=6)
        left_pipette.move_to(wells[0].top(), speed=1)
        left_pipette.blow_out()
        left_pipette.drop_tip()

    for o in range(6,12):
        wells = plate1.columns()[o]
        left_pipette.pick_up_tip()
        left_pipette.move_to(source['A8'].top())
        left_pipette.move_to(source['A8'].bottom(), speed=10)
        left_pipette.mix(
            10,
            150
        )
        left_pipette.aspirate(
            109
        )
        protocol.delay(seconds=6)
        left_pipette.move_to(source['A8'].top(), speed=1)
        left_pipette.move_to(wells[0].top())
        left_pipette.move_to(wells[0].bottom(z=10), speed=10)
        left_pipette.dispense(
            109
        )
        protocol.delay(seconds=6)
        left_pipette.blow_out()
        left_pipette.move_to(source['A8'].top())
        left_pipette.move_to(source['A8'].bottom(), speed=10)
        left_pipette.aspirate(
            109
        )
        protocol.delay(seconds=6)
        left_pipette.move_to(source['A8'].top(), speed=1)
        left_pipette.move_to(wells[0].top())
        left_pipette.move_to(wells[0].bottom(), speed=10)
        left_pipette.dispense(
            109
        )
        protocol.delay(seconds=6)
        left_pipette.mix(
            10,
            150
        )
        protocol.delay(seconds=6)
        left_pipette.move_to(wells[0].top(), speed=1)
        left_pipette.blow_out()
        left_pipette.drop_tip()
    
    left_pipette.flow_rate.aspirate = 92.86
    left_pipette.flow_rate.dispense = 92.86
    left_pipette.flow_rate.blow_out = 92.86

    #Step 7- Incubate 5 minutes
    protocol.comment('Incubating for 5 minutes.')
    protocol.delay(minutes=5)

    #Step 8- Engage magnet, wait for 10 minutes
    protocol.comment('Engaging magnet, running for 10 minutes.')
    mag_mod.engage(height_from_base=3)
    protocol.delay(minutes=10)

    #Step 9/10/11.1
    for i in range(12):
        column = plate1.columns()[i]
        #Step 9- Remove supernatant
        left_pipette.well_bottom_clearance.aspirate = 0
        left_pipette.transfer(
            300,
            column[0],
            protocol.fixed_trash['A1'],
            new_tip="once"
        )

        #Step 10.1- Wash once
            #Had to use building block commands to minimize tip usage
        left_pipette.well_bottom_clearance.aspirate = 1
        left_pipette.pick_up_tip()
        left_pipette.aspirate(
            150,
            source['A3']
            )
        left_pipette.air_gap(30)
        left_pipette.dispense(
            180,
            column[0]
        )
        # left_pipette.mix(         ##Might include, depends on if we want to test for improved washing
        #     5, 150,
        #     column[0]
        # )
            #Back to normal
        left_pipette.well_bottom_clearance.aspirate = 0
        left_pipette.transfer(
            150,
            column[0],
            protocol.fixed_trash['A1'],
            air_gap=(30),
            new_tip="never"
        )
        left_pipette.drop_tip()

        #Step 10.2- Wash again
            #Had to use building block commands to minimize tip usage
        left_pipette.well_bottom_clearance.aspirate = 1
        left_pipette.pick_up_tip()
        left_pipette.aspirate(
            150,
            source['A4']
            )
        left_pipette.air_gap(30)
        left_pipette.dispense(
            180,
            column[0]
        )
        # left_pipette.mix(
        #     5, 150,
        #     column[0]
        # )
            #Back to normal
        left_pipette.well_bottom_clearance.aspirate = 0
        left_pipette.transfer(
            150,
            column[0],
            protocol.fixed_trash['A1'],
            air_gap=(30),
            new_tip="never"
        )
        left_pipette.drop_tip()

        #Step 11.1- Resuspend in TE buffer
        left_pipette.well_bottom_clearance.aspirate = 1
        mag_mod.disengage()
        left_pipette.transfer(
            40,
            source['A2'],
            column[0],
            new_tip="once",
            mix_after=(3,40),
            blow_out=True,
            blowout_location="destination well"
        )
        mag_mod.engage(height_from_base=3)

    #Step 11.2- Disengage magnet
    protocol.comment('Disengaging magnet.')
    mag_mod.disengage()

    #Step 11.3- Replace tips, remove old samples, place new wellplate, and incubate 5 minutes
    protocol.comment('Remove empty tipracks, place new ones in 5, 6, 7, 8, 9, 10. Remove old sample wellplate, replace with clean one.')
    protocol.move_labware(labware=tips1, new_location=protocol_api.OFF_DECK)
    protocol.move_labware(labware=tips2, new_location=protocol_api.OFF_DECK)
    protocol.move_labware(labware=tips3, new_location=protocol_api.OFF_DECK)
    protocol.move_labware(labware=tips4, new_location=protocol_api.OFF_DECK)
    protocol.move_labware(labware=tips5, new_location=protocol_api.OFF_DECK)
    protocol.move_labware(labware=tips6, new_location=protocol_api.OFF_DECK)
    protocol.move_labware(labware=tips7, new_location=protocol_api.OFF_DECK)
    protocol.move_labware(labware=tips9, new_location=5)
    protocol.move_labware(labware=tips10, new_location=6)
    protocol.move_labware(labware=tips11, new_location=7)
    protocol.move_labware(labware=tips12, new_location=8)
    protocol.move_labware(labware=tips13, new_location=9)
    protocol.move_labware(labware=tips14, new_location=10)
    protocol.move_labware(labware=notch, new_location=protocol_api.OFF_DECK)
    protocol.move_labware(labware=plate2, new_location=2)
    protocol.comment('Incubating for 5 minutes.')
    protocol.delay(minutes=5)

    #Step 12- Engage magnet, wait for 3 minutes
    protocol.comment('Engaging magnet, running for 3 minutes, then disengaging')
    mag_mod.engage(height_from_base=3)
    protocol.delay(minutes=3)
    mag_mod.disengage()

    #Step 13- Add guanadine hCl to clean tray
    left_pipette.distribute(
        40,
        source.well('A1'),
        plate2.rows()[0],
        new_tip="once",
        disposal_volume=20,
        touch_tip=True
    )

    #Step 14- Move DNA from old wells to new tray
    left_pipette.transfer(
        45,
        plate1.rows()[0],
        plate2.rows()[0],
        new_tip="always",
        mix_after=(3, 45),
        blow_out=True,
        blowout_location="destination well"
    )

    #Step 15- Add magbeads to all clean wells
    #Had to use building block commands to handle the viscosity
    left_pipette.flow_rate.aspirate = 74
    left_pipette.flow_rate.dispense = 74
    left_pipette.flow_rate.blow_out = 4

    left_pipette.pick_up_tip()          #No pipette mixing here, so one tip at beginning, drop at end. Some changes made to protocol to minimize touching and mixing.
    
    for p in range(6):
        wells = plate2.columns()[p]
        left_pipette.move_to(source['A9'].top())
        left_pipette.move_to(source['A9'].bottom(), speed=10)
        left_pipette.mix(
            10,
            150
        )
        left_pipette.aspirate(
            109
        )
        protocol.delay(seconds=6)
        left_pipette.move_to(source['A9'].top(), speed=1)
        left_pipette.move_to(wells[0].top())
        left_pipette.move_to(wells[0].bottom(z=10), speed=10)
        left_pipette.dispense(
            109
        )
        protocol.delay(seconds=6)
        left_pipette.blow_out()
        left_pipette.move_to(source['A9'].top())
        left_pipette.move_to(source['A9'].bottom(), speed=10)
        left_pipette.aspirate(
            109
        )
        protocol.delay(seconds=6)
        left_pipette.move_to(source['A9'].top(), speed=1)
        left_pipette.move_to(wells[0].top())
        left_pipette.move_to(wells[0].bottom(z=10), speed=10)
        left_pipette.dispense(
            109
        )
        protocol.delay(seconds=6)
        left_pipette.blow_out()

    for o in range(6,12):
        wells = plate1.columns()[o]
        left_pipette.move_to(source['A10'].top())
        left_pipette.move_to(source['A10'].bottom(), speed=10)
        left_pipette.mix(
            10,
            150
        )
        left_pipette.aspirate(
            109
        )
        protocol.delay(seconds=6)
        left_pipette.move_to(source['A10'].top(), speed=1)
        left_pipette.move_to(wells[0].top())
        left_pipette.move_to(wells[0].bottom(z=10), speed=10)
        left_pipette.dispense(
            109
        )
        protocol.delay(seconds=6)
        left_pipette.blow_out()
        left_pipette.move_to(source['A10'].top())
        left_pipette.move_to(source['A10'].bottom(), speed=10)
        left_pipette.aspirate(
            109
        )
        protocol.delay(seconds=6)
        left_pipette.move_to(source['A10'].top(), speed=1)
        left_pipette.move_to(wells[0].top())
        left_pipette.move_to(wells[0].bottom(z=10), speed=10)
        left_pipette.dispense(
            109
        )
        protocol.delay(seconds=6)
        left_pipette.move_to(wells[0].top(), speed=1)
        left_pipette.blow_out()
    
    left_pipette.drop_tip()

    left_pipette.flow_rate.aspirate = 92.86
    left_pipette.flow_rate.dispense = 92.86
    left_pipette.flow_rate.blow_out = 92.86

    #Step 16.1- Move clean tray onto magmod, dispose of old tray
    protocol.comment('Remove old tray from magnetic module and dispose, then move the plate from 2 onto the magnetic module. Place final collection tray in 2.')
    protocol.move_labware(labware=plate1, new_location=protocol_api.OFF_DECK)
    protocol.move_labware(labware=plate2, new_location=mag_mod)
    protocol.move_labware(labware=plate3, new_location=2)

    #Step 16.2- Incubate 5 minutes
    protocol.comment('Incubating for 5 minutes.')
    protocol.delay(minutes=5)

    #Step 17- Engage magnet, wait for 10 minutes
    protocol.comment('Engaging magnet, running for 10 minutes.')
    mag_mod.engage(height_from_base=3)
    protocol.delay(minutes=10)

    #Step 18/19/20.1
    for i in range(12):
        column = plate2.columns()[i]
        #Step 18- Remove supernatant
        left_pipette.well_bottom_clearance.aspirate = 0
        left_pipette.transfer(
            95,        #Might be 303 if magnets are part of supernatant
            column[0],
            protocol.fixed_trash['A1'],
            new_tip="once"
        )

        #Step 19.1- Wash once
            #Had to use building block commands to minimize tip usage
        left_pipette.well_bottom_clearance.aspirate = 1
        left_pipette.pick_up_tip()
        left_pipette.aspirate(
            150,
            source['A5']
            )
        left_pipette.air_gap(30)
        left_pipette.dispense(
            180,
            column[0]
        )
        # left_pipette.mix(         ##Might include, depends on if we want to test for improved washing
        #     5, 150,
        #     column[0]
        # )
            #Back to normal
        left_pipette.well_bottom_clearance.aspirate = 0
        left_pipette.transfer(
            150,
            column[0],
            protocol.fixed_trash['A1'],
            air_gap=(30),
            new_tip="never"
        )
        left_pipette.drop_tip()

        #Step 19.2- Wash again
            #Had to use building block commands to minimize tip usage
        left_pipette.well_bottom_clearance.aspirate = 1
        left_pipette.pick_up_tip()
        left_pipette.aspirate(
            150,
            source['A6']
            )
        left_pipette.air_gap(30)
        left_pipette.dispense(
            180,
            column[0]
        )
        # left_pipette.mix(
        #     5, 150,
        #     column[0]
        # )
            #Back to normal
        left_pipette.well_bottom_clearance.aspirate = 0
        left_pipette.transfer(
            150,
            column[0],
            protocol.fixed_trash['A1'],
            air_gap=(30),
            new_tip="never"
        )
        left_pipette.drop_tip()

        #Step 20.1- Resuspend in TE buffer
        left_pipette.well_bottom_clearance.aspirate = 1
        mag_mod.disengage()
        left_pipette.transfer(
            40,
            source['A2'],
            column[0],
            new_tip="once",
            mix_after=(3,40),
            blow_out=True,
            blowout_location="destination well"
        )
        mag_mod.engage(height_from_base=3)

    #Step 20.2- Disengage magnet
    protocol.comment('Disengaging magnet.')
    mag_mod.disengage()

    #Step 20.3- Incubate for 15 minutes
    protocol.comment('Incubating for 15 minutes.')
    protocol.delay(minutes=15)

    #Step 21- Engage magnet for 3 minutes
    protocol.comment('Engaging magnet, waiting 3 minutes.')
    mag_mod.engage(height_from_base=3)
    protocol.delay(minutes=3)

    #Step 22- Put DNA in final tray
    left_pipette.transfer(
        40,
        plate2.rows()[0],
        plate3.rows()[0],
        new_tip="always",
        blow_out=True,
        blowout_location="destination well"
    )
    mag_mod.disengage()

    #WE DONE BABY
    protocol.set_rail_lights(False)
    protocol.delay(seconds=1)
    protocol.set_rail_lights(True)
    protocol.delay(seconds=1)
    protocol.set_rail_lights(False)
    protocol.delay(seconds=1)
    protocol.set_rail_lights(True)
    protocol.delay(seconds=1)
    protocol.set_rail_lights(False)
    protocol.comment('Protocol complete, dispose of empty tipracks and the plate on the mag mod, seal product tray and store samples appropriately.')