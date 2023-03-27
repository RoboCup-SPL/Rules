#!/usr/bin/env python3

# Usage: ./generateField_simple.py field_2020.json

import json
import math
import cairo
import sys

# read the field dimensions from the rules from a JSON file

assert len(sys.argv) == 2

with open(sys.argv[1]) as f:
    o = json.load(f)

field_length = o['field']['length']
field_width = o['field']['width']
line_width = o['field']['lineWidth']
penalty_mark_size = o['field']['penaltyMarkSize']
goal_area_length = o['field']['goalAreaLength']
goal_area_width = o['field']['goalAreaWidth']
penalty_area_length = o['field']['penaltyAreaLength']
penalty_area_width = o['field']['penaltyAreaWidth']
penalty_mark_distance = o['field']['penaltyMarkDistance']
center_circle_diameter = o['field']['centerCircleDiameter']
border_strip_width = o['field']['borderStripWidth']
goal_post_diameter = o['goal']['postDiameter']
goal_height = o['goal']['height']
goal_inner_width = o['goal']['innerWidth']
goal_depth = o['goal']['depth']

# derive some often used constants from the field dimensions
x_border = field_length * 0.5 + border_strip_width
y_border = field_width * 0.5 + border_strip_width
x_goal_line = field_length * 0.5
y_touchline = field_width * 0.5
x_penalty_area = field_length * 0.5 - penalty_area_length
y_penalty_area = penalty_area_width * 0.5
x_penalty_mark = field_length * 0.5 - penalty_mark_distance
x_goal_area = field_length * 0.5 - goal_area_length
y_goal_area = goal_area_width * 0.5
line_width_2 = line_width * 0.5
penalty_mark_size_2 = penalty_mark_size * 0.5
center_circle_radius = center_circle_diameter * 0.5
pi_2 = math.pi * 0.5

# SVG generation parameters
svg_fieldline_width = 0.05
svg_dimensionline_width = 0.025
svg_symmetryline_width = 0.01
svg_font_size = 0.3
svg_addnotes = False

# outer lines
def draw_outer_lines(context):
    context.move_to(-(x_goal_line), -(y_touchline))
    context.line_to((x_goal_line), -(y_touchline))
    context.line_to((x_goal_line), (y_touchline))
    context.line_to(-(x_goal_line), (y_touchline))
    context.close_path()
    context.move_to(0, -(y_touchline))
    context.line_to(0, (y_touchline))

def draw_penalty_area(context, sign):
    context.move_to(sign * (x_goal_line), -(y_penalty_area))
    context.line_to(sign * (x_penalty_area), -(y_penalty_area))
    context.line_to(sign * (x_penalty_area), (y_penalty_area))
    context.line_to(sign * (x_goal_line), (y_penalty_area))

def draw_goal_area(context, sign):
    context.move_to(sign * (x_goal_line), -(y_goal_area))
    context.line_to(sign * (x_goal_area), -(y_goal_area))
    context.line_to(sign * (x_goal_area), (y_goal_area))
    context.line_to(sign * (x_goal_line), (y_goal_area))

def draw_center_circle(context):
    context.move_to(-center_circle_radius, 0)
    context.arc(0, 0, center_circle_radius, -math.pi, math.pi)
    context.move_to(-penalty_mark_size_2, 0)
    context.line_to(penalty_mark_size_2, 0)

# penalty mark
def draw_penalty_mark(context, sign):
    x_base = x_penalty_mark if sign else 0
    context.move_to(sign * (x_base - penalty_mark_size_2), 0)
    context.line_to(sign * (x_base + penalty_mark_size_2), 0)
    context.move_to(sign * (x_base), -penalty_mark_size_2)
    context.line_to(sign * (x_base), penalty_mark_size_2)

def draw_dimension_horizontal(context, x1, x2, y, height, bar=True, arrow=True, along_offset=-0.1, across_offset=-0.05, label=""):
    if bar:
        context.move_to(x1, y + height * 0.5)
        context.line_to(x1, y - height * 0.5)

        context.move_to(x2, y + height * 0.5)
        context.line_to(x2, y - height * 0.5)

    narrow = abs(x2 - x1) < 0.1
    if arrow:
        context.move_to(x1 + height * (-0.5 if narrow else 0.5), y + height * 0.5)
        context.line_to(x1, y)
        context.line_to(x1 + height * (-0.5 if narrow else 0.5), y - height * 0.5)

        context.move_to(x2 - height * (-0.5 if narrow else 0.5), y + height * 0.5)
        context.line_to(x2, y)
        context.line_to(x2 - height * (-0.5 if narrow else 0.5), y - height * 0.5)

    if not narrow:
        context.move_to(x1, y)
        context.line_to(x2, y)

    context.move_to((((x1 + x2) * 0.5) if not narrow else (x2 + height * 0.5)) + along_offset, y + across_offset)
    #context.show_text(label + str(round(abs(x2 - x1) * 1000)))
    context.show_text(label)

