import nuke
import re

def build_light_setup(light, basex, basey, prev_dot=None, const=None):

    read = nuke.selectedNodes()[0]

    dot0 = nuke.nodes.Dot()
    if prev_dot is None:
        dot0.setInput(0, read)
    else:
        dot0.setInput(0, prev_dot)

    albedo = nuke.nodes.Shuffle2()
    albedo.setInput(0, dot0)
    albedo["in1"].setValue(f"albedo")
    albedo["in2"].setValue("rgba")
    albedo["label"].setValue(f"[value in1]")

    dot1 = nuke.nodes.Dot()
    dot1.setInput(0, albedo)

    dot2 = nuke.nodes.Dot()
    dot2.setInput(0, dot1)

    beauty = nuke.nodes.Shuffle2()
    beauty.setInput(0, dot2)
    beauty["in1"].setValue(f"C_{light}")
    beauty["in2"].setValue("rgba")
    beauty["label"].setValue(f"[value in1]")

    diff = nuke.nodes.Shuffle2()
    diff.setInput(0, albedo)
    diff["in1"].setValue(f"combineddiffuse_{light}")
    diff["in2"].setValue("rgba")
    diff["label"].setValue(f"[value in1]")

    dot3 = nuke.nodes.Dot()
    dot3.setInput(0, diff)

    gloss = nuke.nodes.Shuffle2()
    gloss.setInput(0, dot3)
    gloss["in1"].setValue(f"combinedglossyreflection_{light}")
    gloss["in2"].setValue("rgba")
    gloss["label"].setValue(f"[value in1]")

    div = nuke.nodes.Merge2(operation="divide")
    div.setInput(0, dot1)
    div.setInput(1, diff)

    mult = nuke.nodes.Merge2(operation="multiply")
    mult.setInput(0, div)
    mult.setInput(1, dot2)

    plus = nuke.nodes.Merge2(operation="plus")
    plus.setInput(0, mult)
    plus.setInput(1, gloss)

    trans = nuke.nodes.Shuffle2()
    trans.setInput(0, dot3)
    trans["in1"].setValue(f"glossytransmission_{light}")
    trans["in2"].setValue("rgba")
    trans["label"].setValue(f"[value in1]")

    plus2 = nuke.nodes.Merge2(operation="plus")
    plus2.setInput(0, plus)
    plus2.setInput(1, trans)

    sw = nuke.nodes.Switch()
    sw.setInput(0, beauty)
    sw.setInput(1, plus2)
    sw["label"].setValue(f"[value which]")

    grade = nuke.nodes.Grade()
    grade.setInput(0, sw)
    grade["label"].setValue(f"[value multiply]")

    plus3 = nuke.nodes.Merge2(operation="plus")
    plus3.setInput(0, const)
    plus3.setInput(1, grade)

    note = nuke.nodes.StickyNote()
    clean_light = light.replace("_", " ").title()
    note["label"].setValue(clean_light)
    note["note_font_size"].setValue(40)

    base_x = basex
    base_y = basey

    x_col_inc = 100
    x_col1 = base_x + 50
    x_col2 = x_col1 + x_col_inc
    x_col3 = x_col2 + x_col_inc
    x_col4 = x_col3 + x_col_inc
    x_col5 = basex + 600
    y_row_inc = 50
    y_row1 = base_y + 0
    y_row2 = y_row1 + y_row_inc
    y_row3 = y_row2 + y_row_inc
    y_row4 = y_row3 + y_row_inc
    y_row5 = y_row4 + y_row_inc + 30

    dot0.setXpos(base_x)
    dot0.setYpos(base_y + 10)

    dot1.setXpos(x_col1 + 34)
    dot1.setYpos(y_row2 + 4)  

    dot2.setXpos(x_col1 + 34)
    dot2.setYpos(y_row3 + 4)

    dot3.setXpos(x_col3 + 35)
    dot3.setYpos(y_row1 + 10)

    albedo.setXpos(x_col1)
    albedo.setYpos(y_row1)

    beauty.setXpos(x_col1)
    beauty.setYpos(y_row4)

    diff.setXpos(x_col2)
    diff.setYpos(y_row1)

    gloss.setXpos(x_col3)
    gloss.setYpos(y_row2)

    div.setXpos(x_col2)
    div.setYpos(y_row2)

    mult.setXpos(x_col2)
    mult.setYpos(y_row3)

    plus.setXpos(x_col3)
    plus.setYpos(y_row3)

    trans.setXpos(x_col4)
    trans.setYpos(y_row1)

    plus2.setXpos(x_col4)
    plus2.setYpos(y_row3)

    sw.setXpos(x_col4)
    sw.setYpos(y_row4)

    grade.setXpos(x_col4)
    grade.setYpos(y_row5)

    plus3.setXpos(x_col5)
    plus3.setYpos(y_row5 + 6)

    note.setXpos(basex - 250)
    note.setYpos(basey + 50)

    const = plus3

    return (dot0, const)


PATTERN = re.compile(r"^(C|combineddiffuse|combinedglossyreflection)_(.+)\.(red|green|blue|alpha)$")

def get_light_names(read):

    lights = set()

    for c in read.channels():
        m = PATTERN.match(c)
        if not m:
            continue

        _, light, _ = m.groups()
        lights.add(light)

    return sorted(lights)


def main():

    sel = nuke.selectedNodes()

    if len(sel) != 1 or sel[0].Class() != "Read":
        nuke.message("Select exactly ONE Read node.")
        return

    read = sel[0]

    lights = get_light_names(read)

    if not lights:
        nuke.message("No lights found.")
        return

    basex = read.xpos() + 35
    basey = read.ypos() + 250

    const = nuke.nodes.Constant()
    const.setXpos(basex + 600)
    const.setYpos(basey - 60)

    prev_dot = None
    for light in lights:
        (prev_dot, const) = build_light_setup(light, basex, basey, prev_dot, const)
        basey += 350