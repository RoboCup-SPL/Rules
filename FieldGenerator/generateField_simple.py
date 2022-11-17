#!/usr/bin/env python3

# Usage: ./generateField.py standard_field.json

import json
import math
import cairo
import sys

# read the field dimensions from the rules from a JSON file

assert len(sys.argv) == 2

with open(sys.argv[1]) as f:
    o = json.load(f)

field_length = o['field_length']
field_width = o['field_width']
line_width = o['line_width']
penalty_cross_size = o['penalty_cross_size']
penalty_area_length = o['penalty_area_length']
penalty_area_width = o['penalty_area_width']
penalty_cross_distance = o['penalty_cross_distance']
goal_area_length = o['goal_area_length']
goal_area_width = o['goal_area_width']
center_circle_diameter = o['center_circle_diameter']
border_strip_width = o['border_strip_width']
goal_depth = o['goal_depth']
goal_inner_width = o['goal_inner_width']
goal_post_diameter = o['goal_post_diameter']
goal_height = o['goal_height']

# derive some often used constants from the field dimensions
x_border = field_length * 0.5 + border_strip_width
y_border = field_width * 0.5 + border_strip_width
x_groundline = field_length * 0.5
y_sideline = field_width * 0.5
x_penalty_area = field_length * 0.5 - penalty_area_length
y_penalty_area = penalty_area_width * 0.5
x_penalty_cross = field_length * 0.5 - penalty_cross_distance
x_goal_area = field_length * 0.5 - goal_area_length
y_goal_area = goal_area_width * 0.5
line_width_2 = line_width * 0.5
penalty_cross_size_2 = penalty_cross_size * 0.5
center_circle_radius = center_circle_diameter * 0.5
pi_2 = math.pi * 0.5

# SVG generation parameters
svg_fieldline_width = 0.05
svg_dimensionline_width = 0.025
svg_symmetryline_width = 0.01
svg_font_size = 0.3
svg_addnotes = False

# outer field boundary
def draw_carpet_border(context):
    context.move_to(-x_border, -y_border)
    context.line_to(x_border, -y_border)
    context.line_to(x_border, y_border)
    context.line_to(-x_border, y_border)
    context.close_path()

# outer lines
def draw_outer_lines(context):
    context.move_to(-(x_groundline), -(y_sideline))
    context.line_to((x_groundline), -(y_sideline))
    context.line_to((x_groundline), (y_sideline))
    context.line_to(-(x_groundline), (y_sideline))
    context.line_to(-(x_groundline), (y_sideline))
    context.close_path()
    context.move_to(0, -(y_sideline))
    context.line_to(0, (y_sideline))
    context.close_path()

# inner part of the penalty area (just a rectangle)
def draw_inner_penalty_area(context, sign):
    context.move_to(sign * (x_groundline), -(y_penalty_area))
    context.line_to(sign * (x_groundline), (y_penalty_area))
    context.line_to(sign * (x_penalty_area), (y_penalty_area))
    context.line_to(sign * (x_penalty_area), -(y_penalty_area))
    context.close_path()

def draw_inner_goal_area(context, sign):
    context.move_to(sign * (x_groundline), -(y_goal_area))
    context.line_to(sign * (x_groundline), (y_goal_area))
    context.line_to(sign * (x_goal_area), (y_goal_area))
    context.line_to(sign * (x_goal_area), -(y_goal_area))
    context.close_path()

# inner part of the center circle, including the center dash
def draw_inner_center_circle(context, sign):
    #context.move_to(sign * line_width_2, line_width_2)
    context.move_to(0, 0)
    #angle_offset = math.asin(line_width_2 / (center_circle_radius - line_width_2))
    #context.line_to(sign * line_width_2, line_width_2 / math.tan(angle_offset))
    if sign > 0:
        #context.arc_negative(0, 0, center_circle_radius - line_width_2, pi_2 - angle_offset, -pi_2 + angle_offset)
        context.arc_negative(0, 0, center_circle_radius, pi_2, -pi_2)
    else:
    #    context.arc(0, 0, center_circle_radius - line_width_2, pi_2 + angle_offset, -pi_2 - angle_offset)
        context.arc(0, 0, center_circle_radius, pi_2, -pi_2)
    #context.line_to(sign * line_width_2, -line_width_2)
    #context.line_to(sign * penalty_cross_size_2, -line_width_2)
    #context.line_to(sign * penalty_cross_size_2, line_width_2)
    context.close_path()