def draw_dimension_vertical(context, y1, y2, x, width, bar=True, arrow=True, along_offset=0.1, across_offset=-0.05, label=""):
    if bar:
        context.move_to(x + width * 0.5, y1)
        context.line_to(x - width * 0.5, y1)

        context.move_to(x + width * 0.5, y2)
        context.line_to(x - width * 0.5, y2)

    narrow = abs(y2 - y1) < 0.3
    if arrow:
        context.move_to(x + width * 0.5, y1 + width * (-0.5 if narrow else 0.5))
        context.line_to(x, y1)
        context.line_to(x - width * 0.5, y1 + width * (-0.5 if narrow else 0.5))

        context.move_to(x + width * 0.5, y2 - width * (-0.5 if narrow else 0.5))
        context.line_to(x, y2)
        context.line_to(x - width * 0.5, y2 - width * (-0.5 if narrow else 0.5))

    if not narrow:
        context.move_to(x, y1)
        context.line_to(x, y2)

    context.save()
    context.move_to(x + across_offset, (((y1 + y2) * 0.5) if not narrow else (y1 - width * 0.5)) + along_offset)
    context.rotate(-math.pi / 2)
    #context.show_text(label + str(round(abs(y2 - y1) * 1000)))
    context.show_text(label)
    context.restore()

###############################
## DRAW ENTIRE FIELD DRAWING ##
###############################

# additional padding to all four sides (in meters)
#padding = 0.5
padding = 0.0

width_in_m = field_length + 2 * border_strip_width + 2 * padding
height_in_m = field_width + 2 * border_strip_width + 2 * padding

width, height = 72 * 10 * (width_in_m / height_in_m), 72 * 10

surface = cairo.PDFSurface('field_simple.pdf', width, height)
context = cairo.Context(surface)

# fill the background with Green
context.set_source_rgb(0, 0.5, 0.125)
context.paint()

# set the origin to the center of the field and scale to meters
context.translate(width / 2, height / 2)
context.scale(width / width_in_m, height / height_in_m)
context.set_line_width(svg_fieldline_width)

# draw the contours of lines in White
context.set_source_rgb(1, 1, 1)
draw_outer_lines(context)
draw_center_circle(context)
draw_penalty_area(context, 1)
draw_penalty_area(context, -1)
draw_goal_area(context, 1)
draw_goal_area(context, -1)
draw_penalty_mark(context, 1)
draw_penalty_mark(context, -1)
context.stroke()

# add dimensions in black
context.set_source_rgb(0, 0, 0)
context.set_font_size(svg_font_size)
context.set_line_width(svg_dimensionline_width)

# dimensions for field boundary
#draw_dimension_horizontal(context, -x_border, x_border, -(y_border + 0.1), 0.2)
#draw_dimension_vertical(context, -y_border, y_border, -(x_border + 0.1), 0.2)
draw_dimension_horizontal(context, x_goal_line, x_border, (y_touchline - 0.3), 0.2, label="K")
draw_dimension_vertical(context, y_touchline, y_border, (x_goal_line - 0.3), 0.2, label="K")

# dimensions for outer field lines
#draw_dimension_horizontal(context, -(x_goal_line + line_width_2), (x_goal_line + line_width_2), -(y_touchline + line_width_2 + 0.1), 0.2)
#draw_dimension_vertical(context, -(y_touchline + line_width_2), (y_touchline + line_width_2), -(x_goal_line + line_width_2 + 0.1), 0.2)
draw_dimension_horizontal(context, -(x_goal_line), (x_goal_line), -(y_touchline + line_width_2 + 0.125), 0.2, label="A")
draw_dimension_vertical(context, -(y_touchline), (y_touchline), -(x_goal_line + line_width_2 + 0.125), 0.2, label="B")

# dimension for penalty area length / width
draw_dimension_horizontal(context, -(x_goal_line), -(x_penalty_area), -(y_penalty_area + 0.1), 0.2, label="G")
draw_dimension_vertical(context, -(y_penalty_area), (y_penalty_area), -(x_penalty_area - 0.1), 0.2, across_offset=0.3, label="H")
draw_dimension_horizontal(context, -(x_goal_line), -(x_goal_area), -(y_goal_area + 0.1), 0.2, label="E")
draw_dimension_vertical(context, -(y_goal_area), (y_goal_area), -(x_goal_area - 0.1), 0.2, across_offset=0.3, label="F")

# dimension penalty mark
draw_dimension_horizontal(context, (x_penalty_mark), x_goal_line, penalty_mark_size*2, 0.2, label="I")
draw_dimension_horizontal(context, (x_penalty_mark - penalty_mark_size_2), (x_penalty_mark + penalty_mark_size_2), 0, 0.2, along_offset=0, bar=True, label="D")

# center circle dimensions
draw_dimension_horizontal(context, -(center_circle_radius), (center_circle_radius), 0, 0.2, bar=True, label="J", along_offset=0.2)
#draw_dimension_horizontal(context, -(center_circle_radius - line_width_2), (center_circle_radius - line_width_2), -0.05, 0.1, along_offset=0.2)
#draw_dimension_vertical(context, -(center_circle_radius + line_width_2), (center_circle_radius + line_width_2), -0.05, 0.1, along_offset=-0.2)
#draw_dimension_vertical(context, -(center_circle_radius - line_width_2), (center_circle_radius - line_width_2), 0.125, 0.1, along_offset=-0.2)

# line width
draw_dimension_horizontal(context, -svg_fieldline_width/2, svg_fieldline_width/2, -(y_touchline - 1), 0.2, along_offset=0, bar=False, label="C")

if svg_addnotes:
    context.move_to(0, y_border + 0.2)
    context.show_text("Dimensions are in millimeters. The field is symmetric about both axes (shown in blue).")
    context.move_to(0, y_border + 0.3)
    context.show_text("The penalty marks MUST be crosses and the center mark a rectangular line segment and NOT a circle.")

context.stroke()
