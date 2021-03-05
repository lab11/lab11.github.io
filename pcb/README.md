Website PCBs
============

In order to add a PCB to the website you need to add a `.zip` file to the
pcb folder. The `.zip` should include all of the files relevant to that
PCB, including but not limited to gerbers, board files, images, and a bom.

To be compatible with the pcb.html creation script there are few naming
constraints you need to follow.


Directions
----------

1. **Zip Name**: `<pcb name>_<revision>_<year>-<month>-<day>.zip`. Example:
`impulse_c_2013-11-19.zip`.

2. **PDF Name**: There must be a .pdf file in the root of the zip file. This
should document the board and include the schematic, various copper layers
and silkscreen, and the BOM. The name should be `<pcb name>.pdf`. Example:
`impulse.pdf`.

3. **Info File**: Meta data that is not contained in the zip filename should
be in a `.info` file. The filename should be `<pcb name>.info`. Example:
`impulse.info`. The contents are key value pairs in the form `key: value`.
The keys `author` and `description` must be present. Example:

    author: Brad Campbell
	description: Wrote this readme.

Other keys that are supported:

    notes: Add a note to this pcb like: Issue with Pin 10.

The description field can use Markdown if you want to use links or bold or
whatnot.

Do not include newlines. If you do the paper will not build. 

4. **Image**: Each PCB should have at least two pictures and all pictures should
be in the `/images` folder. There should be a shot of it in real life
(after it has been made and assembled) and named `images/<pcb name>.jpg`.
There should also be a shot of the PCB from the board file named
`images/<pcb name>_pcb.jpg`. All images can also be pngs.


Adding to Website
-----------------

To add the PCB to the website add the `.zip` to the `website/pcb` folder in
shed.

