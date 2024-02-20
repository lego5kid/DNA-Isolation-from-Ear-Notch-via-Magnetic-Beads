# DNA Isolation from Ear Notch via Magnetic Beads

### This is a protocol series--built on the opentrons api--that automates the isolation of DNA from ear notches when using the Opentrons OT-2 pipetting robot. This documentation will help you understand how to use this protocol, and how I built this protocol.

### All sections will have links to their respective pages on the Opentrons API documentation for further depth. A link to the full API documentation can be found [here](https://docs.opentrons.com/v2/index.html).

## I. Installation

1. If this is for use on a brand new OT-2, make sure you've downloaded the opentrons software and connected and calibrated your robot, instructions on how to do so can be found on [opentrons' website](https://support.opentrons.com/s/ot-2/get-started-guide).
    - This guide also shows how to add the protocol(s) to the opentrons app, just make sure it's the version you want!
2. From the labware menu, click import, and select the *thermoscientific_96_wellplate_1200ul.json* file.
    - The opentrons software doesn't have the specs for this labware baked in, so I had to custom-make it for use in this protocol.
3. That's it! You should be able to select the protocol, and it will give you a preview of all the reagents and labware needed to run.

## II. Likely Changes

In the case of changed labware, volumes, etc., I've put together a list of simple command breakdowns to allow for easy augmentation.

**I highly recommend using either ctrl-F find and replace or ctrl-shift-L multi-cursor within VS Code to make changes across the protocol. A breakdown of these functions can be found [here](https://code.visualstudio.com/docs/editor/codebasics).**

### 1. [Labware](https://docs.opentrons.com/v2/new_labware.html)

```python
Custom_Name = protocol.load_labware('labwareid', deck_position)
```

- The custom name is how the item will be called in later comands.
- The labware id is obtained from [opentrons' labware library.](https://labware.opentrons.com/)
- The deck position is numbered on the robot.

#### 1a. Tips

- If you update the tips custom name, make sure you update the available tip racks in the loaded pipetter

```python
Custom_Name = protocol.load_instrument('pippetteid', 'left or right', tip_racks=[tips1, tips2, etc.])
```

### 2. [Reagents](https://docs.opentrons.com/v2/new_labware.html#labeling-liquids-in-wells)

The defined reagents are only for the convenience of showing needed reagents in the opentrons software. The protocol runs perfectly fine without them.

However, if you wish to change/update the reagents, heres a breakdown of the commands

```python
#Defining Reagents
Custom_Name = protocol.define_liquid(
    name="display name",
    description="Short description to show in the software",
    *display_color="color hexcode"
)
```

Loading reagents just shows the defined reagens in the UI of the opentrons app, as well as the volume needed in each well. Again, these aren't mandatory, just a nice addition.

```python
#Loading Reagents
labwarename["Well"].load_liquid(liquid=Custom_Name, volume=999)     # Volume is in uL
```

All total volumes are relatively arbitrary, with most being the volume needed for 96 wells with 10% excess, but some are less. We just wanted to ensure there was some excess reagents in case the pipette couldn't aspirate everything in the reservoirs. 

### 3. [Transfer Commands](https://docs.opentrons.com/v2/new_complex_commands.html)

For the sake of brevity and understanding, having the wells in the `()` allows you to select or list specific wells/columns/rows. When using `[]`, the value entered returns a list of all wells within the selected column/row. 
- For example, `plate1.rows()[0]` will return all wells within row 1(A1, A2, ...), since python starts counting at 0.

For more depth on the options for the source and destination wells, see [here](https://docs.opentrons.com/v2/complex_commands/sources_destinations.html) in the docs.

A more in-depth breakdown of the optional arguments can be found in [this section](https://docs.opentrons.com/v2/complex_commands/parameters.html) of the opentrons' API documentation.

```python
All parts with * before them are optional for the command. 

pipette.transfer(
    volume,
    source.wells(),
    destination.wells(),
    *new_tip="never, once, or always",                          # default is once
    *mix_before=(repititions, volume),                          # default has no mixing
    *touch_tip=True/False,                                      # default is false
    *air_gap=volume,                                            # default has no air gap
    *mix_after=(repititions, volume),
    *blow_out=True/False,                                       # default is false
    *blowout_location="destination well, source well, trash",   # default is trash
    *trash=True/false                                           # default is true
)
```

### 4. [Viscous Reagents](https://support.opentrons.com/s/article/How-to-handle-viscous-liquids-in-the-Python-API)

[Here](https://support.opentrons.com/s/article/How-to-handle-viscous-liquids-in-the-Python-API)'s opentrons' documentation of aspriation/blowout speeds, as well as recommended delays. Just follow the rates and delays for the liquid most closely resembling what you use.

The flow rates are defined at the beginnning of the step, in uL/s, so change those as necessary:

```python
left_pipette.flow_rate.aspirate = 74
left_pipette.flow_rate.dispense = 74
left_pipette.flow_rate.blow_out = 4
```

The delays are scattered within, in the format of:

```python
protocol.delay(seconds=6)   # The time unit can be changes to minutes and hours, if necessary
```
So change the time or remove the delay entirely if desired.

A pdf doc I found from opentrons says to move the tip into any fluid at 10mm/s, so you'l see that used throughout, however the withdrawal speed is currently set to 1mm/s, and to change, edit the following commands:

```python
left_pipette.move_to(source['A7'].top(), speed=1)   # Speed is in mm/s
```

And I reset the flow rates to the default of 92.96 at the and of the step.

## III. Weird things of note.

There were a number of things that are wierd with the API, and with working on the robot in general, so I wanted to document them here so you understand the thinking.

#### 1. API versioning and the trash bin

With the protocol, I have the robot disposing of the supernatant into the trash bin during the washing steps, and in API version 2.15 and earlier, it works great. The trashbin has a well that can be called with the `protocol.fixed_trash['A1']` command.

However, with API v2.16 and later, they changed the trash into a Trashbin object, which also removed its wells. This meant that I couldn't dispense supernatant or waste fluids into the trash, or at least I couldn't get it to work. 

As such, I recommend keeping protocol 2 on API version 2.15, unless you have a way of making it work.

#### 2. Multiple reagent wells and for loops

You probably noticed I have the magbead steps split into two for loops, and in the washing for loops, I have muliple source wells. This is due to the large volume of reagents, and needing to pull from multiple wells to keep the robot from just transferring air. 

There's probably a better way to code this, so if you're up to it, feel free to optimize it.

#### 3. Custom labware and magnet engage height

At time of writing, the 1200uL, 96-wellplate we use is not in the official opentrons labware library, so I had to make the labware manually using opentrons' [Custom Labware Creator](https://labware.opentrons.com/create).

The only limiatation with this, is that all the official labware, they came with a default engage height for the magnetic module, and the custom labware doesn't. To get around this, the engage height is set manually within the protocol, with the following command:

```python
mag_mod.engage(height_from_base=3)  # If using labware from the official library, the height_from_base argument can be removed.
```