# penalty mark
def draw_penalty_cross(context, sign):
    x_base = x_penalty_cross if sign else 0
    #sign = sign if sign else 1
    #context.move_to(sign * (x_base - line_width_2), line_width_2)
    #context.line_to(sign * (x_base - line_width_2), penalty_cross_size_2)
    #context.line_to(sign * (x_base + line_width_2), penalty_cross_size_2)
    #context.line_to(sign * (x_base + line_width_2), line_width_2)
    #context.line_to(sign * (x_base + penalty_cross_size_2), line_width_2)
    #context.line_to(sign * (x_base + penalty_cross_size_2), -line_width_2)
    #context.line_to(sign * (x_base + line_width_2), -line_width_2)
    #context.line_to(sign * (x_base + line_width_2), -penalty_cross_size_2)
    #context.line_to(sign * (x_base - line_width_2), -penalty_cross_size_2)
    #context.line_to(sign * (x_base - line_width_2), -line_width_2)
    #context.line_to(sign * (x_base - penalty_cross_size_2), -line_width_2)
    #context.line_to(sign * (x_base - penalty_cross_size_2), line_width_2)
    context.move_to(sign * (x_base - penalty_cross_size_2), 0)
    context.line_to(sign * (x_base + penalty_cross_size_2), 0)
    context.move_to(sign * (x_base), -penalty_cross_size_2)
    context.line_to(sign * (x_base), penalty_cross_size_2)
    context.close_path()

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

surface = cairo.SVGSurface('field_simple.svg', width, height)
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
#draw_carpet_border(context)
draw_outer_lines(context)
#draw_inner_lines(context, 1)
#draw_inner_lines(context, -1)
draw_inner_penalty_area(context, 1)
draw_inner_penalty_area(context, -1)
draw_inner_goal_area(context, 1)
draw_inner_goal_area(context, -1)
draw_inner_center_circle(context, 1)
draw_inner_center_circle(context, -1)
draw_penalty_cross(context, 1)
draw_penalty_cross(context, -1)
context.stroke()

# draw symmetry axes in blue
#context.set_line_width(svg_symmetryline_width)
#context.set_source_rgb(0, 0, 1)
#context.move_to(-width_in_m * 0.5, 0)
#context.line_to(width_in_m * 0.5, 0)
#context.move_to(0, -height_in_m * 0.5)
#context.line_to(0, height_in_m * 0.5)
#context.stroke()
#context.set_line_width(svg_fieldline_width)

# add dimensions in black
context.set_source_rgb(0, 0, 0)
context.set_font_size(svg_font_size)
context.set_line_width(svg_dimensionline_width)

# dimensions for field boundary
#draw_dimension_horizontal(context, -x_border, x_border, -(y_border + 0.1), 0.2)
#draw_dimension_vertical(context, -y_border, y_border, -(x_border + 0.1), 0.2)
draw_dimension_horizontal(context, x_groundline, x_border, (y_sideline - 0.3), 0.2, label="K")
draw_dimension_vertical(context, y_sideline, y_border, (x_groundline - 0.3), 0.2, label="K")

# dimensions for outer field lines
#draw_dimension_horizontal(context, -(x_groundline + line_width_2), (x_groundline + line_width_2), -(y_sideline + line_width_2 + 0.1), 0.2)
#draw_dimension_vertical(context, -(y_sideline + line_width_2), (y_sideline + line_width_2), -(x_groundline + line_width_2 + 0.1), 0.2)
draw_dimension_horizontal(context, -(x_groundline), (x_groundline), -(y_sideline + line_width_2 + 0.125), 0.2, label="A")
draw_dimension_vertical(context, -(y_sideline), (y_sideline), -(x_groundline + line_width_2 + 0.125), 0.2, label="B")

# dimension for inner half field size
#draw_dimension_horizontal(context, -(x_groundline - line_width_2), -line_width_2, -(y_sideline - line_width_2 - 0.1), 0.2, bar=False)
#draw_dimension_vertical(context, -(y_sideline - line_width_2), (y_sideline - line_width_2), center_circle_radius + 0.5, 0.2, bar=False)

# dimension for inner penalty area length / width
#draw_dimension_horizontal(context, -(x_groundline - line_width_2), -(x_penalty_area + line_width_2), -(y_penalty_area - line_width_2 - 0.1), 0.2, bar=False)
#draw_dimension_vertical(context, -(y_penalty_area - line_width_2), (y_penalty_area - line_width_2), -(x_groundline + line_width_2 - 0.2), 0.2, bar=False)

# dimension for outer penalty area length / width
draw_dimension_horizontal(context, -(x_groundline), -(x_penalty_area), -(y_penalty_area + 0.1), 0.2, label="G")
draw_dimension_vertical(context, -(y_penalty_area), (y_penalty_area), -(x_penalty_area - 0.1), 0.2, across_offset=0.3, label="H")
draw_dimension_horizontal(context, -(x_groundline), -(x_goal_area), -(y_goal_area + 0.1), 0.2, label="E")
draw_dimension_vertical(context, -(y_goal_area), (y_goal_area), -(x_goal_area - 0.1), 0.2, across_offset=0.3, label="F")

# penalty area width from center
#draw_dimension_vertical(context, 0, (y_penalty_area - line_width_2), -(x_penalty_area + line_width_2 + 0.1), 0.2, bar=False)
#draw_dimension_vertical(context, 0, (y_penalty_area + line_width_2), -(x_penalty_area - line_width_2 - 0.3), 0.2)

# dimension for the length between inner sideline and outer penalty area
#draw_dimension_vertical(context, (y_penalty_area + line_width_2), (y_sideline - line_width_2), -(x_groundline - line_width_2 - 0.1), 0.2, bar=False)

# dimension penalty mark
draw_dimension_horizontal(context, (x_penalty_cross), x_groundline, penalty_cross_size*2, 0.2, label="I")
draw_dimension_horizontal(context, (x_penalty_cross - penalty_cross_size_2), (x_penalty_cross + penalty_cross_size_2), 0, 0.2, along_offset=0, bar=True, label="D")

# center circle dimensions
draw_dimension_horizontal(context, -(center_circle_radius), (center_circle_radius), 0, 0.2, bar=True, label="J", along_offset=0.2)
#draw_dimension_horizontal(context, -(center_circle_radius - line_width_2), (center_circle_radius - line_width_2), -0.05, 0.1, along_offset=0.2)
#draw_dimension_vertical(context, -(center_circle_radius + line_width_2), (center_circle_radius + line_width_2), -0.05, 0.1, along_offset=-0.2)
#draw_dimension_vertical(context, -(center_circle_radius - line_width_2), (center_circle_radius - line_width_2), 0.125, 0.1, along_offset=-0.2)

# distance between inner sideline and outer center circle
#draw_dimension_vertical(context, (center_circle_radius + line_width_2), (y_sideline - line_width_2), -(line_width_2 + 0.05), 0.1, bar=False)

# line width
draw_dimension_horizontal(context, -svg_fieldline_width/2, svg_fieldline_width/2, -(y_sideline - 1), 0.2, along_offset=0, bar=False, label="C")

if svg_addnotes:
    context.move_to(0, y_border + 0.2)
    context.show_text("Dimensions are in millimeters. The field is symmetric about both axes (shown in blue).")
    context.move_to(0, y_border + 0.3)
    context.show_text("The penalty marks MUST be crosses and the center dash a rectangular line segment and NOT a circle.")

context.stroke()

